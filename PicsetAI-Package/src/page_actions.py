"""Page interaction helpers: select mode / style / quality / count / analyze."""

import logging
from typing import Optional

from playwright.async_api import Page

from config import SELECTORS

logger = logging.getLogger(__name__)


async def select_mode(page: Page, mode: str = "主图") -> bool:
    """Select generation mode (main image / detail image)."""
    logger.info("Selecting mode: %s", mode)
    try:
        sel = SELECTORS["mode_button"].format(mode=mode)
        mode_btn = await page.wait_for_selector(sel, timeout=5000)
        await mode_btn.click()
        await page.wait_for_timeout(500)
        logger.info("Mode selected: %s", mode)
        return True
    except Exception as exc:
        logger.warning("Mode selection failed: %s", exc)
        return False


async def select_style(page: Page, style: str = "3:4 竖版") -> bool:
    """Select size/style from dropdown."""
    logger.info("Selecting style: %s", style)
    try:
        # Open dropdown
        style_dropdown = await page.query_selector(SELECTORS["style_dropdown"])
        if style_dropdown:
            await style_dropdown.click()
            await page.wait_for_timeout(500)
            option = await page.query_selector(f"text={style}")
            if option:
                await option.click()
                await page.wait_for_timeout(300)
                logger.info("Style selected: %s", style)
                return True

        # Fallback: direct combobox match
        sel = SELECTORS["style_combobox"].format(style=style)
        style_btn = await page.query_selector(sel)
        if style_btn:
            await style_btn.click()
            await page.wait_for_timeout(500)
            logger.info("Style selected (fallback): %s", style)
            return True

        logger.warning("Style option not found: %s", style)
        return False
    except Exception as exc:
        logger.warning("Style selection failed: %s", exc)
        return False


async def select_quality(page: Page, quality: str = "2K 高清") -> bool:
    """Select image quality."""
    logger.info("Selecting quality: %s", quality)
    try:
        sel = SELECTORS["quality_button"].format(quality=quality)
        quality_btn = await page.query_selector(sel)
        if quality_btn:
            await quality_btn.click()
            await page.wait_for_timeout(500)
            logger.info("Quality selected: %s", quality)
            return True
        logger.warning("Quality option not found: %s", quality)
        return False
    except Exception as exc:
        logger.warning("Quality selection failed: %s", exc)
        return False


async def select_count(page: Page, count: str = "1 张") -> bool:
    """Select generation count."""
    logger.info("Selecting count: %s", count)
    try:
        sel = SELECTORS["count_button"].format(count=count)
        count_btn = await page.query_selector(sel)
        if count_btn:
            await count_btn.click()
            await page.wait_for_timeout(500)
            logger.info("Count selected: %s", count)
            return True
        logger.warning("Count option not found: %s", count)
        return False
    except Exception as exc:
        logger.warning("Count selection failed: %s", exc)
        return False


async def analyze_product(page: Page) -> bool:
    """Click the 'analyze product' button after upload."""
    logger.info("Analyzing product...")
    try:
        from src.uploader import dismiss_popups
        await dismiss_popups(page)
        await page.wait_for_timeout(500)

        analyze_btn = await page.wait_for_selector(
            SELECTORS["analyze_button"], timeout=10000
        )
        disabled = await analyze_btn.get_attribute("disabled")
        aria_disabled = await analyze_btn.get_attribute("aria-disabled")

        if disabled is not None or aria_disabled == "true":
            logger.warning("Analyze button is still disabled; upload may have failed")
            return False

        await analyze_btn.click()
        logger.info("Analyze button clicked")
        return True
    except Exception as exc:
        logger.error("Analyze button click failed: %s", exc)
        return False
