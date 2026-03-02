#!/bin/bash

# Verifica se o usuário passou o arquivo
if [ -z "$1" ]; then
  echo "Erro: Você esqueceu de informar o arquivo Markdown."
  echo "Uso correto: md2pdf nome_do_arquivo.md"
  exit 1
fi

# Descobre o caminho absoluto do arquivo (evita erros se você usar '../pasta/arquivo.md')
CAMINHO_ABSOLUTO=$(readlink -f "$1")
PASTA_DO_ARQUIVO=$(dirname "$CAMINHO_ABSOLUTO")
NOME_DO_ARQUIVO=$(basename "$CAMINHO_ABSOLUTO")

# Executa o Docker mapeando a pasta exata onde o arquivo está
echo "Convertendo '$NOME_DO_ARQUIVO' para PDF..."
docker run --rm -v "$PASTA_DO_ARQUIVO":/workspace md2pdf "$NOME_DO_ARQUIVO"
