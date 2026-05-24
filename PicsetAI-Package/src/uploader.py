"""Upload logic with retry and error detection for PicsetAI."""

import logging
import os
from typing import Optional

from playwright.async_api import Page, TimeoutError as PlaywrightTimeout

from config import DEFAULTS, SELECTORS

logger = logging.getLogger(__name__)


async def dismiss_popups(page: Page) -> None:
    """Close any popups or notifications that might block interaction."""
    try:
        close_btn = await page.query_selector(SELECTORS["popup_close"])
        if close_btn:
            await close_btn.click()
            await page.wait_for_timeout(500)
    except Exception as exc:
        logger.debug("No popup to dismiss: %s", exc)
    # ESC as fallback
    await page.keyboard.press("Escape")
    await page.wait_for_timeout(300)


async def check_upload_error(page: Page) -> Optional[str]:
    """Detect upload / review error notifications. Returns error text or None."""
    all_selectors = SELECTORS["error_texts"] + SELECTORS["error_containers"]
    for sel in all_selectors:
        try:
            el = await page.query_selector(sel)
            if el and await el.is_visible():
                text = await el.inner_text()
                if any(kw in text for kw in SELECTORS["error_keywords"]):
                    return text[:200]
        except Exception:
            pass
    return None


async def wait_for_upload_done(page: Page, timeout: int = DEFAULTS["upload_timeout"]) -> bool:
    """Poll until upload is confirmed (analyze button enabled or preview visible)."""
    for i in range(timeout // 2):
        await page.wait_for_timeout(2000)

        # Check for error notifications
        err = await check_upload_error(page)
        if err:
            logger.warning("Error notification detected: %s", err)

        # Check if "analyze product" button is enabled
        try:
            btn = await page.query_selector(SELECTORS["analyze_button"])
            if btn:
                is_disabled = await btn.get_attribute("disabled")
                is_aria_disabled = await btn.get_attribute("aria-disabled")
                if not is_disabled and is_aria_disabled != "true":
                    try:
                        await btn.click(timeout=1000)
                        logger.info("Upload confirmed (analyze button enabled)")
                        return True
                    except Exception:
                        pass
        except Exception:
            pass

        # Fallback: check for preview thumbnails
        previews = await page.query_selector_all(SELECTORS["preview_image"])
        if previews:
            logger.info("Upload confirmed (preview visible, %d items)", len(previews))
            return True

        logger.debug("Waiting for upload... (%ds/%ds)", i * 2 + 2, timeout)

    logger.warning("Upload wait timed out after %ds", timeout)
    return False


async def upload_image(
    page: Page,
    image_path: str,
    max_retries: int = DEFAULTS["max_retries"],
) -> bool:
    """Upload an image with retry and exponential backoff.

    Returns True on success.
    """
    logger.info("Uploading image: %s", image_path)

    if not os.path.exists(image_path):
        logger.error("File not found: %s", image_path)
        return False

    abs_path = os.path.abspath(image_path)

    for attempt in range(1, max_retries + 1):
        try:
            logger.info("Upload attempt %d/%d", attempt, max_retries)
            await dismiss_popups(page)

            # Wait for upload region
            await page.wait_for_selector(SELECTORS["upload_region"], timeout=10000)

            # Set file input
            file_input = await page.wait_for_selector(SELECTORS["file_input"], timeout=5000)
            await file_input.set_input_files(abs_path)
            logger.info("File selected, waiting for upload...")

            # Wait for upload to complete
            upload_ok = await wait_for_upload_done(page)

            # Check for post-upload errors
            err = await check_upload_error(page)
            if err:
                if "审核" in err or "不可用" in err:
                    logger.warning("Server review service error: %s", err)
                    if attempt < max_retries:
                        backoff = 2 ** attempt
                        logger.info("Retrying in %ds (exponential backoff)...", backoff)
                        await page.wait_for_timeout(backoff * 1000)
                        continue
                    else:
                        logger.error("Max retries reached; server review unavailable")
                        return False
                else:
                    logger.warning("Upload error: %s", err)
                    if attempt < max_retries:
                        continue

            if upload_ok:
                return True

        except PlaywrightTimeout:
            logger.warning("Timeout on attempt %d", attempt)
            if attempt < max_retries:
                await page.wait_for_timeout(3000)
                continue
        except Exception as exc:
            logger.error("Upload exception: %s", exc)
            if attempt < max_retries:
                backoff = 2 ** attempt
                await page.wait_for_timeout(backoff * 1000)
                continue

    logger.error("Upload failed after %d attempts", max_retries)
    return False
