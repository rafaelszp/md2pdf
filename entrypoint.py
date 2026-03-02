#!/usr/bin/env python3
import sys
import os
import markdown
from weasyprint import HTML

if len(sys.argv) < 2:
    print("Erro: Nenhum arquivo especificado.")
    sys.exit(1)

input_file = sys.argv[1]
basename = os.path.splitext(input_file)[0]
output_pdf = f"{basename}.pdf"

with open(input_file, 'r', encoding='utf-8') as f:
    md_text = f.read()

html_body = markdown.markdown(
    md_text,
    extensions=['extra', 'codehilite', 'toc']
)

html_content = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <style>
        /* Configura a página A4 com margens decentes */
        @page {{ size: A4; margin: 2cm; }}

        body {{ font-family: Arial, "Noto Color Emoji", sans-serif; line-height: 1.6; color: #333; }}

        /* Força a tabela a caber na tela e quebrar textos longos */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
            table-layout: fixed; /* Impede que a tabela ultrapasse 100% da largura */
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
            word-wrap: break-word;      /* Quebra palavras normais */
            overflow-wrap: break-word;  /* Regra moderna de quebra */
            word-break: break-word;     /* Garante que links/códigos longos quebrem */
        }}
        th {{ background-color: #f2f2f2; }}

        /* Força os blocos de código a quebrarem a linha em vez de sumirem da página */
        pre {{
            background: #f4f4f4;
            padding: 15px;
            border-radius: 8px;
            white-space: pre-wrap; /* Essencial: faz o código quebrar de linha no PDF */
            word-wrap: break-word;
        }}
        code {{ background: #f4f4f4; padding: 2px 5px; border-radius: 4px; font-family: monospace; font-size: 0.9em; }}

        a {{ color: #0366d6; text-decoration: none; }}
        img {{ max-width: 100%; height: auto; }} /* Impede imagens gigantes de vazarem */
    </style>
</head>
<body>
    {html_body}
</body>
</html>
"""

print(f"Renderizando o PDF para '{input_file}'...")
HTML(string=html_content).write_pdf(output_pdf)

print(f"✅ Sucesso! O arquivo {output_pdf} foi gerado perfeitamente.")
