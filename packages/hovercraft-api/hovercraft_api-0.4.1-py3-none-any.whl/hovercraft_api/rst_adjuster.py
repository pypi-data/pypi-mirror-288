import re
from loguru import logger
from art import *

class RSTAdjuster:
    def __init__(self, css_file='css/mytheme.css'):
        self.css_file = css_file
        logger.info("RSTAdjuster initialized")

    def read_file(self, file_path):
        """指定されたファイルを読み込み、その内容を返す"""
        logger.info(f"ファイル '{file_path}' を読み込んでいます")
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            logger.success(f"ファイルの読み込みが完了しました: {file_path}")
            return content
        except IOError as e:
            logger.error(f"ファイルの読み込み中にエラーが発生しました: {str(e)}")
            raise

    def save_file(self, content, output_file):
        """指定された内容をファイルに保存する"""
        logger.info(f"ファイルを '{output_file}' に保存しています")
        try:
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(content)
            logger.success(f"ファイルの保存が完了しました: {output_file}")
        except IOError as e:
            logger.error(f"ファイルの保存中にエラーが発生しました: {str(e)}")
            raise

    def adjust_for_hovercraft(self, rst_file, hovercraft_rst_file):
        """RSTファイルをHovercraft用に調整する"""
        print(text2art(">>    RSTAdjuster","rnd-medium"))
        logger.info(f"RSTファイル '{rst_file}' をHovercraft用に調整しています")
        content = self.read_file(rst_file)
        slides = re.split(r'\n--------------\n+', content)

        new_content = [
            ":title: Your Presentation Title",
            ":data-transition-duration: 1000",
            f":css: {self.css_file}",
            ""
        ]

        for i, slide in enumerate(slides):
            new_slide = f".. class:: step\n\n   :data-x: {i * 1000}\n   :data-y: 0\n\n{slide.strip()}\n\n"
            new_content.append(new_slide)

        self.save_file('\n'.join(new_content), hovercraft_rst_file)
        logger.success(f"Hovercraft用のRSTファイルを作成しました: {hovercraft_rst_file}")

if __name__ == "__main__":
    import os

    # テスト用のRSTファイルを作成
    test_rst = r"example\hovercraft_assets\test_output.rst"
    adjuster = RSTAdjuster()
    output_rst = r"example\hovercraft_assets\test_output_hovercraft.rst"
    
    try:
        adjuster.adjust_for_hovercraft(test_rst, output_rst)
        print(f"調整されたRSTファイルの内容:")
        with open(output_rst, "r") as f:
            print(f.read())
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")

