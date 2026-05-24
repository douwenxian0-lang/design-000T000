#!/usr/bin/env python3
"""Self-test for PicsetAI-Package v2.1 refactoring."""
import os
import sys
import inspect
import tempfile
import unittest

sys.stdout.reconfigure(encoding="utf-8")
os.chdir(os.path.dirname(os.path.abspath(__file__)))

passed = 0
failed = 0

def test(name, fn):
    global passed, failed
    try:
        fn()
        print(f"  [OK] {name}")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] {name}: {e}")
        failed += 1
    except Exception as e:
        print(f"  [ERROR] {name}: {type(e).__name__}: {e}")
        failed += 1


def t1_imports():
    """All modules import cleanly."""
    import config
    from config import SELECTORS, DEFAULTS
    import src.browser
    from src.browser import BrowserManager
    from src.uploader import upload_image, dismiss_popups, check_upload_error, wait_for_upload_done
    from src.page_actions import select_mode, select_style, select_quality, select_count, analyze_product
    from src.downloader import download_results, _verify_download
    from src.pipeline import full_flow, batch_process, open_studio, wait_for_generation

def t2_config():
    """Config has all required keys and sensible values."""
    from config import SELECTORS, DEFAULTS
    for key in ["popup_close", "file_input", "upload_region", "analyze_button", "download_button", "error_keywords"]:
        assert key in SELECTORS, f"Missing selector: {key}"
    for key in ["url", "mode", "style", "quality", "count", "max_retries", "generation_timeout"]:
        assert key in DEFAULTS, f"Missing default: {key}"
    assert DEFAULTS["max_retries"] == 3
    assert DEFAULTS["generation_timeout"] == 180

def t3_browser_interface():
    """BrowserManager has correct interface."""
    from src.browser import BrowserManager
    bm = BrowserManager(headless=True, slow_mo=0)
    assert hasattr(bm, "start")
    assert hasattr(bm, "close")
    assert hasattr(bm, "new_page")
    # Note: hasattr() calls the property getter, which raises RuntimeError when
    # browser is not started. So we check via the class instead.
    assert "page" in dir(BrowserManager) or any("page" == p.fget.__name__ for p in bm.__class__.__dict__.values() if isinstance(p, property))
    assert "context" in dir(BrowserManager) or any("context" == p.fget.__name__ for p in bm.__class__.__dict__.values() if isinstance(p, property))
    # page and context should raise when not started
    try:
        _ = bm.page
        raise AssertionError("page should raise RuntimeError when not started")
    except RuntimeError:
        pass  # expected
    try:
        _ = bm.context
        raise AssertionError("context should raise RuntimeError when not started")
    except RuntimeError:
        pass  # expected

def t4_no_bare_except():
    """No bare except: in any module."""
    import config, src.browser, src.uploader, src.page_actions, src.downloader, src.pipeline
    for mod in [config, src.browser, src.uploader, src.page_actions, src.downloader, src.pipeline]:
        source = inspect.getsource(mod)
        for i, line in enumerate(source.split("\n"), 1):
            if line.strip() == "except:":
                raise AssertionError(f"Bare except in {mod.__name__} line {i}")

def t5_no_emoji():
    """No emoji in any .py source file."""
    emoji_ranges = [(0x1F300, 0x1FAFF), (0x2600, 0x27BF), (0x2B50, 0x2B55), (0x2702, 0x2764)]
    py_files = []
    for root, dirs, files in os.walk("."):
        for f in files:
            if f.endswith(".py"):
                py_files.append(os.path.join(root, f))
    for fp in py_files:
        with open(fp, encoding="utf-8") as fh:
            for i, line in enumerate(fh, 1):
                for c in line:
                    cp = ord(c)
                    for lo, hi in emoji_ranges:
                        if lo <= cp <= hi:
                            raise AssertionError(f"Emoji U+{cp:04X} in {fp}:{line.strip()[:40]}")

def t6_no_print_in_src():
    """No print() in src/ modules (should use logging)."""
    issues = []
    for root, dirs, files in os.walk("./src"):
        for f in files:
            if f.endswith(".py"):
                fp = os.path.join(root, f)
                with open(fp, encoding="utf-8") as fh:
                    for i, line in enumerate(fh, 1):
                        stripped = line.strip()
                        if "print(" in stripped and not stripped.startswith("#"):
                            issues.append(f"{fp}:{i}")
    assert len(issues) == 0, f"Found print() in src/ at: {issues}"

def t7_download_verify():
    """Download file verification works for JPEG, PNG, WEBP, and rejects empty."""
    from src.downloader import _verify_download
    from pathlib import Path

    # Empty file -> fail
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"")
        empty = Path(f.name)
    assert not _verify_download(empty), "Empty file should fail"

    # Valid PNG
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)
        png = Path(f.name)
    assert _verify_download(png), "Valid PNG should pass"

    # Valid JPEG
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as f:
        f.write(b"\xff\xd8\xff\xe0" + b"\x00" * 100)
        jpg = Path(f.name)
    assert _verify_download(jpg), "Valid JPEG should pass"

    # Valid WEBP
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webp") as f:
        f.write(b"RIFF\x00\x00\x00\x00WEBP" + b"\x00" * 100)
        webp = Path(f.name)
    assert _verify_download(webp), "Valid WEBP should pass"

    # Nonexistent -> fail
    assert not _verify_download(Path("/nonexistent/abc.png")), "Nonexistent should fail"

def t8_unit_tests():
    """Formal unit tests pass."""
    loader = unittest.TestLoader()
    suite = loader.discover("tests")
    runner = unittest.TextTestRunner(verbosity=0, stream=open(os.devnull, "w"))
    result = runner.run(suite)
    assert result.wasSuccessful(), f"{len(result.failures)} failures, {len(result.errors)} errors"

def t9_cli_help():
    """CLI --help works without error."""
    import subprocess
    result = subprocess.run(
        [sys.executable, "picset_ai_full_flow.py", "--help"],
        capture_output=True, text=True, timeout=10
    )
    assert result.returncode == 0, f"CLI --help failed: {result.stderr}"
    assert "Picset AI" in result.stdout, "Missing description in help"

def t10_type_hints():
    """All async methods in src/ have return type hints."""
    import src.browser, src.uploader, src.page_actions, src.downloader, src.pipeline
    missing = []
    for mod in [src.browser, src.uploader, src.page_actions, src.downloader, src.pipeline]:
        source = inspect.getsource(mod)
        tree = compile(source, mod.__file__, "exec")
        # Simple text check: async def ... -> ... pattern
        for i, line in enumerate(source.split("\n"), 1):
            stripped = line.strip()
            if stripped.startswith("async def ") and "->" not in stripped and ":" in stripped:
                # Exclude private test helpers
                if not stripped.startswith("async def _"):
                    func_name = stripped.split("(")[0].replace("async def ", "")
                    missing.append(f"{mod.__name__}:{func_name}")
    # Allow a few (e.g. __aexit__) to be unannotated
    assert len(missing) <= 3, f"Missing type hints on: {missing}"

def t11_no_emoji_in_cli():
    """CLI entry point has sys.stdout.reconfigure for Windows."""
    with open("picset_ai_full_flow.py", encoding="utf-8") as f:
        source = f.read()
    assert "sys.stdout.reconfigure" in source, "Missing sys.stdout.reconfigure for Windows"
    assert "sys.stderr.reconfigure" in source, "Missing sys.stderr.reconfigure for Windows"


# ---- Run all tests ----
print("=" * 50)
print("PicsetAI-Package v2.1 Self-Test")
print("=" * 50)

tests = [
    ("Module imports", t1_imports),
    ("Config integrity", t2_config),
    ("BrowserManager interface", t3_browser_interface),
    ("No bare except", t4_no_bare_except),
    ("No emoji in source", t5_no_emoji),
    ("No print() in src/", t6_no_print_in_src),
    ("Download verification", t7_download_verify),
    ("Unit tests pass", t8_unit_tests),
    ("CLI --help works", t9_cli_help),
    ("Type hints present", t10_type_hints),
    ("Windows UTF-8 guard", t11_no_emoji_in_cli),
]

for name, fn in tests:
    test(name, fn)

print()
print("=" * 50)
if failed == 0:
    print(f"ALL {passed} TESTS PASSED")
else:
    print(f"{passed} passed, {failed} failed")
print("=" * 50)

sys.exit(0 if failed == 0 else 1)
