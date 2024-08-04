import re
from loguru import logger
from art import *
from pprint import pformat

class MermaidFusionMaster:
    def __init__(self):
        logger.info("MermaidFusionMasterを初期化しています")

    def orchestrate_fusion(self, html_path, output_path):
        print(text2art(">>    MermaidFusionMaster","rnd-medium"))
        logger.info("Mermaid統合プロセスを開始します")
        html_content = self._acquire_content(html_path)

        if html_content:
            mermaid_essences = self._extract_mermaid_essences(html_content)
            if mermaid_essences:
                logger.info(f"抽出されたMermaidブロック: {len(mermaid_essences)}")
                logger.debug(f"Mermaidブロックの内容:\n{pformat(mermaid_essences)}")
                enhanced_html = self._infuse_mermaid_contents(html_content, mermaid_essences)
                enhanced_html = self._empower_with_mermaid_scripts(enhanced_html)
                self._materialize_fusion(output_path, enhanced_html)
                logger.success("Mermaid統合プロセスが見事に完了しました")
            else:
                logger.warning("Mermaidのエッセンスが見つからず、融合プロセスを中断します")
                self._materialize_fusion(output_path, html_content)
        else:
            logger.error("必要な素材の取得に失敗し、融合プロセスを中断します")

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

    def _materialize_fusion(self, file_path, content):
        logger.info(f"融合結果を{file_path}に具現化します")
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            logger.success(f"融合結果の具現化が完了しました: {file_path}")
        except Exception as e:
            logger.error(f"融合結果の具現化中に障害が発生しました: {str(e)}")

    def _extract_mermaid_essences(self, html_content):
        logger.info("Mermaidのエッセンスを抽出します")
        pattern = r'<pre class="highlight ">\.\. code:: mermaid\s*(.*?)</pre>'
        mermaid_matches = re.findall(pattern, html_content, re.DOTALL)
        if mermaid_matches:
            logger.success(f"Mermaidのエッセンス抽出に成功しました: {len(mermaid_matches)}個")
            return [match.strip() for match in mermaid_matches]
        else:
            logger.warning("Mermaidのエッセンスが見つかりませんでした")
            return []

    def _infuse_mermaid_contents(self, html_content, mermaid_essences):
        logger.info("HTMLにMermaidのエッセンスを注入します")
        pattern = r'<p>Cannot.*?</p>\s*<pre class="highlight ">.. code:: mermaid\s*(.*?)</pre>'
        
        for essence in mermaid_essences:
            match = re.search(pattern, html_content, re.DOTALL)
            if match:
                original_content = match.group(0)
                logger.debug(f"マッチした原文:\n{original_content}")
                
                replacement = f'''\n<div class="mermaid">
{essence}
</div>'''
                
                html_content = html_content.replace(original_content, replacement, 1)
                logger.success("Mermaidコードの置換が完了しました")
            else:
                logger.warning("対応するMermaidブロックが見つかりませんでした")
        
        return html_content

    def _empower_with_mermaid_scripts(self, html_content):
        logger.info("HTMLをMermaidの力で強化します")
        mermaid_enchantment = '''
<script src="https://unpkg.com/mermaid/dist/mermaid.min.js"></script>
<script>
  document.addEventListener('DOMContentLoaded', (event) => {
    mermaid.initialize({
        startOnLoad: true,
        theme: 'default'
    });
    
    function renderMermaid() {
      const mermaidDivs = document.querySelectorAll('.mermaid');
      mermaidDivs.forEach((div) => {
        if (div.offsetHeight === 0) {
          mermaid.init(undefined, div);
        }
      });
    }

    // 初回レンダリング
    renderMermaid();

    // 1秒ごとにレンダリングを試みる
    setInterval(renderMermaid, 1000);
  });
</script>
'''
        head_end = html_content.find('</head>')
        if head_end != -1:
            empowered_html = html_content[:head_end] + mermaid_enchantment + html_content[head_end:]
            logger.success("Mermaidの力による強化が完了しました")
            return empowered_html
        else:
            logger.error("HTMLの頭部が見つからず、強化に失敗しました")
            return html_content

def main():
    logger.info("Mermaid融合の儀式を開始します")
    fusion_master = MermaidFusionMaster()
    fusion_master.orchestrate_fusion(
        'example2/hovercraft_assets/index.html',
        'example2/hovercraft_assets/enchanted_output.html'
    )

if __name__ == "__main__":
    main()
