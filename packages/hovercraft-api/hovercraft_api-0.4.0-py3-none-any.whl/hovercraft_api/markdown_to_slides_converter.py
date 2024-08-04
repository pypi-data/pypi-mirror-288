from loguru import logger
from litellm import completion
from art import *

class MarkdownToSlidesConverter:
    def __init__(self, model_name="gemini/gemini-1.5-pro-latest"):
        logger.info("MarkdownToSlidesConverter initialized")
        self.model_name = model_name

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

    def convert_to_slides(self, markdown_text):
        """マークダウンをスライド形式に変換する"""
        logger.info("マークダウンをスライド形式に変換しています")
        prompt = f"""
以下のマークダウンをスライド形式のマークダウンに変換してください。
変換の際は、次のルールに従ってください：

1. タイトルは# (h1)で表現してください。
2. 章見出しは## (h2)のみを使用してください。
3. 箇条書きを駆使してスライドの内容を構成してください。
5. コンテンツは簡潔に、1スライドあたり3-5項目程度にまとめてください。
6. 図などがある場合は簡潔な1行程度のスライド＋図になるようにして
7. 長いソースコードがある場合は簡潔に要約して重要な個所だけを表示するようにして

変換するマークダウンの内容：

{markdown_text}
        """

        try:
            response = completion(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}]
            )
            slides_content = response.choices[0].message.content
            
            # 指定された置換を適用
            slides_content = slides_content.replace('\n## ', '\n---\n\n## ')

            logger.success("スライド形式への変換が完了しました")
            return slides_content
        except Exception as e:
            logger.error(f"スライド変換中にエラーが発生しました: {str(e)}")
            raise

    def convert_file(self, input_file, output_file):
        """入力ファイルを読み込み、変換し、出力ファイルに保存する"""
        print(text2art(">>    MarkdownToSlidesConverter","rnd-medium"))
        try:
            markdown_content = self.read_file(input_file)
            slides_content = self.convert_to_slides(markdown_content)
            self.save_file(slides_content, output_file)
            logger.success(f"ファイルの変換が完了しました: {input_file} -> {output_file}")
        except Exception as e:
            logger.error(f"ファイルの変換中にエラーが発生しました: {str(e)}")
            raise

if __name__ == "__main__":
    import os

    # テスト用のマークダウンファイルを作成
    test_md = "example/README.md"
    converter = MarkdownToSlidesConverter()
    output_md = "example/hovercraft_assets/test_output_slides.md"
    
    try:
        converter.convert_file(test_md, output_md)
        print(f"変換されたスライド形式のマークダウンファイルの内容:")
        with open(output_md, "r", encoding="utf8") as f:
            print(f.read())
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")

