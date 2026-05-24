@echo off
chcp 65001 >nul
echo ========================================
echo   Picset AI 自动化工具 - Windows 安装
echo ========================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Install Python 3.8+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/3] Installing Python dependencies...
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
if errorlevel 1 (
    echo [ERROR] pip install failed. Check your network.
    pause
    exit /b 1
)

echo.
echo [2/3] Installing Playwright Chromium...
REM Uncomment and set proxy if needed:
REM set HTTPS_PROXY=http://127.0.0.1:7890
python -m playwright install chromium
if errorlevel 1 (
    echo [ERROR] Chromium install failed.
    echo   Tip: Set HTTPS_PROXY above if you need a proxy.
    pause
    exit /b 1
)

echo.
echo [3/3] Verifying installation...
python -c "from playwright.sync_api import sync_playwright; print('Playwright OK')"
if errorlevel 1 (
    echo [ERROR] Playwright verification failed.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Installation complete!
echo ========================================
echo.
echo Usage:
echo   Single image : python picset_ai_full_flow.py --image ./photo.jpg
echo   Batch folder  : python picset_ai_full_flow.py --folder ./images
echo   Interactive   : python picset_ai_full_flow.py --interactive
echo   Verbose log   : python picset_ai_full_flow.py --image ./photo.jpg -v
echo.
pause
