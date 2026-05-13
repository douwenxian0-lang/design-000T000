#!/usr/bin/env python3
"""
Picset AI 完整自动化流程
上传 → 选择 → 生成 → 下载

使用方法:
    python picset_ai_full_flow.py --image ./images/product.jpg
    python picset_ai_full_flow.py --folder ./images --style "3:4 竖版"
    python picset_ai_full_flow.py --interactive
"""

import asyncio
import argparse
import os
import sys
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout


class PicsetAIFullFlow:
    """Picset AI 完整自动化流程"""

    def __init__(self, headless=False, slow_mo=300):
        self.headless = headless
        self.slow_mo = slow_mo
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.download_path = None

    async def __aenter__(self):
        await self.init_browser()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def init_browser(self):
        """初始化浏览器"""
        print("🚀 初始化浏览器...")
        self.playwright = await async_playwright().start()

        self.browser = await self.playwright.chromium.launch(
            headless=self.headless,
            slow_mo=self.slow_mo,
            args=['--start-maximized']
        )

        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )

        # 设置下载路径
        self.download_path = Path("./downloads")
        self.download_path.mkdir(exist_ok=True)
        await self.context.set_extra_http_headers({
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
        })

        self.page = await self.context.new_page()
        print("✅ 浏览器就绪")

    async def open_studio(self):
        """打开全品类商品图页面"""
        print("🌐 打开 Picset AI...")
        await self.page.goto("https://picsetai.cn/studio-genesis", wait_until="domcontentloaded", timeout=60000)
        await self.page.wait_for_timeout(3000)
        print(f"✅ 页面加载: {await self.page.title()}")

        # 关闭弹窗
        try:
            await self.page.keyboard.press('Escape')
            await self.page.wait_for_timeout(500)
        except:
            pass

    async def upload_image(self, image_path):
        """上传图片"""
        print(f"📤 上传图片: {image_path}")

        if not os.path.exists(image_path):
            print(f"❌ 文件不存在: {image_path}")
            return False

        try:
            # 等待文件上传 input 出现
            file_input = await self.page.wait_for_selector("input[type='file']", timeout=10000)
            await file_input.set_input_files(os.path.abspath(image_path))

            # 等待上传完成
            await self.page.wait_for_timeout(3000)
            print("✅ 图片上传成功")
            return True
        except Exception as e:
            print(f"❌ 上传失败: {e}")
            return False

    async def select_mode(self, mode="主图"):
        """选择生成模式

        Args:
            mode: 主图 / 详情图
        """
        print(f"🎯 选择模式: {mode}")

        try:
            mode_btn = await self.page.wait_for_selector(f"button:has-text('{mode}')", timeout=5000)
            await mode_btn.click()
            await self.page.wait_for_timeout(500)
            print(f"✅ 已选择模式: {mode}")
            return True
        except Exception as e:
            print(f"⚠️ 模式选择失败: {e}")
            return False

    async def select_style(self, style="3:4 竖版"):
        """选择尺寸风格

        Args:
            style: 3:4 竖版 / 1:1 方版 / 16:9 横版
        """
        print(f"🎨 选择风格: {style}")

        try:
            style_btn = await self.page.wait_for_selector(f"button:has-text('{style}')", timeout=5000)
            await style_btn.click()
            await self.page.wait_for_timeout(500)
            print(f"✅ 已选择风格: {style}")
            return True
        except Exception as e:
            print(f"⚠️ 风格选择失败: {e}")
            return False

    async def select_quality(self, quality="2K 高清"):
        """选择图片质量

        Args:
            quality: 2K 高清 / 4K 超清
        """
        print(f"📷 选择质量: {quality}")

        try:
            quality_btn = await self.page.wait_for_selector(f"button:has-text('{quality}')", timeout=5000)
            await quality_btn.click()
            await self.page.wait_for_timeout(500)
            print(f"✅ 已选择质量: {quality}")
            return True
        except Exception as e:
            print(f"⚠️ 质量选择失败: {e}")
            return False

    async def select_count(self, count="1 张"):
        """选择生成数量

        Args:
            count: 1 张 / 4 张
        """
        print(f"🔢 选择数量: {count}")

        try:
            count_btn = await self.page.wait_for_selector(f"button:has-text('{count}')", timeout=5000)
            await count_btn.click()
            await self.page.wait_for_timeout(500)
            print(f"✅ 已选择数量: {count}")
            return True
        except Exception as e:
            print(f"⚠️ 数量选择失败: {e}")
            return False

    async def analyze_product(self):
        """点击分析产品按钮"""
        print("🔍 分析产品...")

        try:
            # 查找分析产品按钮
            analyze_btn = await self.page.wait_for_selector(
                "button:has-text('分析产品'), button:has-text('生成')",
                timeout=10000
            )
            await analyze_btn.click()
            print("✅ 已点击分析按钮")
            return True
        except Exception as e:
            print(f"❌ 分析按钮点击失败: {e}")
            return False

    async def wait_for_generation(self, timeout=120):
        """等待生成完成

        Args:
            timeout: 超时时间（秒）
        """
        print("⏳ 等待生成完成...")

        try:
            # 等待最多 timeout 秒
            # 检查是否出现"下载"按钮或"已完成"状态
            for i in range(timeout // 5):
                await self.page.wait_for_timeout(5000)

                # 检查是否有下载按钮
                download_btn = await self.page.query_selector("button:has-text('下载')")
                if download_btn:
                    print("✅ 生成完成！")
                    return True

                # 检查进度条
                progress = await self.page.query_selector("[class*='progress'], [class*='loading']")
                if progress:
                    print(f"⏳ 仍在生成中... ({i*5}s)")

                print(f"⏳ 等待中... ({i*5}s/{timeout}s)")

            print("⚠️ 生成超时")
            return False

        except Exception as e:
            print(f"⚠️ 等待生成时出错: {e}")
            return False

    async def download_results(self, output_folder=None):
        """下载生成的结果"""
        print("⬇️ 下载结果...")

        if output_folder is None:
            output_folder = self.download_path
        else:
            output_folder = Path(output_folder)
            output_folder.mkdir(parents=True, exist_ok=True)

        try:
            # 等待下载按钮出现
            download_btn = await self.page.wait_for_selector("button:has-text('下载')", timeout=30000)

            # 点击下载
            async with self.page.expect_download() as download_info:
                await download_btn.click()

            download = await download_info.value
            filename = output_folder / download.suggested_filename
            await download.save_as(str(filename))
            print(f"✅ 下载完成: {filename}")
            return str(filename)

        except Exception as e:
            print(f"❌ 下载失败: {e}")
            return None

    async def full_flow(self, image_path, mode="主图", style="3:4 竖版", quality="2K 高清", count="1 张"):
        """完整流程：上传 → 选择 → 生成 → 下载

        Args:
            image_path: 图片路径
            mode: 模式（主图/详情图）
            style: 风格（3:4 竖版/1:1 方版等）
            quality: 质量（2K 高清/4K 超清）
            count: 数量（1 张/4 张）
        """
        print("\n" + "="*60)
        print("Picset AI 完整自动化流程")
        print("="*60)
        print(f"📷 图片: {image_path}")
        print(f"🎯 模式: {mode}")
        print(f"🎨 风格: {style}")
        print(f"📷 质量: {quality}")
        print(f"🔢 数量: {count}")
        print("="*60 + "\n")

        # 1. 打开页面
        await self.open_studio()

        # 2. 上传图片
        if not await self.upload_image(image_path):
            return False

        # 3. 选择模式
        await self.select_mode(mode)

        # 4. 选择风格
        await self.select_style(style)

        # 5. 选择质量
        await self.select_quality(quality)

        # 6. 选择数量
        await self.select_count(count)

        # 7. 点击分析
        await self.analyze_product()

        # 8. 等待生成
        await self.wait_for_generation(timeout=120)

        # 9. 下载结果
        result = await self.download_results()

        print("\n" + "="*60)
        if result:
            print(f"✅ 流程完成！文件已保存: {result}")
        else:
            print("⚠️ 流程完成，但下载可能失败")
        print("="*60)

        return result

    async def batch_process(self, folder, mode="主图", style="3:4 竖版", quality="2K 高清"):
        """批量处理文件夹中的所有图片"""
        print(f"\n📦 批量处理: {folder}")

        # 获取所有图片
        images = []
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.webp']:
            images.extend(Path(folder).glob(ext))
            images.extend(Path(folder).glob(ext.upper()))

        print(f"📊 找到 {len(images)} 张图片")

        results = []
        for i, image_path in enumerate(images, 1):
            print(f"\n{'#'*60}")
            print(f"处理第 {i}/{len(images)} 张: {image_path.name}")
            print(f"{'#'*60}")

            # 打开新页面处理
            page = await self.context.new_page()
            self.page = page

            try:
                result = await self.full_flow(
                    str(image_path),
                    mode=mode,
                    style=style,
                    quality=quality
                )
                results.append({"image": str(image_path), "result": result})
            except Exception as e:
                print(f"❌ 处理失败: {e}")
                results.append({"image": str(image_path), "result": None})

            await page.close()

        # 总结
        print("\n" + "="*60)
        print("批量处理完成")
        print("="*60)
        success = sum(1 for r in results if r["result"])
        print(f"✅ 成功: {success}/{len(results)}")
        for r in results:
            status = "✅" if r["result"] else "❌"
            print(f"{status} {Path(r['image']).name}")

        return results

    async def screenshot(self, filename="picset.png"):
        """截图"""
        await self.page.screenshot(path=filename, full_page=True)
        print(f"📸 截图: {filename}")

    async def close(self):
        """关闭浏览器"""
        print("🔴 关闭浏览器...")
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        print("✅ 完成")


async def interactive_mode():
    """交互模式"""
    print("\n" + "="*60)
    print("Picset AI 自动化 - 交互模式")
    print("="*60)

    async with PicsetAIFullFlow(headless=False, slow_mo=300) as bot:
        # 打开页面
        await bot.open_studio()

        while True:
            print("\n可用命令:")
            print("  1. upload [路径]  - 上传图片")
            print("  2. mode [主图/详情图] - 选择模式")
            print("  3. style [风格] - 选择风格")
            print("  4. analyze       - 分析产品")
            print("  5. wait          - 等待生成")
            print("  6. download      - 下载结果")
            print("  7. shot          - 截图")
            print("  8. flow          - 完整流程")
            print("  9. quit          - 退出")

            cmd = input("\n输入命令: ").strip()

            if cmd == "quit":
                break
            elif cmd.startswith("upload "):
                await bot.upload_image(cmd[7:])
            elif cmd.startswith("mode "):
                await bot.select_mode(cmd[5:])
            elif cmd.startswith("style "):
                await bot.select_style(cmd[6:])
            elif cmd == "analyze":
                await bot.analyze_product()
            elif cmd == "wait":
                await bot.wait_for_generation()
            elif cmd == "download":
                await bot.download_results()
            elif cmd == "shot":
                await bot.screenshot()
            elif cmd == "flow":
                image = input("图片路径: ").strip()
                await bot.full_flow(image)


def main():
    parser = argparse.ArgumentParser(description="Picset AI 完整自动化流程")
    parser.add_argument("--image", "-i", help="单张图片路径")
    parser.add_argument("--folder", "-f", help="图片文件夹（批量处理）")
    parser.add_argument("--mode", "-m", default="主图", help="模式: 主图/详情图")
    parser.add_argument("--style", "-s", default="3:4 竖版", help="风格: 3:4 竖版/1:1 方版/16:9 横版")
    parser.add_argument("--quality", "-q", default="2K 高清", help="质量: 2K 高清/4K 超清")
    parser.add_argument("--count", "-c", default="1 张", help="数量: 1 张/4 张")
    parser.add_argument("--interactive", help="交互模式")
    parser.add_argument("--headless", action="store_true", help="无头模式")

    args = parser.parse_args()

    if args.interactive:
        asyncio.run(interactive_mode())
    elif args.folder:
        asyncio.run(PicsetAIFullFlow(headless=args.headless).batch_process(
            args.folder, args.mode, args.style, args.quality
        ))
    elif args.image:
        asyncio.run(PicsetAIFullFlow(headless=args.headless).full_flow(
            args.image, args.mode, args.style, args.quality, args.count
        ))
    else:
        parser.print_help()
        print("\n示例:")
        print("  python picset_ai_full_flow.py --image ./product.jpg")
        print("  python picset_ai_full_flow.py --folder ./images")
        print("  python picset_ai_full_flow.py --interactive")


if __name__ == "__main__":
    asyncio.run(main() if not sys.argv[1:] else main())
