#!/usr/bin/env bash
# PicsetAI-Package - macOS/Linux install
set -e

echo "========================================"
echo "  Picset AI Automation - Install"
echo "========================================"

# Check Python
if ! command -v python3 &>/dev/null; then
    echo "[ERROR] python3 not found. Install Python 3.8+ first."
    exit 1
fi

echo "[1/3] Installing Python dependencies..."
pip3 install -r requirements.txt

echo "[2/3] Installing Playwright Chromium..."
python3 -m playwright install chromium

echo "[3/3] Verifying..."
python3 -c "from playwright.sync_api import sync_playwright; print('Playwright OK')"

echo ""
echo "========================================"
echo "  Installation complete!"
echo "========================================"
echo ""
echo "Usage:"
echo "  Single image : python3 picset_ai_full_flow.py --image ./photo.jpg"
echo "  Batch folder  : python3 picset_ai_full_flow.py --folder ./images"
echo "  Interactive   : python3 picset_ai_full_flow.py --interactive"
