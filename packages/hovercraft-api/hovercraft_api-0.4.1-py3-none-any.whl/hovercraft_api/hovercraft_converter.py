import subprocess
from loguru import logger
import os
from art import *
import shutil

class HovercraftConverter:
    def __init__(self, output_dir='output', css_file='css/mytheme.css'):
        self.output_dir = output_dir
        self.css_file = css_file
        os.makedirs(self.output_dir, exist_ok=True)
        logger.info("HovercraftConverter initialized")

    def convert(self, rst_file):
        print(text2art(">>   HovercraftConverter","rnd-medium"))
        """RSTファイルをHovercraftスライドに変換する"""
        logger.info(f"RSTファイル '{rst_file}' をHovercraftスライドに変換しています")
        try:
            command = ['hovercraft', rst_file, self.output_dir]
            if self.css_file:
                command.extend(['-c', self.css_file])

            logger.debug(f"Hovercraftのコマンド: \n{' '.join(command)}")
            subprocess.run(command, check=True)

            index_file = os.path.join(self.output_dir, 'index.html')
            if os.path.exists(index_file):
                logger.success(f"HTMLスライドの生成が完了しました: {index_file}")
                return True
            else:
                logger.error(f"HTMLファイルが生成されませんでした: {index_file}")
                return False

        except subprocess.CalledProcessError as e:
            logger.error(f"Hovercraftの実行中にエラーが発生しました: {str(e)}")
            return False

if __name__ == "__main__":
    # テスト用のRSTファイルを作成
    test_rst = r"example\hovercraft_assets\test_output_dynamic_hovercraft.rst"
    converter = HovercraftConverter(
        output_dir=r'example\hovercraft_assets',
    )
    
    try:
        success = converter.convert(test_rst)
        if success:
            print(f"Hovercraftスライドが正常に生成されました。出力ディレクトリ: {converter.output_dir}")
        else:
            print("Hovercraftスライドの生成中にエラーが発生しました。")
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
