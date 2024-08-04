import os
import subprocess
import re
import uuid
from loguru import logger
from art import *
import html
import shutil
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup


class MermaidSVGConverter:
    def __init__(self, css_file=None):
        logger.info("MermaidSVGConverterを初期化しています")
        self.mmdc_path = self._find_mmdc()
        self.css_file = css_file

    def _find_mmdc(self):
        mmdc_path = shutil.which('mmdc')
        if mmdc_path:
            logger.info(f"mmdcコマンドが見つかりました: {mmdc_path}")
            return mmdc_path
        else:
            logger.error("mmdcコマンドが見つかりません。PATHを確認してください。")
            return None

    def convert_html_mermaid_to_svg(self, input_html_path, output_html_path):
        print(text2art(">>    MermaidSVGConverter", "rnd-medium"))
        logger.info("Mermaid to SVG変換プロセスを開始します")
        
        if not self.mmdc_path:
            logger.error("mmdcコマンドが利用できないため、変換プロセスを中断します")
            return

        input_dir = os.path.dirname(input_html_path)
        svg_dir = os.path.join(input_dir, "svg")
        os.makedirs(svg_dir, exist_ok=True)
        logger.info(f"SVG保存用ディレクトリを作成しました: {svg_dir}")

        html_content = self._acquire_content(input_html_path)
        if html_content:
            html_content, mermaid_blocks = self._extract_mermaid_blocks(html_content)
            if mermaid_blocks:
                logger.info(f"抽出されたMermaidブロック: {len(mermaid_blocks)}")
                enhanced_html = self._convert_mermaid_to_svg(html_content, mermaid_blocks, svg_dir, input_html_path)
                self._materialize_fusion(output_html_path, enhanced_html)
                logger.success("Mermaid to SVG変換プロセスが見事に完了しました")
            else:
                self._materialize_fusion(output_html_path, html_content)
                logger.warning("Mermaidのブロックが見つからず、変換プロセスを中断します")
        else:
            logger.error("HTMLファイルの取得に失敗し、変換プロセスを中断します")

    def _acquire_content(self, file_path):
        logger.info(f"{file_path}の内容を取得します")
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            logger.success(f"{file_path}の内容取得に成功しました")
            return content
        except Exception as e:
            logger.error(f"{file_path}の取得中に障害が発生しました: {str(e)}")
            return None

    def _extract_mermaid_blocks(self, html_content):
        logger.info("HTMLからMermaidブロックを抽出します")
        pattern = r'<div class="mermaid">\s*(.*?)\s*</div>'
        mermaid_blocks = []
        
        def replace_with_placeholder(match):
            placeholder = f"__MERMAID_{len(mermaid_blocks):03d}__"
            mermaid_blocks.append(match.group(1))
            return placeholder

        modified_html = re.sub(pattern, replace_with_placeholder, html_content, flags=re.DOTALL)
        
        if mermaid_blocks:
            logger.success(f"Mermaidブロックの抽出に成功しました: {len(mermaid_blocks)}個")
        else:
            logger.warning("Mermaidブロックが見つかりませんでした")
        
        return modified_html, mermaid_blocks

    def _adjust_svg_width(self, svg_file):
        with open(svg_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'xml')

        # <g>要素を検索 (class属性に"node"を含むもの)
        for g in soup.find_all('g', class_=lambda x: x and 'node' in x.split()):
            rect = g.find('rect', class_='basic label-container')
            foreign_object = g.find('foreignObject')
            
            if rect and foreign_object:
                try:
                    # foreignObjectの幅を調整
                    fo_width = foreign_object.get('width')
                    if fo_width and fo_width != '0':
                        new_fo_width = float(fo_width) + 20
                        foreign_object['width'] = str(new_fo_width)
                        logger.debug(f"foreignObject幅調整: {fo_width} -> {new_fo_width}")

                    # rectの幅を調整
                    rect_width = rect.get('width')
                    if rect_width and rect_width != '0':
                        new_rect_width = float(rect_width) + 20
                        rect['width'] = str(new_rect_width)
                        logger.debug(f"rect幅調整: {rect_width} -> {new_rect_width}")

                    # rectのx属性を調整（中央揃えを維持するため）
                    rect_x = rect.get('x')
                    if rect_x:
                        new_rect_x = float(rect_x) - 10
                        rect['x'] = str(new_rect_x)
                        logger.debug(f"rect x位置調整: {rect_x} -> {new_rect_x}")

                    # 親のg要素の変換を調整（必要な場合）
                    transform = g.get('transform')
                    if transform:
                        match = re.search(r'translate\(([-\d.]+),\s*([-\d.]+)\)', transform)
                        if match:
                            x, y = map(float, match.groups())
                            new_x = x + 10  # X座標を10ピクセル右に移動
                            g['transform'] = f'translate({new_x}, {y})'
                            logger.debug(f"g transform調整: {x},{y} -> {new_x},{y}")

                except ValueError as e:
                    logger.error(f"幅の調整中にエラーが発生しました: {e}")
                    logger.error(f"問題のある要素: {g}")
                    # エラーが発生しても処理を続行
                    continue

        # SVG要素の調整
        svg = soup.find('svg')
        if svg:
            viewbox = svg.get('viewBox')
            if viewbox:
                x, y, width, height = map(float, viewbox.split())
                
                # viewBoxの幅を20増やす
                new_width = width + 20
                svg['viewBox'] = f"{x} {y} {new_width} {height}"
                
                # style属性を更新
                style = svg.get('style', '')
                style_dict = dict(item.split(': ') for item in style.split('; ') if item)
                style_dict['max-width'] = f'{new_width}px'
                style_dict['background-color'] = 'None'
                
                # テキストのシャープネスを向上させるための設定を追加
                style_dict['shape-rendering'] = 'crispEdges'
                style_dict['text-rendering'] = 'optimizeLegibility'
                
                svg['style'] = '; '.join(f'{k}: {v}' for k, v in style_dict.items())

        # テキスト要素のフォントサイズを調整
        for text in soup.find_all('text'):
            current_size = text.get('font-size')
            if current_size:
                # フォントサイズを少し大きくする（例: 10%増加）
                new_size = float(current_size.replace('px', '')) * 1.1
                text['font-size'] = f'{new_size}px'

        # 調整後のSVGファイル名
        adjusted_svg_file = svg_file.replace('.svg', '_adjusted.svg')
        
        # SVGを保存
        with open(adjusted_svg_file, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        return adjusted_svg_file

    def _convert_mermaid_to_svg(self, html_content, mermaid_blocks, svg_dir, input_html_path):
        logger.info("MermaidをSVGに変換します")
        current_dir = os.getcwd()
        logger.debug(f"現在の作業ディレクトリ: {current_dir}")
        
        for index, block in enumerate(mermaid_blocks):
            decoded_block = html.unescape(block)
            
            # 「-->」を「-.->」に置換
            decoded_block = decoded_block.replace('-->', '-.->')
            decoded_block = decoded_block.replace('graph TD', 'graph LR')
            
            mermaid_file = os.path.join(svg_dir, f"mermaid_{uuid.uuid4().hex}.mmd")
            svg_file = os.path.join(svg_dir, f"mermaid_{uuid.uuid4().hex}.svg")
            
            with open(mermaid_file, 'w', encoding='utf-8') as f:
                f.write(decoded_block)
                
            logger.debug(f"mermaid_file: {mermaid_file}")
            logger.debug(f"decoded block: \n{decoded_block}")
            
            cmd = [self.mmdc_path, '-i', mermaid_file, '-o', svg_file]
            
            # CSSファイルが指定されている場合、コマンドに追加
            if self.css_file:
                cmd.extend(['--cssFile', self.css_file])
            
            cmd_debug = " ".join(cmd)
            logger.debug(f"mermaid-cliを実行します: {cmd_debug}")
            try:
                result = subprocess.run(cmd, check=True, capture_output=True, text=True, cwd=current_dir)
                logger.debug(f"mermaid-cli output: {result.stdout}")
                logger.debug(f"mermaid-cli error: {result.stderr}")
            except subprocess.CalledProcessError as e:
                logger.error(f"mermaid-cliの実行中にエラーが発生しました: {str(e)}")
                logger.error(f"mermaid-cli error output: {e.stderr}")
                continue
            
            # SVGファイルの幅を調整
            adjusted_svg_file = self._adjust_svg_width(svg_file)
            relative_svg_path = os.path.relpath(adjusted_svg_file, os.path.dirname(input_html_path)).replace('\\', '/')
            
            # <object>タグと<img>タグの両方を生成
            object_tag = f'<object type="image/svg+xml" data="{relative_svg_path}" style="width: 100%; height: auto;">SVGがサポートされていません</object>'
            img_tag = f'<img src="{relative_svg_path}" alt="Mermaid diagram" style="width: 100%; height: auto;">'
            
            # combined_tags = f'<div class="mermaid-svg-container">{object_tag}{img_tag}</div>'
            combined_tags = f'<div class="mermaid-svg-container">{img_tag}</div>'
            
            placeholder = f"__MERMAID_{index:03d}__"
            html_content = html_content.replace(placeholder, combined_tags)
            
            logger.success(f"Mermaid図 {index + 1} をSVGに変換しました: {os.path.basename(svg_file)}")

        return html_content

    def _materialize_fusion(self, file_path, content):
        logger.info(f"変換結果を{file_path}に具現化します")
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            logger.success(f"変換結果の具現化が完了しました: {file_path}")
        except Exception as e:
            logger.error(f"変換結果の具現化中に障害が発生しました: {str(e)}")

def main():
    logger.info("Mermaid to SVG変換の儀式を開始します")
    css_file = 'css/svg_oasis.css'  # CSSファイルのパスを指定
    svg_converter = MermaidSVGConverter(css_file=css_file)
    svg_converter.convert_html_mermaid_to_svg(
        'example2/hovercraft_assets/enchant_codeblock.html',
        'example2/hovercraft_assets/index_with_svg.html'
    )

if __name__ == "__main__":
    main()
