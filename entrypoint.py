#!/usr/bin/env python3
import sys
import os
import re
import markdown
from weasyprint import HTML
from pygments.formatters import HtmlFormatter

if len(sys.argv) < 2:
    print("Error: No file specified.")
    sys.exit(1)

input_file = sys.argv[1]
basename = os.path.splitext(input_file)[0]
output_pdf = f"{basename}.pdf"

# 1. Read the Markdown file
with open(input_file, 'r', encoding='utf-8') as f:
    md_text = f.read()

# ==========================================
# MAGIC AUTO-FIX FOR ATTACHED LISTS
# Injects a double line break before lists (with markers -, *, + or numbers)
# if the previous text is attached to them.
md_text = re.sub(r'([^\n])\n(\s*[-*+]\s+)', r'\1\n\n\2', md_text)
md_text = re.sub(r'([^\n])\n(\s*\d+\.\s+)', r'\1\n\n\2', md_text)
# ==========================================

# 2. Convert to HTML
html_body = markdown.markdown(
    md_text,
    extensions=['extra', 'codehilite', 'toc']
)

# 3. Pygments colors
pygments_css = HtmlFormatter(style='default').get_style_defs('.codehilite')

# 4. Final HTML with hardened CSS
html_content = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <style>
        {pygments_css}

        @page {{ size: A4; margin: 2cm; }}

        @font-face {{
            font-family: 'OnlyEmojis';
            src: local('Noto Color Emoji');
            unicode-range: U+2600-27BF, U+1F300-1F9FF, U+1FA70-1FAFF;
        }}

        body {{
            font-family: "Hack", monospace, "OnlyEmojis";
            line-height: 1.6;
            color: #333;
        }}

        table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; table-layout: fixed; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; word-wrap: break-word; overflow-wrap: break-word; word-break: break-word; }}
        th {{ background-color: #f2f2f2; }}

        pre, code {{ font-family: "Hack", monospace, "OnlyEmojis"; }}
        .codehilite {{ background: #f8f8f8; padding: 15px; border-radius: 8px; margin-bottom: 20px; }}
        .codehilite pre {{ margin: 0; white-space: pre-wrap; word-wrap: break-word; }}
        code {{ background: #f4f4f4; padding: 2px 5px; border-radius: 4px; font-size: 0.9em; }}

        /* Visual guarantee for lists */
        ul, ol {{ margin-top: 1em; margin-bottom: 1em; padding-left: 40px; display: block; }}
        li {{ display: list-item; margin-bottom: 0.5em; }}
        ul ul, ol ol, ul ol, ol ul {{ margin-top: 0; margin-bottom: 0; }}

        a {{ color: #0366d6; text-decoration: none; }}
        img {{ max-width: 100%; height: auto; }}
    </style>
</head>
<body>
    {html_body}
</body>
</html>
"""

# 5. Render the PDF
print(f"Rendering PDF for '{input_file}'...")
HTML(string=html_content).write_pdf(output_pdf)

print(f"✅ Success! The file {output_pdf} was generated perfectly.")
