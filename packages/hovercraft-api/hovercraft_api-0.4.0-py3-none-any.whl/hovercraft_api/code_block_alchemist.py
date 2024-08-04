import re
from loguru import logger
from art import *

class CodeBlockTransmuter:
    def __init__(self):
        logger.info("CodeBlockTransmuterを起動します")

    def transmute_documents(self, html_path, md_path, output_path):
        print(text2art(">>   CodeBlockTransmuter","rnd-medium"))
        logger.info("コードブロック変換プロセスを開始します")
        html_content = self._summon_content(html_path)
        md_content = self._summon_content(md_path)

        if html_content and md_content:
            code_essences = self._extract_code_essences(md_content)
            if code_essences:
                transmuted_html = self._infuse_code_blocks(html_content, code_essences)
                transmuted_html = self._add_highlight_js(transmuted_html)
                self._manifest_transmutation(output_path, transmuted_html)
                logger.success("コードブロック変換プロセスが見事に完了しました")
            else:
                logger.warning("変換すべき非Mermaidコードブロックが見つかりませんでした")
                self._manifest_transmutation(output_path, html_content)
        else:
            logger.error("必要な素材の召喚に失敗し、変換プロセスを中断します")

    def _summon_content(self, file_path):
        logger.info(f"{file_path}の内容を召喚します")
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            logger.success(f"{file_path}の内容召喚に成功しました")
            return content
        except Exception as e:
            logger.error(f"{file_path}の召喚中に障害が発生しました: {str(e)}")
            return None

    def _extract_code_essences(self, md_content):
        logger.info("非Mermaidコードブロックのエッセンスを抽出します")
        pattern = r'```(\w+)\n(.*?)```'
        matches = re.findall(pattern, md_content, re.DOTALL)
        code_essences = [(lang, code.strip()) for lang, code in matches if lang.lower() != 'mermaid']
        if code_essences:
            logger.success(f"{len(code_essences)}個の非Mermaidコードブロックのエッセンス抽出に成功しました")
        else:
            logger.warning("非Mermaidコードブロックのエッセンスが見つかりませんでした")
        return code_essences

    def _infuse_code_blocks(self, html_content, code_essences):
        logger.info("HTMLに非Mermaidコードブロックを注入します")
        for lang, code in code_essences:
            pattern = r'<p>Content block expected for the "code" directive; none found.</p>.*?</dl>'
            infusion = f'''<pre><code class="language-{lang}">
{code}
</code></pre>'''
            html_content = re.sub(pattern, infusion, html_content, count=1, flags=re.DOTALL)
        logger.success("非Mermaidコードブロックの注入が完了しました")
        return html_content

    def _add_highlight_js(self, html_content):
        logger.info("HTMLにhighlight.jsのリンクを追加します")
        highlight_js_links = '''
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/default.min.css">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/highlight.min.js"></script>
  <script>hljs.highlightAll();</script>
'''
        head_end_tag = '</head>'
        html_content = html_content.replace(head_end_tag, f'{highlight_js_links}\n{head_end_tag}')
        logger.success("highlight.jsのリンク追加が完了しました")
        return html_content

    def _manifest_transmutation(self, file_path, content):
        logger.info(f"変換結果を{file_path}に具現化します")
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            logger.success(f"変換結果の具現化が完了しました: {file_path}")
        except Exception as e:
            logger.error(f"変換結果の具現化中に障害が発生しました: {str(e)}")

def main():
    logger.info("コードブロック変換の儀式を開始します")
    transmuter = CodeBlockTransmuter()
    transmuter.transmute_documents(
        'example/hovercraft_assets/index2.html',
        'example/hovercraft_assets/test_output_slides.md',
        'example/hovercraft_assets/index3.html'
    )

if __name__ == "__main__":
    main()
