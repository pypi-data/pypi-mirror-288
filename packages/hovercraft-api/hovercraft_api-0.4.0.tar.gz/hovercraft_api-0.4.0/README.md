<p align="center">
<img src="https://huggingface.co/datasets/MakiAi/IconAssets/resolve/main/HovercraftAPI.png" width="100%">
<br>
<h1 align="center">HovercraftAPI</h1>
<h2 align="center">
  ～ Craft your story, let HovercraftAPI do the rest ～
<br>
  <img alt="PyPI - Version" src="https://img.shields.io/pypi/v/hovercraft-api">
<img alt="PyPI - Format" src="https://img.shields.io/pypi/format/hovercraft-api">
<img alt="PyPI - Implementation" src="https://img.shields.io/pypi/implementation/hovercraft-api">
<img alt="PyPI - Status" src="https://img.shields.io/pypi/status/hovercraft-api">
<img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dd/hovercraft-api">
<img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dw/hovercraft-api">
<img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/hovercraft-api">
<img alt="PyPI - Downloads" src="https://img.shields.io/pepy/dt/hovercraft-api">

<a href="https://github.com/Sunwood-ai-labs/HovercraftAPI" title="Go to GitHub repo"><img src="https://img.shields.io/static/v1?label=HovercraftAPI&message=Sunwood-ai-labs&color=blue&logo=github"></a>
<img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/Sunwood-ai-labs/HovercraftAPI">
<a href="https://github.com/Sunwood-ai-labs/HovercraftAPI"><img alt="forks - Sunwood-ai-labs" src="https://img.shields.io/github/forks/HovercraftAPI/Sunwood-ai-labs?style=social"></a>
<a href="https://github.com/Sunwood-ai-labs/HovercraftAPI"><img alt="GitHub Last Commit" src="https://img.shields.io/github/last-commit/Sunwood-ai-labs/HovercraftAPI"></a>
<a href="https://github.com/Sunwood-ai-labs/HovercraftAPI"><img alt="GitHub Top Language" src="https://img.shields.io/github/languages/top/Sunwood-ai-labs/HovercraftAPI"></a>
<img alt="GitHub Release" src="https://img.shields.io/github/v/release/Sunwood-ai-labs/HovercraftAPI?color=red">
<img alt="GitHub Tag" src="https://img.shields.io/github/v/tag/Sunwood-ai-labs/HovercraftAPI?sort=semver&color=orange">
<img alt="GitHub Actions Workflow Status" src="https://img.shields.io/github/actions/workflow/status/Sunwood-ai-labs/HovercraftAPI/publish-to-pypi.yml">
<br>
<p align="center">
  <a href="https://hamaruki.com/"><b>[🌐 Website]</b></a> •
  <a href="https://github.com/Sunwood-ai-labs"><b>[🐱 GitHub]</b></a>
  <a href="https://x.com/hAru_mAki_ch"><b>[🐦 Twitter]</b></a> •
  <a href="https://hamaruki.com/"><b>[🍀 Official Blog]</b></a>
</p>

</h2>

</p>

>[!IMPORTANT]
>このリポジトリのリリースノートやREADME、コミットメッセージの9割近くは[claude.ai](https://claude.ai/)や[ChatGPT4](https://chatgpt.com/)を活用した[AIRA](https://github.com/Sunwood-ai-labs/AIRA), [SourceSage](https://github.com/Sunwood-ai-labs/SourceSage), [Gaiah](https://github.com/Sunwood-ai-labs/Gaiah), [HarmonAI_II](https://github.com/Sunwood-ai-labs/HarmonAI_II)で生成しています。

## 🌟 HovercraftAPI

HovercraftAPIは、Markdownファイルから印象的なHovercraftプレゼンテーションを簡単に作成するためのPythonツールです。Mermaidダイアグラムやコードブロックのサポート、カスタムCSSによるスタイリングなど、多彩な機能を提供します。

## 🎥 デモ

https://github.com/user-attachments/assets/670f8b37-88eb-4f8e-9bbe-2bf9f7797d5e

## 🚀 はじめに

### インストール

```bash
pip install hovercraft-api
```

## 📝 HovercraftAPIの使い方

### コマンドラインインターフェース

基本的な使用方法:
```bash
hovercraftapi example/README.md -c css/mytheme.css
```

3Dダイナミックトランジションを有効にする場合:
```bash
hovercraft-api example3/README.md -c css/mytheme.css --enable-dynamic-position
```


### css

```bash
poetry run hovercraft-api example3/README.md -c css/oasis.css --enable-dynamic-position 
poetry run hovercraft-api example3/README.md -c css/Deepsea_and_Rust.css --enable-dynamic-position --svg-css-file css/svg_oasis.css
```

### Pythonスクリプト内での使用

```python
from hovercraft_api import HovercraftAPI

api = HovercraftAPI("your_markdown_file.md", css_file="path/to/your/custom.css", enable_dynamic_position=True)
api.generate_slides()
```

## 特徴

* Markdownからスライドを生成
* Mermaidダイアグラムとコードブロックをサポート
* カスタムCSSによるスタイリング
* CLIインターフェース対応
* スライドのキャプチャと動画生成機能 (実験的機能)
* 動的なスライド位置決め機能 ([v0.2.0で追加](https://github.com/Sunwood-ai-labs/HovercraftAPI/releases/tag/v0.2.0))
* MermaidダイアグラムのSVG変換とアニメーション ([v0.2.0で追加](https://github.com/Sunwood-ai-labs/HovercraftAPI/releases/tag/v0.2.0))
* ローカルMermaid SVGプレビューサーバー ([v0.2.0で追加](https://github.com/Sunwood-ai-labs/HovercraftAPI/releases/tag/v0.2.0))

## 必要条件

* Python 3.10以上
* Poetry（依存関係管理に使用）
* その他の依存関係は `pyproject.toml` を参照してください。

## カスタムCSS

デフォルトのCSSファイルは `css/mytheme.css` です。カスタムCSSファイルを使用する場合は、`-c` または `--css` オプションで指定してください。

## プロジェクト構造

```plaintext
HovercraftAPI/
├─ css/
│  ├─ mytheme.css
│  ├─ flowchart1.css
├─ docs/
│  ├─ usage.md
├─ example/
│  ├─ README.md
│  ├─ sample.py
├─ hovercraft_api/
│  ├─ code_block_alchemist.py
│  ├─ dynamic_rst_adjuster.py
│  ├─ HovercraftAPI.py
│  ├─ hovercraft_converter.py
│  ├─ markdown_to_rst_converter.py
│  ├─ markdown_to_slides_converter.py
│  ├─ mermaid_alchemist.py
│  ├─ mermaid_server.py
│  ├─ mermaid_svg_converter.py
│  ├─ rst_adjuster.py
│  ├─ slide_capturer.py
│  ├─ svg_animator.py
│  ├─ utils.py
│  ├─ __init__.py
├─ pyproject.toml
├─ README.md
```

## 🛠️ 開発

このプロジェクトはPoetryを使用して依存関係を管理しています。開発環境のセットアップは以下のコマンドで行えます：

```bash
poetry install
```

3Dダイナミックトランジションを有効にしてHovercraftAPIを実行:
```bash
poetry run hovercraft-api example2\README.md  --enable-dynamic-position
```

ローカルMermaid SVGプレビューサーバーを起動:
```bash
poetry run python hovercraft_api\mermaid_server.py
```

MermaidダイアグラムをSVGに変換:
```bash
poetry run python hovercraft_api\mermaid_svg_converter.py
```


MermaidダイアグラムをSVGに変換:
```bash
poetry run hovercraft-api example2\README.md --stages capture_slides --capture-images --capture-video
```

## 🤝 貢献

プルリクエストは大歓迎です。大きな変更の場合は、まずissueを開いて議論してください。

## 🙏 サポート

問題が発生した場合は、GitHubのissueを開いてください。 

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は [LICENSE](LICENSE) ファイルを参照してください。
