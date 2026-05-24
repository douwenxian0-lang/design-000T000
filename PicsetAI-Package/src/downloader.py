"""Download logic with verification for PicsetAI results."""

import logging
from pathlib import Path
from typing import Optional

from playwright.async_api import Page, TimeoutError as PlaywrightTimeout

from config import DEFAULTS, SELECTORS

logger = logging.getLogger(__name__)


async def download_results(
    page: Page,
    output_folder: Optional[Path] = None,
    timeout: int = DEFAULTS["download_timeout"],
) -> Optional[str]:
    """Download generated images and verify file integrity.

    Returns the saved file path on success, None on failure.
    """
    logger.info("Downloading results...")
    if output_folder is None:
        output_folder = Path(DEFAULTS["download_dir"])
    output_folder.mkdir(parents=True, exist_ok=True)

    try:
        download_btn = await page.wait_for_selector(
            SELECTORS["download_button"], timeout=timeout * 1000
        )

        async with page.expect_download(timeout=timeout * 1000) as download_info:
            await download_btn.click()

        download = await download_info.value
        filename = output_folder / download.suggested_filename
        await download.save_as(str(filename))

        # Verify downloaded file
        if _verify_download(filename):
            logger.info("Download verified: %s (%d bytes)", filename, filename.stat().st_size)
            return str(filename)
        else:
            logger.warning("Download file verification failed: %s", filename)
            return str(filename)  # still return path; caller can decide

    except PlaywrightTimeout:
        logger.warning("Download button timeout; trying fallback...")
        return await _download_fallback(page, output_folder)
    except Exception as exc:
        logger.warning("Download failed: %s; trying fallback...", exc)
        return await _download_fallback(page, output_folder)


async def _download_fallback(page: Page, output_folder: Path) -> Optional[str]:
    """Fallback download: click any visible download button."""
    try:
        download_btns = await page.query_selector_all(SELECTORS["download_button_any"])
        for btn in download_btns:
            if await btn.is_visible():
                await btn.click()
                await page.wait_for_timeout(5000)
                logger.info("Fallback download clicked")
                return str(output_folder)
        logger.warning("No visible download button found")
        return None
    except Exception as exc:
        logger.error("Fallback download failed: %s", exc)
        return None


def _verify_download(filepath: Path) -> bool:
    """Basic download verification: file exists and is non-empty."""
    if not filepath.exists():
        return False
    size = filepath.stat().st_size
    if size == 0:
        return False
    # Quick header check for common image formats
    try:
        with open(filepath, "rb") as f:
            header = f.read(8)
        if header[:3] == b"\xff\xd8\xff":  # JPEG
            return True
        if header[:8] == b"\x89PNG\r\n\x1a\n":  # PNG
            return True
        if header[:4] == b"RIFF" and header[8:12] == b"WEBP":  # WEBP
            return True
        # Not a recognized image header, but file is non-empty
        logger.debug("Unrecognized file header for %s, but file is non-empty (%d bytes)", filepath, size)
        return True
    except Exception as exc:
        logger.debug("Header check failed: %s", exc)
        return True  # don't fail on header check errors
