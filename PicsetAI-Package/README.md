# Picset AI 自动化工具

使用 Playwright 自动化操作 Picset AI 网页版 (https://picsetai.cn/)，完整流程：**上传 → 选择 → 生成 → 下载**。

---

## 项目结构

```
PicsetAI-Package/
  config/
    __init__.py        # 选择器集中管理 + 默认参数
  src/
    browser.py         # 浏览器生命周期管理
    uploader.py        # 上传逻辑 + 重试 + 指数退避
    page_actions.py    # 页面交互（模式/风格/质量/数量）
    downloader.py      # 下载 + 文件校验
    pipeline.py        # 完整流水线编排
  tests/
    test_pipeline.py   # 单元测试
  picset_ai_full_flow.py  # CLI 入口
  requirements.txt        # 锁定版本
  setup.bat / setup.sh    # 一键安装
  .gitignore
```

---

## 快速开始

### Windows 一键安装

双击运行 `setup.bat`，自动完成所有依赖安装。

### 手动安装

```bash
pip install -r requirements.txt
python -m playwright install chromium
```

---

## 使用方法

```bash
# 单张图片（主图模式，默认 3:4 竖版）
python picset_ai_full_flow.py --image ./photo.jpg

# 批量处理文件夹内所有图片
python picset_ai_full_flow.py --folder ./images

# 交互模式
python picset_ai_full_flow.py --interactive

# 指定参数 + 详细日志
python picset_ai_full_flow.py --image ./photo.jpg --mode 详情图 --quality "4K 超清" -v

# 无头模式
python picset_ai_full_flow.py --image ./photo.jpg --headless
```

---

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--image` / `-i` | 单张图片路径 | - |
| `--folder` / `-f` | 图片文件夹路径（批量） | - |
| `--mode` / `-m` | 主图 / 详情图 | 主图 |
| `--style` / `-s` | 3:4 竖版 / 1:1 方版 / 16:9 横版 | 3:4 竖版 |
| `--quality` / `-q` | 2K 高清 / 4K 超清 | 2K 高清 |
| `--count` / `-c` | 1 张 / 4 张 | 1 张 |
| `--headless` | 无头模式（后台运行） | False |
| `--verbose` / `-v` | 详细日志（DEBUG级别） | False |
| `--interactive` | 交互模式 | False |

---

## 完整流程

```
打开页面 → 上传图片 → 选择模式 → 选择风格
     → 选择质量 → 点击分析 → 等待生成 → 下载结果 → 文件校验
```

---

## v2.1 更新内容

- **修复**: 移除所有 emoji，解决 Windows GBK 崩溃问题
- **修复**: 裸 `except:` 改为 `except Exception as e`，不再吞异常
- **新增**: `logging` 模块替代 `print()`，支持 `-v` 详细日志
- **新增**: 下载文件校验（检查文件头 JPEG/PNG/WEBP）
- **新增**: 上传重试指数退避（2s → 4s → 8s）
- **新增**: 选择器集中管理（`config/`），UI 改版只改一处
- **新增**: `.gitignore`、单元测试、版本锁定 `requirements.txt`
- **重构**: 单文件 665 行拆分为 6 个模块，职责清晰

---

## 注意事项

- 首次运行自动下载 Chromium（约 150MB）
- 如遇 Chromium 下载失败，编辑 `setup.bat`，取消 `set HTTPS_PROXY=...` 的注释并填入代理地址
- 支持格式：JPG / PNG / WEBP
- 单次最多上传 6 张图片
- 生成时间：30-60 秒（视服务器负载）
- Windows 用户：已内置 `sys.stdout.reconfigure(encoding='utf-8')` 防止中文乱码

---

**版本**: 2.1
**创建时间**: 2026-05-12
**更新时间**: 2026-05-24
