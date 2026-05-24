"""Unit tests for non-browser logic in PicsetAI-Package."""

import unittest
from pathlib import Path
from unittest.mock import MagicMock, AsyncMock, patch

# We test pure functions / sync helpers only; browser calls are mocked.


class TestConfig(unittest.TestCase):
    """Verify config module loads correctly."""

    def test_selectors_has_required_keys(self):
        from config import SELECTORS
        required = [
            "popup_close", "file_input", "upload_region",
            "analyze_button", "download_button", "error_keywords",
        ]
        for key in required:
            self.assertIn(key, SELECTORS, f"Missing selector: {key}")

    def test_defaults_has_required_keys(self):
        from config import DEFAULTS
        required = ["url", "mode", "style", "quality", "count", "max_retries"]
        for key in required:
            self.assertIn(key, DEFAULTS, f"Missing default: {key}")


class TestDownloaderVerify(unittest.TestCase):
    """Test download file verification."""

    def test_verify_nonexistent_file(self):
        from src.downloader import _verify_download
        self.assertFalse(_verify_download(Path("/nonexistent/file.png")))

    def test_verify_empty_file(self):
        import tempfile, os
        from src.downloader import _verify_download
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"")
            path = Path(f.name)
        try:
            self.assertFalse(_verify_download(path))
        finally:
            os.unlink(path)

    def test_verify_valid_png(self):
        import tempfile, os
        from src.downloader import _verify_download
        png_header = b"\x89PNG\r\n\x1a\n" + b"\x00" * 100
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:
            f.write(png_header)
            path = Path(f.name)
        try:
            self.assertTrue(_verify_download(path))
        finally:
            os.unlink(path)

    def test_verify_valid_jpeg(self):
        import tempfile, os
        from src.downloader import _verify_download
        jpeg_header = b"\xff\xd8\xff\xe0" + b"\x00" * 100
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as f:
            f.write(jpeg_header)
            path = Path(f.name)
        try:
            self.assertTrue(_verify_download(path))
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()
