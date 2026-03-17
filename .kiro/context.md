# md2pdf — Contexto do Projeto

## Visão Geral

Ferramenta CLI Docker-based que converte Markdown → PDF usando Python, WeasyPrint e tipografia monoespaçada (Hack). Projeto inteiramente gerado por IA.

## Arquitetura

- `entrypoint.py` — script Python principal (lê MD, aplica fixes, converte HTML, gera PDF via WeasyPrint)
- `md2pdf.sh` — wrapper Bash (resolve caminhos, monta volume Docker, executa container)
- `Dockerfile` — imagem python:3.12-slim com WeasyPrint, fontes (Hack, DejaVu, Noto Color Emoji), Pygments
- `prompt.md` — prompt original usado para gerar o projeto

## Problemas Resolvidos

### Outline vermelha em box-drawing characters (2026-03-17)

**Problema:** Caracteres como `│ ├── └── ──▶` apareciam com borda/outline vermelha no PDF.

**Causa raiz:** O Pygments aplica `border: 1px solid #F00` na classe `.codehilite .err` para tokens que o lexer não reconhece. Box-drawing e setas dentro de code blocks eram classificados como "erro".

**Solução:** Adicionado CSS override `.codehilite .err { border: none; }` após o CSS do Pygments no `entrypoint.py`. Também adicionado DejaVu Sans Mono como font fallback e `@font-face` BoxDraw com `unicode-range` para cobertura Unicode estendida.

**Commit:** e423dd6

### Diagramas ASCII quebrando no PDF (2026-03-17)

**Problema:** Diagramas ASCII largos (ex: fluxogramas com múltiplas colunas de boxes) ficavam completamente quebrados no PDF — linhas partidas, caracteres desalinhados.

**Causa raiz:** Duas coisas:
1. `white-space: pre-wrap` + `word-wrap: break-word` no `.codehilite pre` quebravam linhas do diagrama para caber na página, destruindo o alinhamento.
2. `font-size: 0.9em` e `padding: 2px 5px` no `code` afetavam o `<code>` dentro de `.codehilite pre`, alterando o espaçamento.

**Solução:**
- `.codehilite pre`: trocado `pre-wrap` por `pre`, removido `word-wrap`, adicionado `font-size: 0.7em` para diagramas largos caberem na página A4.
- `.codehilite`: adicionado `overflow: hidden` como safety net.
- `.codehilite code`: reset de background, padding, border-radius e font-size para não interferir no espaçamento mono.
- Trade-off: fonte menor em code blocks (0.7em) para acomodar diagramas largos.

## Detalhes Técnicos

- Fontes: Hack (principal) → DejaVu Sans Mono (fallback) → monospace → OnlyEmojis
- `@font-face` BoxDraw aponta para `/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf` via `url()` (WeasyPrint nem sempre resolve `local()`)
- `@font-face` OnlyEmojis com `unicode-range` restrito evita que Noto Color Emoji sequestre números
- Auto-fix de listas grudadas via regex no entrypoint
- Extensões Markdown: extra, codehilite, toc

## Divergências com o prompt original

- Font-face no código é `OnlyEmojis` (prompt pedia `ApenasEmojis`)
- Hack instalado via apt-get (prompt pedia download direto do GitHub)
- `rm -rf /var/lib/apt/lists/*` duplicado no Dockerfile (bug menor)
