"""PicsetAI-Package config: selectors and defaults."""

# ---------------------------------------------------------------------------
# CSS selectors – centralized so UI changes only need editing here
# ---------------------------------------------------------------------------
SELECTORS = {
    # Popups
    "popup_close": "button:has-text('立即体验'), button:has-text('关闭'):not(:has-text('生成结果'))",

    # Upload area
    "upload_region": "region:has([class*='dashed']), [class*='dashed'][class*='border']",
    "file_input": "input[type='file']",

    # Upload verification
    "analyze_button": "button:has-text('分析产品')",
    "preview_image": "[class*='preview'], [class*='thumbnail'], img[src*='blob']",

    # Error detection
    "error_texts": [
        "text=审核服务暂不可用",
        "text=上传失败",
        "text=请上传图片",
        "text=服务暂时不可用",
    ],
    "error_containers": [
        "[class*='toast']:has-text('审核')",
        "[class*='notification']:has-text('审核')",
        "[class*='message']:has-text('审核')",
        "[class*='error']",
    ],

    # Mode / style / quality / count
    "mode_button": "button[aria-label*='{mode}'], button:has-text('{mode}'):not([disabled])",
    "style_dropdown": "region:has(heading:has-text('一键生成')) [class*='combobox'], combobox:has-text('3:4')",
    "style_combobox": "[class*='combobox']:has-text('{style}')",
    "quality_button": "combobox:has-text('{quality}'), [class*='dropdown']:has-text('{quality}')",
    "count_button": "combobox:has-text('{count}'), [class*='count']:has-text('{count}')",

    # Download
    "download_button": "button:has-text('下载'):visible",
    "download_button_any": "button:has-text('下载')",

    # Loading / progress
    "loading_indicators": (
        "[class*='progress'], [class*='loading'], [class*='spinner'], "
        "text=生成中, text=处理中, text=稍等"
    ),

    # Error keywords
    "error_keywords": ["审核", "失败", "错误", "不可用", "error", "failed"],
    "service_error_keywords": ["审核", "服务不可用", "failed", "error"],
}

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------
DEFAULTS = {
    "url": "https://picsetai.cn/studio-genesis",
    "mode": "主图",
    "style": "3:4 竖版",
    "quality": "2K 高清",
    "count": "1 张",
    "headless": False,
    "slow_mo": 300,
    "viewport": {"width": 1920, "height": 1080},
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "accept_language": "zh-CN,zh;q=0.9,en;q=0.8",
    "download_dir": "./downloads",
    "upload_timeout": 30,
    "generation_timeout": 180,
    "download_timeout": 60,
    "max_retries": 3,
    "image_extensions": ["*.jpg", "*.jpeg", "*.png", "*.webp"],
}
