import re
import random
from loguru import logger
from art import *

class DynamicRSTAdjuster:
    def __init__(self, grid_width=6000, grid_height=6000, grid_depth=3000, slide_width=1000, slide_height=750, slide_depth=1000, css_file='css/mytheme.css', enable_dynamic_position=True, use_rotate_x=False, use_rotate_y=False, use_rotate_z=False):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.grid_depth = grid_depth
        self.slide_width = slide_width
        self.slide_height = slide_height
        self.slide_depth = slide_depth
        self.css_file = css_file
        self.enable_dynamic_position = enable_dynamic_position
        self.use_rotate_x = use_rotate_x
        self.use_rotate_y = use_rotate_y
        self.use_rotate_z = use_rotate_z
        self.grid_points = self.generate_grid_points() if self.enable_dynamic_position else []
        self.used_points = set()
        logger.info(f"DynamicRSTAdjuster initialized with {'3D' if self.enable_dynamic_position else '2D'} grid, dynamic positioning {'enabled' if self.enable_dynamic_position else 'disabled'}")

    def generate_grid_points(self):
        points = []
        for x in range(0, self.grid_width, self.slide_width):
            for y in range(0, self.grid_height, self.slide_height):
                for z in range(-self.grid_depth, self.grid_depth + 1, self.slide_depth):
                    points.append((x, y, z))
        random.shuffle(points)
        logger.info(f"Generated {len(points)} grid points")
        return points

    def get_random_position(self):
        if not self.grid_points:
            logger.warning("All grid points have been used. Resetting grid.")
            self.grid_points = list(set(self.generate_grid_points()) - self.used_points)
            if not self.grid_points:
                logger.error("No available grid points even after reset.")
                return None, None, None

        point = self.grid_points.pop()
        self.used_points.add(point)
        logger.debug(f"Selected grid point: {point}")
        return point

    def get_random_rotation(self):
        return random.randint(0, 360)

    def read_file(self, file_path):
        logger.info(f"ファイル '{file_path}' を読み込んでいます")
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            logger.success(f"ファイルの読み込みが完了しました: {file_path}")
            logger.debug(f"ファイルの内容:\n{content[:100]}")
            return content
        except IOError as e:
            logger.error(f"ファイルの読み込み中にエラーが発生しました: {str(e)}")
            raise

    def save_file(self, content, output_file):
        logger.info(f"ファイルを '{output_file}' に保存しています")
        try:
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(content)
            logger.success(f"ファイルの保存が完了しました: {output_file}")
            logger.debug(f"保存された内容:\n{content[:100]}")
        except IOError as e:
            logger.error(f"ファイルの保存中にエラーが発生しました: {str(e)}")
            raise

    def parse_rst_content(self, content):
        logger.info("RSTコンテンツの解析を開始します")
        slides = re.split(r'\n.. class:: step\n', content)
        header = slides.pop(0)
        logger.debug(f"解析されたヘッダー:\n{header}")
        logger.info(f"{len(slides)}個のスライドが見つかりました")
        for i, slide in enumerate(slides, 1):
            logger.debug(f"スライド {i}:\n{slide}\n{'='*40}")
        return header, slides


    def adjust_slide_coordinates(self, slide, slide_index):
        logger.info("スライドの座標を調整します")

        if self.enable_dynamic_position:
            x, y, z = self.get_random_position()
            if x is None:
                logger.error("Failed to get a valid position. Skipping slide adjustment.")
                return slide
        else:
            x = slide_index * self.slide_width
            y = 0
            z = 0

        new_attributes = [
            f":data-x: {x}",
            f":data-y: {y}",
            f":data-z: {z}"
        ]

        if self.use_rotate_x:
            new_attributes.append(f":data-rotate-x: {self.get_random_rotation()}")
        if self.use_rotate_y:
            new_attributes.append(f":data-rotate-y: {self.get_random_rotation()}")
        if self.use_rotate_z:
            new_attributes.append(f":data-rotate: {self.get_random_rotation()}")

        # スライドを行に分割し、既存の属性を削除
        lines = slide.strip().split('\n')
        content_lines = [line for line in lines if not line.strip().startswith(':data-')]

        # 新しいスライド内容を構築
        new_slide = ["----", ""] + new_attributes + [""] + content_lines

        adjusted_slide = '\n'.join(new_slide)
        logger.debug(f"調整後のスライド:\n{adjusted_slide}")
        return adjusted_slide

    def adjust_for_dynamic_hovercraft(self, rst_file, output_file):
        logger.info(f"RSTファイル '{rst_file}' をダイナミックなHovercraft用に調整しています")
        content = self.read_file(rst_file)
        
        header, slides = self.parse_rst_content(content)

        new_content = [header.strip()]

        for i, slide in enumerate(slides):
            adjusted_slide = self.adjust_slide_coordinates(slide, i)
            new_content.append(adjusted_slide)
            logger.info(f"スライド {i+1} が調整されました")

        final_content = '\n\n'.join(new_content)
        logger.debug(f"最終的な内容:\n{final_content[:500]}")
        self.save_file(final_content, output_file)
        logger.success(f"ダイナミックなHovercraft用のRSTファイルを作成しました: {output_file}")
        
# メインの実行部分
if __name__ == "__main__":
    import os
    import sys

    # loguruのログレベルを設定
    logger.remove()
    logger.add(sys.stderr, level="DEBUG")

    # テスト用のRSTファイルのパス
    test_rst = r"example\hovercraft_assets\test_output_hovercraft.rst"
    output_rst = r"example\hovercraft_assets\test_output_dynamic_hovercraft.rst"
    
    adjuster = DynamicRSTAdjuster()
    
    try:
        # 回転オプションを有効にしてテスト
        adjuster.adjust_for_dynamic_hovercraft(test_rst, output_rst)
        print(f"調整されたダイナミックRSTファイルの内容:")
        with open(output_rst, "r") as f:
            print(f.read())
    except Exception as e:
        logger.exception(f"エラーが発生しました: {str(e)}")
