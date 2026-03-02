#!/bin/bash

# Verifica se o usuário passou um arquivo como argumento
if [ -z "$1" ]; then
  echo "Erro: Nenhum arquivo especificado."
  echo "Uso: docker run --rm -v \$(pwd):/workspace md2pdf seu-arquivo.md"
  exit 1
fi

INPUT_FILE="$1"
# Pega o nome do arquivo sem a extensão .md
BASENAME="${INPUT_FILE%.*}"

# 1. Converte Markdown para HTML
# Usamos a extensão "extra" (para tabelas) e "codehilite" (para blocos de código)
markdown_py "$INPUT_FILE" -x extra -x codehilite -f "${BASENAME}.html"

# 2. Converte HTML para PDF usando WeasyPrint
weasyprint "${BASENAME}.html" "${BASENAME}.pdf"

# 3. Limpa o HTML temporário
rm "${BASENAME}.html"

echo "✅ Sucesso! O arquivo ${BASENAME}.pdf foi gerado."
