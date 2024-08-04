import os
from loguru import logger
import shutil
import argparse
from typing import List
from dotenv import load_dotenv

from .markdown_to_rst_converter import MarkdownToRSTConverter
from .rst_adjuster import RSTAdjuster
from .hovercraft_converter import HovercraftConverter
from .mermaid_alchemist import MermaidFusionMaster
from .code_block_alchemist import CodeBlockTransmuter
from .markdown_to_slides_converter import MarkdownToSlidesConverter
from .dynamic_rst_adjuster import DynamicRSTAdjuster
from .mermaid_svg_converter import MermaidSVGConverter
from .slide_capturer import SlideCapturer
from art import *

class HovercraftAPI:
    def __init__(self, markdown_file: str, css_file: str = 'css/mytheme.css', 
                 svg_css_file: str = 'css/svg_oasis.css',
                 js_file: str = 'js/mermaid.min.js', model_name: str = "gemini/gemini-1.5-pro-latest",
                 grid_width: int = 6000, grid_height: int = 6000, grid_depth: int = 6000,
                 slide_width: int = 1000, slide_height: int = 750, slide_depth: int = 1000,
                 enable_dynamic_position: bool = False,
                 use_rotate_x: bool = False, use_rotate_y: bool = False, use_rotate_z: bool = False,
                 capture_images: bool = False, capture_video: bool = False,
                 capture_fps: int = 30, capture_duration: int = 5,
                 html_file: str = 'index_with_svg.html',
                 stages: List[str] = ['all']):

        # Load environment variables from .env file
        self.working_dir = os.getcwd()
        dotenv_path = os.path.join(self.working_dir, '.env')
        load_dotenv(dotenv_path)
        
        # 入力ファイルと設定
        self.markdown_file = markdown_file  # 入力Markdownファイルのパス
        self.css_file = css_file  # 使用するCSSファイルのパス
        self.svg_css_file = svg_css_file
        self.js_file = js_file  # 使用するJavaScriptファイルのパス
        self.model_name = model_name  # 使用するLLMモデルの名前

        # グリッドとスライドの寸法設定
        self.grid_width = grid_width  # グリッドの幅（ピクセル）
        self.grid_height = grid_height  # グリッドの高さ（ピクセル）
        self.grid_depth = grid_depth  # グリッドの奥行き（ピクセル）
        self.slide_width = slide_width  # 各スライドの幅（ピクセル）
        self.slide_height = slide_height  # 各スライドの高さ（ピクセル）
        self.slide_depth = slide_depth  # 各スライドの奥行き（ピクセル）

        # 動的位置調整の設定
        self.enable_dynamic_position = enable_dynamic_position  # 動的位置調整を有効にするかどうか
        self.use_rotate_x = use_rotate_x  # X軸回転を使用するかどうか
        self.use_rotate_y = use_rotate_y  # Y軸回転を使用するかどうか
        self.use_rotate_z = use_rotate_z  # Z軸回転を使用するかどうか

        # スライドキャプチャの設定
        self.capture_images = capture_images  # スライドを画像としてキャプチャするかどうか
        self.capture_video = capture_video  # スライドを動画としてキャプチャするかどうか
        self.capture_fps = capture_fps  # 動画キャプチャ時のフレームレート
        self.capture_duration = capture_duration  # 各スライドのキャプチャ時間（秒）
        self.html_file = html_file  # 生成されるHTMLファイルの名前

        # 実行するステージの設定
        self.stages = stages  # 実行するステージのリスト

        # ファイルパスとディレクトリの設定
        self.working_dir = os.getcwd()  # 現在の作業ディレクトリ
        self.markdown_dir = os.path.dirname(self.markdown_file)  # Markdownファイルのディレクトリ
        self.assets_dir = os.path.join(self.markdown_dir, 'hovercraft_assets')  # アセットディレクトリのパス
        self.slides_md_file = os.path.join(self.assets_dir, 'slides.md')  # 生成されるスライドMarkdownファイルのパス
        self.rst_file = os.path.join(self.assets_dir, 'temp.rst')  # 一時的なRSTファイルのパス
        self.hovercraft_rst_file = os.path.join(self.assets_dir, 'temp_hovercraft.rst')  # Hovercraft用RSTファイルのパス
        self.html_file = os.path.join(self.assets_dir, 'index.html')  # 生成されるHTMLファイルのパス
        self.mermaid_html_file = os.path.join(self.assets_dir, 'enchant_mermaid.html')  # Mermaid図を含むHTMLファイルのパス
        self.codeblock_html_file = os.path.join(self.assets_dir, 'enchant_codeblock.html')  # コードブロックを含むHTMLファイルのパス
        self.svg_html_file = os.path.join(self.assets_dir, 'index_with_svg.html')  # SVGを含む最終的なHTMLファイルのパス

        # CSSパスの設定
        self.css_src = os.path.join(self.working_dir, self.css_file)  # ソースCSSファイルのパス
        self.css_dest = os.path.join(self.assets_dir, self.css_file)  # コピー先CSSファイルのパス
        
        # JavaScript file path setup
        self.js_file = js_file
        self.js_src = os.path.join(self.working_dir, self.js_file)
        self.js_dest = os.path.join(self.assets_dir, self.js_file)

        # コンバーターとアジャスターの初期化
        self.md_to_rst_converter = MarkdownToRSTConverter()  # MarkdownからRSTへのコンバーター
        self.rst_adjuster = RSTAdjuster(css_file=self.css_file)  # RSTアジャスター
        self.hovercraft_converter = HovercraftConverter(output_dir=self.assets_dir, css_file=self.css_file)  # Hovercraftコンバーター
        self.mermaid_fusion_master = MermaidFusionMaster()  # Mermaid図の統合ツール
        self.codeblock_transmuter = CodeBlockTransmuter()  # コードブロック変換ツール
        self.md_to_slides_converter = MarkdownToSlidesConverter(model_name=self.model_name)  # Markdownからスライドへのコンバーター
        self.mermaid_svg_converter = MermaidSVGConverter(css_file=self.svg_css_file)  # MermaidからSVGへのコンバーター

        # 動的RSTアジャスターの設定
        self.dynamic_rst_adjuster = DynamicRSTAdjuster(
            grid_width=self.grid_width,
            grid_height=self.grid_height,
            grid_depth=self.grid_depth,
            slide_width=self.slide_width,
            slide_height=self.slide_height,
            slide_depth=self.slide_depth,
            css_file=self.css_file,
            use_rotate_x=self.use_rotate_x,
            use_rotate_y=self.use_rotate_y,
            use_rotate_z=self.use_rotate_z
        )  # 動的RSTアジャスター

        # スライドキャプチャーの設定
        self.slide_capturer = SlideCapturer(self.assets_dir, html_file=self.html_file)  # スライドキャプチャツール

        # 'all'ステージがある場合、すべてのステージを展開
        if 'all' in self.stages:
            self.stages = ['md_to_slides', 'md_to_rst', 'rst_to_hovercraft', 'hovercraft_to_html', 
                           'mermaid_fusion', 'codeblock_transmute', 'mermaid_to_svg', 'capture_slides']

        # アセットディレクトリの初期化
        os.makedirs(self.assets_dir, exist_ok=True)
        self._copy_assets()
        
        logger.info("HovercraftAPIが初期化されました")

    def _copy_assets(self):
        # CSS file copy
        if os.path.exists(self.css_src):
            os.makedirs(os.path.dirname(self.css_dest), exist_ok=True)
            shutil.copy2(self.css_src, self.css_dest)
            logger.info(f"CSSファイルをコピーしました: {self.css_src} から {self.css_dest}")
        else:
            logger.warning(f"CSSファイルが見つかりません: {self.css_src}")

        # JavaScript file copy
        if os.path.exists(self.js_src):
            os.makedirs(os.path.dirname(self.js_dest), exist_ok=True)
            shutil.copy2(self.js_src, self.js_dest)
            logger.info(f"JavaScriptファイルをコピーしました: {self.js_src} から {self.js_dest}")
        else:
            logger.warning(f"JavaScriptファイルが見つかりません: {self.js_src}")


    def generate_slides(self):
        try:
            if 'md_to_slides' in self.stages:
                self.md_to_slides_converter.convert_file(self.markdown_file, self.slides_md_file)
                logger.info("Markdownをスライド用Markdownに変換しました")

            if 'md_to_rst' in self.stages:
                self.md_to_rst_converter.convert(self.slides_md_file, self.rst_file)
                logger.info("MarkdownをRSTに変換しました")

            if 'rst_to_hovercraft' in self.stages:
                self.rst_adjuster.adjust_for_hovercraft(self.rst_file, self.hovercraft_rst_file)
                logger.info("RSTをHovercraft用に調整しました")

                if self.enable_dynamic_position:
                    dynamic_hovercraft_rst_file = os.path.join(self.assets_dir, 'temp_dynamic_hovercraft.rst')  
                    self.dynamic_rst_adjuster.adjust_for_dynamic_hovercraft(self.hovercraft_rst_file, dynamic_hovercraft_rst_file)
                    self.hovercraft_rst_file = dynamic_hovercraft_rst_file 
                    logger.info("動的な位置調整を適用しました")

            if 'hovercraft_to_html' in self.stages:
                self.hovercraft_converter.convert(self.hovercraft_rst_file)
                logger.info("HovercraftでHTMLを生成しました")

            if 'mermaid_fusion' in self.stages:
                self.mermaid_fusion_master.orchestrate_fusion(self.html_file, self.mermaid_html_file)
                logger.info("Mermaid図を統合しました")

            if 'codeblock_transmute' in self.stages:
                self.codeblock_transmuter.transmute_documents(self.mermaid_html_file, self.slides_md_file, self.codeblock_html_file)
                logger.info("コードブロックを変換しました")

            if 'mermaid_to_svg' in self.stages:
                self.mermaid_svg_converter.convert_html_mermaid_to_svg(self.codeblock_html_file, self.svg_html_file)
                logger.info("MermaidをSVGに変換しました")

            logger.success(f"Hovercraftスライド生成が完了しました: {self.svg_html_file}")

            if 'capture_slides' in self.stages:
                self.capture_slides()

            return True

        except Exception as e:
            logger.error(f"スライド生成中にエラーが発生しました: {str(e)}")
            return False

    def capture_slides(self):
        # スライドを画像としてキャプチャ
        if self.capture_images:
            self.slide_capturer.capture_slides_as_png()
            logger.info("スライドを画像としてキャプチャしました")

        # スライドを動画としてキャプチャ
        if self.capture_video:
            self.slide_capturer.capture_slides_as_video(fps=self.capture_fps, duration=self.capture_duration)
            self.slide_capturer.create_video_from_images(self.assets_dir, os.path.join(self.assets_dir, 'slides_video.mp4'), fps=self.capture_fps)
            logger.info("スライドをキャプチャして動画を作成しました")

def hovercraft_parser(parser):
    parser.add_argument("markdown_file", help="入力Markdownファイル")
    parser.add_argument("-c", "--css", default="css/mytheme.css", help="CSSファイル（作業ディレクトリからの相対パス）")
    parser.add_argument("--svg-css-file", default="css/svg_oasis.css", help="CSSファイル（作業ディレクトリからの相対パス）")
    parser.add_argument("--js-file", default="js/impress.js", help="JavaScriptファイル（作業ディレクトリからの相対パス）")
    parser.add_argument("--model-name", default="gemini/gemini-1.5-pro-latest", help="使用するLLMモデル名")

    # グリッドとスライドのサイズ設定
    parser.add_argument("--grid-width", type=int, default=6000, help="グリッドの幅")
    parser.add_argument("--grid-height", type=int, default=6000, help="グリッドの高さ")
    parser.add_argument("--grid-depth", type=int, default=6000, help="グリッドの奥行き")
    parser.add_argument("--slide-width", type=int, default=1000, help="スライドの幅")
    parser.add_argument("--slide-height", type=int, default=750, help="スライドの高さ")
    parser.add_argument("--slide-depth", type=int, default=1000, help="スライドの奥行き")

    # 動的位置調整のオプション
    parser.add_argument("--enable-dynamic-position", action="store_true", help="動的なスライド位置を有効にする")
    parser.add_argument("--use-rotate-x", action="store_true", help="X軸回転を有効にする")
    parser.add_argument("--use-rotate-y", action="store_true", help="Y軸回転を有効にする")
    parser.add_argument("--use-rotate-z", action="store_true", help="Z軸回転を有効にする")

    # スライドキャプチャのオプション
    parser.add_argument("--capture-images", action="store_true", help="スライドを画像としてキャプチャする")
    parser.add_argument("--capture-video", action="store_true", help="スライドを動画としてキャプチャする")
    parser.add_argument("--capture-fps", type=int, default=30, help="動画キャプチャ時のフレームレート")
    parser.add_argument("--capture-duration", type=int, default=5, help="動画キャプチャ時の各スライドのキャプチャ時間（秒）")
    parser.add_argument("--html-file", default="index_with_svg.html", help="キャプチャするHTMLファイル名")
    
    # 実行ステージの選択
    parser.add_argument("--stages", nargs='+', default=['all'], 
                        choices=['all', 'md_to_slides', 'md_to_rst', 'rst_to_hovercraft', 
                                 'hovercraft_to_html', 'mermaid_fusion', 'codeblock_transmute', 
                                 'mermaid_to_svg', 'capture_slides'],
                        help="実行するステージを選択（複数選択可能）")

    return parser


def cli():
    print(tprint("  HovercraftAPI",font="rnd-large"))
    parser = argparse.ArgumentParser(
        description="MarkdownからHovercraftスライドを生成します", 
        prog='hovercraftapi'
    )
    parser = hovercraft_parser(parser)
    args = parser.parse_args()

    api = HovercraftAPI(
        args.markdown_file, 
        css_file=args.css,
        svg_css_file=args.svg_css_file,
        grid_width=args.grid_width,
        grid_height=args.grid_height,
        grid_depth=args.grid_depth,
        slide_width=args.slide_width,
        slide_height=args.slide_height,
        slide_depth=args.slide_depth,
        enable_dynamic_position=args.enable_dynamic_position,
        use_rotate_x=args.use_rotate_x,
        use_rotate_y=args.use_rotate_y,
        use_rotate_z=args.use_rotate_z,
        capture_images=args.capture_images,
        capture_video=args.capture_video,
        capture_fps=args.capture_fps,
        capture_duration=args.capture_duration,
        stages=args.stages,
        html_file=args.html_file
    )
    api.generate_slides()

if __name__ == "__main__":
    cli()
