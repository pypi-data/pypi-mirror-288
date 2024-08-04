import subprocess
from loguru import logger
from art import *

class MarkdownToRSTConverter:
    def __init__(self):
        logger.info("MarkdownToRSTConverter initialized")

    def convert(self, input_file, output_file):
        """MarkdownをRSTに変換する"""
        print(text2art(">>   MarkdownToRSTConverter","rnd-medium"))
        logger.info(f"Markdownを '{input_file}' からRST '{output_file}' に変換しています")
        try:
            cmd = ['pandoc', '-f', 'markdown', '-t', 'rst', '-o', output_file, input_file]
            cmd_debug = " ".join(cmd)
            logger.debug(f"pandocコマンド: \n{cmd_debug}")
            subprocess.run(cmd, check=True)
            logger.success(f"Markdownを正常にRSTに変換しました: {output_file}")
        except subprocess.CalledProcessError as e:
            logger.error(f"pandocの実行中にエラーが発生しました: {str(e)}")
            raise

if __name__ == "__main__":
    import os

    # テスト用のマークダウンファイルを作成
    test_md = "example/hovercraft_assets/test_output_slides.md"
    converter = MarkdownToRSTConverter()
    output_rst = "example/hovercraft_assets/test_output.rst"
    
    try:
        converter.convert(test_md, output_rst)
        print(f"変換されたRSTファイルの内容:")
        with open(output_rst, "r", encoding="utf8") as f:
            print(f.read())
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")

