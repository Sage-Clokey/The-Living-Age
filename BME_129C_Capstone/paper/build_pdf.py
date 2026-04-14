"""
Build capstone paper as PDF with integrated figures.
Converts Markdown → HTML with academic styling → PDF via WeasyPrint.
"""

import re
import base64
from pathlib import Path
import markdown
from weasyprint import HTML

PAPER_DIR = Path(__file__).resolve().parent
FIGURES_DIR = PAPER_DIR / "figures"
MD_FILE = PAPER_DIR / "capstone_paper.md"
OUT_PDF = PAPER_DIR / "capstone_paper.pdf"


def embed_image(match):
    """Replace markdown image references with base64-embedded images."""
    alt = match.group(1)
    src = match.group(2)

    # Resolve path relative to paper dir
    img_path = PAPER_DIR / src
    if not img_path.exists():
        # Try figures dir directly
        img_path = FIGURES_DIR / Path(src).name
    if not img_path.exists():
        return f'<p class="missing-fig">[Figure not found: {src}]</p>'

    suffix = img_path.suffix.lower()
    mime = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
            ".svg": "image/svg+xml", ".pdf": "application/pdf"}.get(suffix, "image/png")

    # For PDF figures, skip embedding (WeasyPrint can't render embedded PDFs)
    if suffix == ".pdf":
        png_alt = img_path.with_suffix(".png")
        if png_alt.exists():
            img_path = png_alt
            mime = "image/png"
        else:
            return f'<p class="missing-fig">[PDF figure: {src} — convert to PNG]</p>'

    data = base64.b64encode(img_path.read_bytes()).decode()
    return f'<img src="data:{mime};base64,{data}" alt="{alt}" class="figure-img">'


def md_to_html(md_text: str) -> str:
    """Convert markdown to HTML, embedding images as base64."""
    # Replace image references with embedded versions
    # Pattern: ![alt](path)
    md_text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', embed_image, md_text)

    # Convert markdown to HTML
    extensions = ['tables', 'fenced_code', 'footnotes', 'smarty']
    html_body = markdown.markdown(md_text, extensions=extensions)

    return html_body


def build():
    md_text = MD_FILE.read_text(encoding="utf-8")
    html_body = md_to_html(md_text)

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
@page {{
    size: letter;
    margin: 1in 1in 1in 1in;
    @bottom-center {{
        content: counter(page);
        font-family: Georgia, serif;
        font-size: 9pt;
        color: #666;
    }}
}}

body {{
    font-family: Georgia, "Times New Roman", serif;
    font-size: 11pt;
    line-height: 1.65;
    color: #1a1a1a;
    max-width: 100%;
    text-align: justify;
    hyphens: auto;
}}

/* Title */
h1 {{
    font-size: 18pt;
    font-weight: bold;
    text-align: center;
    margin-bottom: 6pt;
    line-height: 1.3;
    color: #0d1117;
    page-break-after: avoid;
}}

/* Author block */
h1 + p {{
    text-align: center;
}}

/* Section headers */
h2 {{
    font-size: 14pt;
    font-weight: bold;
    margin-top: 28pt;
    margin-bottom: 10pt;
    color: #1b4332;
    border-bottom: 1px solid #2d6a4f;
    padding-bottom: 4pt;
    page-break-after: avoid;
}}

h3 {{
    font-size: 12pt;
    font-weight: bold;
    margin-top: 20pt;
    margin-bottom: 8pt;
    color: #2d6a4f;
    page-break-after: avoid;
}}

/* Paragraphs */
p {{
    margin-bottom: 8pt;
    orphans: 3;
    widows: 3;
}}

/* Epigraph / blockquotes */
blockquote {{
    margin: 16pt 30pt;
    padding: 8pt 16pt;
    border-left: 3px solid #2d6a4f;
    background: #f8f9f7;
    font-style: italic;
    color: #333;
    page-break-inside: avoid;
}}

blockquote p {{
    margin-bottom: 4pt;
}}

/* Italicized epigraph lines at section starts */
h2 + p > em:first-child {{
    display: block;
    font-style: italic;
    color: #2d6a4f;
    margin-bottom: 12pt;
    font-size: 10.5pt;
}}

/* Bold emphasis */
strong {{
    color: #1a1a1a;
}}

/* Inline emphasis */
em {{
    font-style: italic;
}}

/* Figures */
.figure-img {{
    display: block;
    max-width: 100%;
    margin: 16pt auto;
    page-break-inside: avoid;
}}

/* Figure captions (paragraphs after images starting with "Figure") */
img + p, .figure-img + p {{
    font-size: 9.5pt;
    color: #444;
    line-height: 1.5;
    margin-top: -8pt;
    margin-bottom: 16pt;
}}

/* Tables */
table {{
    border-collapse: collapse;
    width: 100%;
    margin: 14pt 0;
    font-size: 9.5pt;
    page-break-inside: avoid;
}}

th {{
    background: #1b4332;
    color: white;
    font-weight: bold;
    padding: 6pt 8pt;
    text-align: left;
    border: 1px solid #1b4332;
}}

td {{
    padding: 5pt 8pt;
    border: 1px solid #ddd;
    vertical-align: top;
}}

tr:nth-child(even) {{
    background: #f5f7f5;
}}

/* Horizontal rules */
hr {{
    border: none;
    border-top: 1px solid #ccc;
    margin: 24pt 0;
}}

/* Lists */
ul, ol {{
    margin: 8pt 0 8pt 24pt;
}}

li {{
    margin-bottom: 4pt;
}}

/* Math (inline) */
code {{
    font-family: "Courier New", monospace;
    font-size: 10pt;
    background: #f0f0f0;
    padding: 1pt 3pt;
    border-radius: 2pt;
}}

/* Missing figures */
.missing-fig {{
    background: #fff3cd;
    border: 1px solid #ffc107;
    padding: 8pt;
    text-align: center;
    color: #856404;
    font-style: italic;
}}

/* Page breaks before major sections */
h2 {{
    page-break-before: auto;
}}

/* Keep figure + caption together */
p:has(> img), p:has(> .figure-img) {{
    page-break-inside: avoid;
    page-break-after: avoid;
}}

/* References section - smaller font */
h2:last-of-type ~ p {{
    font-size: 10pt;
    line-height: 1.45;
}}

/* Author info styling */
h1 + p > strong {{
    font-size: 12pt;
}}
</style>
</head>
<body>
{html_body}
</body>
</html>"""

    print("Generating PDF...")
    HTML(string=full_html, base_url=str(PAPER_DIR)).write_pdf(str(OUT_PDF))
    print(f"Saved: {OUT_PDF}")
    print(f"Size: {OUT_PDF.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    build()
