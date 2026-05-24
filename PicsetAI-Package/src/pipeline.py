"""Full pipeline orchestration: upload -> select -> generate -> download."""

import asyncio
import logging
from pathlib import Path
from typing import Optional

from playwright.async_api import Page

from config import DEFAULTS, SELECTORS
from src.browser import BrowserManager
from src.uploader import upload_image, dismiss_popups, check_upload_error
from src.page_actions import (
    select_mode,
    select_style,
    select_quality,
    select_count,
    analyze_product,
)
from src.downloader import download_results

logger = logging.getLogger(__name__)


async def open_studio(page: Page) -> None:
    """Open the PicsetAI studio page and dismiss popups."""
    url = DEFAULTS["url"]
    logger.info("Opening PicsetAI: %s", url)
    await page.goto(url, wait_until="domcontentloaded", timeout=60000)
    await page.wait_for_timeout(2000)
    title = await page.title()
    logger.info("Page loaded: %s", title)
    await dismiss_popups(page)


async def wait_for_generation(page: Page, timeout: int = DEFAULTS["generation_timeout"]) -> bool:
    """Poll until generation is complete (download button appears)."""
    logger.info("Waiting for generation (timeout=%ds)...", timeout)
    try:
        for i in range(timeout // 5):
            await page.wait_for_timeout(5000)

            # Check for service errors
            err = await check_upload_error(page)
            if err and any(kw in err for kw in SELECTORS["service_error_keywords"]):
                logger.error("Service error during generation: %s", err)
                return False

            # Check for download button
            download_btns = await page.query_selector_all(SELECTORS["download_button_any"])
            if download_btns:
                visible_btns = [b for b in download_btns if await b.is_visible()]
                if visible_btns:
                    logger.info("Generation complete (%d download buttons)", len(visible_btns))
                    return True

            # Still loading?
            loading_els = await page.query_selector_all(SELECTORS["loading_indicators"])
            if loading_els:
                logger.debug("Still generating... (%ds/%ds)", i * 5 + 5, timeout)

            if (i * 5) % 15 == 0:
                logger.info("Waiting... (%ds/%ds)", i * 5, timeout)

        logger.warning("Generation timed out after %ds", timeout)
        return False
    except Exception as exc:
        logger.error("Error while waiting for generation: %s", exc)
        return False


async def full_flow(
    page: Page,
    image_path: str,
    mode: str = DEFAULTS["mode"],
    style: str = DEFAULTS["style"],
    quality: str = DEFAULTS["quality"],
    count: str = DEFAULTS["count"],
) -> Optional[str]:
    """Execute the complete pipeline for a single image.

    Returns the downloaded file path on success, None on failure.
    """
    logger.info("=" * 50)
    logger.info("Pipeline start: image=%s  mode=%s  style=%s  quality=%s  count=%s",
                image_path, mode, style, quality, count)
    logger.info("=" * 50)

    # 1. Open page
    await open_studio(page)

    # 2. Upload
    if not await upload_image(page, image_path):
        await page.screenshot(path="upload_failed.png", full_page=True)
        logger.error("Upload failed; screenshot saved")
        return None

    # 3. Select options
    await select_mode(page, mode)
    await select_style(page, style)
    await select_quality(page, quality)
    await select_count(page, count)

    # 4. Analyze
    if not await analyze_product(page):
        await page.screenshot(path="analyze_failed.png", full_page=True)
        logger.error("Analyze failed; screenshot saved")
        return None

    # 5. Wait for generation
    if not await wait_for_generation(page):
        await page.screenshot(path="generation_timeout.png", full_page=True)
        logger.error("Generation timed out; screenshot saved")
        return None

    # 6. Download
    result = await download_results(page)

    if result:
        logger.info("Pipeline complete! File saved: %s", result)
    else:
        logger.warning("Pipeline complete but download may have failed")
    return result


async def batch_process(
    browser: BrowserManager,
    folder: str,
    mode: str = DEFAULTS["mode"],
    style: str = DEFAULTS["style"],
    quality: str = DEFAULTS["quality"],
) -> list[dict]:
    """Process all images in a folder sequentially (one page per image)."""
    logger.info("Batch processing: %s", folder)

    images: list[Path] = []
    for ext in DEFAULTS["image_extensions"]:
        images.extend(Path(folder).glob(ext))
        images.extend(Path(folder).glob(ext.upper()))

    logger.info("Found %d images", len(images))

    results: list[dict] = []
    for i, image_path in enumerate(images, 1):
        logger.info("#%d/%d  %s", i, len(images), image_path.name)

        page = await browser.new_page()
        browser.page = page
        try:
            result = await full_flow(page, str(image_path), mode=mode, style=style, quality=quality)
            results.append({"image": str(image_path), "result": result})
        except Exception as exc:
            logger.error("Batch item failed: %s", exc)
            results.append({"image": str(image_path), "result": None})
        finally:
            await page.close()

    # Summary
    success = sum(1 for r in results if r["result"])
    logger.info("Batch complete: %d/%d succeeded", success, len(results))
    for r in results:
        status = "[OK]" if r["result"] else "[FAIL]"
        logger.info("  %s %s", status, Path(r["image"]).name)

    return results
