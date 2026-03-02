#!/bin/bash

# Check if the user provided the file
if [ -z "$1" ]; then
  echo "Error: You forgot to specify the Markdown file."
  echo "Correct usage: md2pdf filename.md"
  exit 1
fi

# Discover the absolute path of the file (avoids errors if you use '../folder/file.md')
CAMINHO_ABSOLUTO=$(readlink -f "$1")
PASTA_DO_ARQUIVO=$(dirname "$CAMINHO_ABSOLUTO")
NOME_DO_ARQUIVO=$(basename "$CAMINHO_ABSOLUTO")

# Run Docker mapping the exact folder where the file is located
echo "Converting '$NOME_DO_ARQUIVO' to PDF..."
docker run --rm -v "$PASTA_DO_ARQUIVO":/workspace md2pdf "$NOME_DO_ARQUIVO"
