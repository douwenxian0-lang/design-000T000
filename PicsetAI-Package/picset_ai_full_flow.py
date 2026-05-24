#!/usr/bin/env python3
"""PicsetAI-Package CLI entry point.

Usage:
    python picset_ai_full_flow.py --image ./product.jpg
    python picset_ai_full_flow.py --folder ./images
    python picset_ai_full_flow.py --interactive
"""

import argparse
import asyncio
import logging
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows (prevents GBK crash with Chinese characters)
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]

from config import DEFAULTS
from src.browser import BrowserManager
from src.pipeline import full_flow, batch_process, open_studio
from src.uploader import upload_image, dismiss_popups
from src.page_actions import (
    select_mode,
    select_style,
    analyze_product,
)
from src.downloader import download_results


def setup_logging(verbose: bool = False) -> None:
    """Configure logging with console output."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


async def interactive_mode() -> None:
    """Interactive REPL for step-by-step control."""
    logger = logging.getLogger("interactive")
    logger.info("PicsetAI Interactive Mode")

    async with BrowserManager(headless=False) as browser:
        await open_studio(browser.page)

        while True:
            print("\nCommands:")
            print("  1. upload [path]        - Upload image")
            print("  2. mode [main|detail]   - Select mode")
            print("  3. style [style]        - Select style")
            print("  4. analyze              - Analyze product")
            print("  5. wait                 - Wait for generation")
            print("  6. download             - Download results")
            print("  7. shot                 - Take screenshot")
            print("  8. close                - Dismiss popups")
            print("  9. flow                 - Run full pipeline")
            print("  0. quit                 - Exit")

            cmd = input("\n> ").strip()

            if cmd == "quit" or cmd == "0":
                break
            elif cmd.startswith("upload ") or cmd.startswith("1 "):
                path = cmd.split(maxsplit=1)[1] if " " in cmd else ""
                if path:
                    await upload_image(browser.page, path)
                else:
                    print("  Usage: upload <image_path>")
            elif cmd.startswith("mode ") or cmd.startswith("2 "):
                m = cmd.split(maxsplit=1)[1] if " " in cmd else "main"
                await select_mode(browser.page, m)
            elif cmd.startswith("style ") or cmd.startswith("3 "):
                s = cmd.split(maxsplit=1)[1] if " " in cmd else ""
                if s:
                    await select_style(browser.page, s)
            elif cmd == "analyze" or cmd == "4":
                await analyze_product(browser.page)
            elif cmd == "wait" or cmd == "5":
                from src.pipeline import wait_for_generation
                await wait_for_generation(browser.page)
            elif cmd == "download" or cmd == "6":
                await download_results(browser.page)
            elif cmd == "shot" or cmd == "7":
                await browser.page.screenshot(path="screenshot.png", full_page=True)
                logger.info("Screenshot saved: screenshot.png")
            elif cmd == "close" or cmd == "8":
                await dismiss_popups(browser.page)
                logger.info("Popups dismissed")
            elif cmd == "flow" or cmd == "9":
                image = input("  Image path: ").strip()
                if image:
                    await full_flow(browser.page, image)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Picset AI automation pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python picset_ai_full_flow.py --image ./product.jpg
  python picset_ai_full_flow.py --folder ./images
  python picset_ai_full_flow.py --image ./photo.jpg --mode detail --quality "4K"
  python picset_ai_full_flow.py --interactive
        """,
    )
    parser.add_argument("--image", "-i", help="Single image path")
    parser.add_argument("--folder", "-f", help="Image folder (batch)")
    parser.add_argument("--mode", "-m", default=DEFAULTS["mode"],
                        help="Mode: main / detail (default: main)")
    parser.add_argument("--style", "-s", default=DEFAULTS["style"],
                        help="Style: 3:4 / 1:1 / 16:9 (default: 3:4)")
    parser.add_argument("--quality", "-q", default=DEFAULTS["quality"],
                        help="Quality: 2K / 4K (default: 2K)")
    parser.add_argument("--count", "-c", default=DEFAULTS["count"],
                        help="Count: 1 / 4 (default: 1)")
    parser.add_argument("--interactive", action="store_true",
                        help="Interactive mode")
    parser.add_argument("--headless", action="store_true",
                        help="Headless mode (no browser window)")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Enable debug logging")

    args = parser.parse_args()
    setup_logging(verbose=args.verbose)

    if args.interactive:
        asyncio.run(interactive_mode())
    elif args.folder:
        async def _batch():
            async with BrowserManager(headless=args.headless) as browser:
                await batch_process(browser, args.folder, args.mode, args.style, args.quality)
        asyncio.run(_batch())
    elif args.image:
        async def _single():
            async with BrowserManager(headless=args.headless) as browser:
                await full_flow(browser.page, args.image, args.mode, args.style, args.quality, args.count)
        asyncio.run(_single())
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
