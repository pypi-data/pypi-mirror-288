import re

def add_animation_to_svg(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        svg_content = file.read()

    # アニメーション用のCSSを更新
    animation_css = '''
    <style>
    .flowchart-link {
        stroke-dasharray: 5, 5;
        animation: flowchart-dash 30s linear infinite;
    }
    @keyframes flowchart-dash {
        to {
            stroke-dashoffset: 1000;
        }
    }
    </style>
    '''
    
    # 既存のstyleタグを探し、その中にアニメーションCSSを追加
    style_match = re.search(r'<style>(.*?)</style>', svg_content, re.DOTALL)
    if style_match:
        updated_style = style_match.group(1) + animation_css
        svg_content = svg_content.replace(style_match.group(0), f'<style>{updated_style}</style>')
    else:
        # styleタグがない場合は、SVGの開始タグの直後に追加
        svg_content = re.sub(r'(<svg[^>]*>)', r'\1' + animation_css, svg_content)

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(svg_content)

# 使用例
input_svg = 'example/hovercraft_assets/svg/mermaid_f03c6d66fd85486592310a73a9af2adc.svg'
output_svg = 'example/hovercraft_assets/svg/animated_mermaid.svg'
add_animation_to_svg(input_svg, output_svg)
print(f"アニメーションが追加されたSVGファイルが {output_svg} に保存されました。")
