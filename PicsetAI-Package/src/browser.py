"""Browser lifecycle management for PicsetAI automation."""

import logging
from pathlib import Path
from typing import Optional

from playwright.async_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    async_playwright,
)

from config import DEFAULTS

logger = logging.getLogger(__name__)


class BrowserManager:
    """Manage Playwright browser lifecycle with context reuse."""

    def __init__(
        self,
        headless: bool = DEFAULTS["headless"],
        slow_mo: int = DEFAULTS["slow_mo"],
        download_dir: str = DEFAULTS["download_dir"],
    ) -> None:
        self.headless = headless
        self.slow_mo = slow_mo
        self.download_dir = Path(download_dir)
        self._playwright: Optional[Playwright] = None
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None
        self._page: Optional[Page] = None

    # -- async context manager --------------------------------------------------

    async def __aenter__(self) -> "BrowserManager":
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:  # noqa: ANN001
        await self.close()

    # -- properties -------------------------------------------------------------

    @property
    def page(self) -> Page:
        if self._page is None:
            raise RuntimeError("Browser not started. Call start() first.")
        return self._page

    @page.setter
    def page(self, value: Page) -> None:
        self._page = value

    @property
    def context(self) -> BrowserContext:
        if self._context is None:
            raise RuntimeError("Browser not started. Call start() first.")
        return self._context

    # -- lifecycle --------------------------------------------------------------

    async def start(self) -> None:
        """Launch browser, create context and first page."""
        logger.info("Initializing browser (headless=%s, slow_mo=%dms)", self.headless, self.slow_mo)
        self.download_dir.mkdir(parents=True, exist_ok=True)

        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(
            headless=self.headless,
            slow_mo=self.slow_mo,
            args=["--start-maximized"],
        )
        self._context = await self._browser.new_context(
            viewport=DEFAULTS["viewport"],
            user_agent=DEFAULTS["user_agent"],
            accept_downloads=True,
        )
        await self._context.set_extra_http_headers(
            {"Accept-Language": DEFAULTS["accept_language"]}
        )
        self._page = await self._context.new_page()
        logger.info("Browser ready")

    async def close(self) -> None:
        """Shut down browser cleanly."""
        logger.info("Closing browser")
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()
        logger.info("Browser closed")

    async def new_page(self) -> Page:
        """Open a new page in the existing context (for batch processing)."""
        page = await self._context.new_page()
        return page
