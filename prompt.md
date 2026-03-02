**Act as a DevOps Engineer and Python Expert.**
I need to create a Docker-based command-line tool to convert Markdown files into high-quality PDFs. I want to avoid Node/Chromium-based tools or Pandoc/LaTeX. The strategy must use Python's native `Markdown` library and `WeasyPrint` for rendering.
Generate the `Dockerfile` and the `entrypoint.py` script strictly following the requirements below:
**Dockerfile Requirements:**
1. Use the base image `python:3.12-slim`.
2. Install WeasyPrint's graphical dependencies via `apt-get`: `libpango-1.0-0`, `libpangoft2-1.0-0`, `libffi-dev`, `libjpeg-dev`, `libopenjp2-7-dev`.
3. Install `fontconfig`, `wget`, `unzip`, and the `fonts-noto-color-emoji` package (for emojis).
4. **Crucial for typography:** Do not install the Hack font via `apt-get`. Download it directly from the Source Foundry GitHub releases (version v3.003 TTF) using `wget`, extract it to the system fonts folder, and run `fc-cache -f -v`.
5. Install via `pip`: `Markdown`, `WeasyPrint`, and `Pygments`.
6. Set `WORKDIR /workspace` and define the `entrypoint.py` script as executable and as the `ENTRYPOINT` of the image.


**entrypoint.py Requirements (Processing and HTML):**
1. Read the Markdown file passed as an argument, forcing `utf-8` encoding.
2. **List Auto-Fix:** Use the `re` (regex) library to automatically inject a blank line before lists (marked with `-`, `*`, `+`, or numbers) if they are attached to the preceding text without a blank line. This bypasses the limitation of Python's standard Markdown library, which renders glued lists "inline".
3. Convert to HTML activating the extensions: `extra`, `codehilite`, and `toc`.
4. Generate the Syntax Highlighting CSS using Pygments' `HtmlFormatter` ('default' style) and inject it into the final HTML.


**Visual and CSS Requirements (WeasyPrint):**
The generated HTML must contain a `<style` block with the following rules to bypass known WeasyPrint bugs:
1. **Emoji Shielding:** Create an `@font-face` named `ApenasEmojis` pointing to `Noto Color Emoji`, but apply a restricted `unicode-range` to emoji blocks (e.g., `U+2600-27BF, U+1F300-1F9FF, U+1FA70-1FAFF`). This prevents the emoji font from "hijacking" normal numbers and causing bizarre spacing.
2. **Main Font:** Set `body`, `pre`, and `code` to use `font-family: "Hack", monospace, "ApenasEmojis";` (100% monospaced document).
3. **Tables and Limits:** Force `table-layout: fixed;` and `word-wrap: break-word;` on tables (`td`, `th`) to prevent them from overflowing the A4 page.
4. **Code Blocks:** Force `white-space: pre-wrap;` and `word-wrap: break-word;` inside the `.codehilite pre` class so that the code wraps to the next line instead of disappearing off the page.
5. **Page Formatting:** 2cm margins, A4 size, and ensure correct margins on `ul`, `ol`, and `li` tags.


The script must save the PDF in the same directory with the same name as the original file and display success messages in the terminal.
