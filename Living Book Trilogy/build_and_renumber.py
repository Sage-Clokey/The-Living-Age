#!/usr/bin/env python3
"""
Generate 6 new chapter PDFs from markdown drafts and renumber all existing
chapter files to match the planned structure in chapters_content.json.
"""

import os
import re
import markdown
from weasyprint import HTML

BASE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# 1. CSS matching existing PDF style (Letter size, clean serif typography)
# ---------------------------------------------------------------------------
CSS = """
@page {
    size: Letter;
    margin: 1in;
}
body {
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 12pt;
    line-height: 1.6;
    color: #222;
}
h1 {
    font-size: 22pt;
    margin-top: 0;
    margin-bottom: 4pt;
    page-break-after: avoid;
}
h2 {
    font-size: 16pt;
    margin-top: 24pt;
    margin-bottom: 8pt;
    page-break-after: avoid;
}
h3 {
    font-size: 13pt;
    margin-top: 18pt;
    margin-bottom: 6pt;
    page-break-after: avoid;
}
p {
    margin: 0 0 10pt 0;
    text-align: justify;
}
blockquote {
    margin: 12pt 24pt;
    padding-left: 12pt;
    border-left: 3pt solid #888;
    font-style: italic;
    color: #444;
}
hr {
    border: none;
    border-top: 1px solid #ccc;
    margin: 20pt 0;
}
ul, ol {
    margin: 8pt 0;
    padding-left: 24pt;
}
li {
    margin-bottom: 4pt;
}
strong {
    font-weight: bold;
}
em {
    font-style: italic;
}
table {
    border-collapse: collapse;
    margin: 12pt 0;
    width: 100%;
}
th, td {
    border: 1px solid #999;
    padding: 6pt 8pt;
    text-align: left;
    font-size: 11pt;
}
th {
    background: #f0f0f0;
    font-weight: bold;
}
.header-meta {
    font-size: 10pt;
    color: #666;
    margin-bottom: 16pt;
    border-bottom: 1px solid #ccc;
    padding-bottom: 8pt;
}
"""


def md_to_pdf(md_path, pdf_path, book_label, part_label, chapter_label):
    """Convert a markdown file to a styled PDF."""
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    html_body = markdown.markdown(md_text, extensions=["tables", "smarty"])

    header = f'<div class="header-meta">{book_label}<br>{part_label}<br>{chapter_label}</div>'

    full_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>{CSS}</style></head>
<body>{header}{html_body}</body></html>"""

    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    HTML(string=full_html).write_pdf(pdf_path)
    print(f"  PDF created: {os.path.relpath(pdf_path, BASE)}")


# ---------------------------------------------------------------------------
# 2. Generate the 6 new chapter PDFs
# ---------------------------------------------------------------------------
NEW_CHAPTERS = [
    {
        "src": "chapter_drafts/maul_shadow_lord.md",
        "dst": "Book II - The Spiral and the Block/Part 2 - The Mythology of Media/Chapter 13 - Maul the Shadow Lord.pdf",
        "book": "Book II - The Spiral and the Block",
        "part": "Part 2 - The Mythology of Media",
        "chapter": "Chapter 13 - Maul the Shadow Lord",
    },
    {
        "src": "chapter_drafts/neutral_jing.md",
        "dst": "Book II - The Spiral and the Block/Part 2 - The Mythology of Media/Chapter 18 - Neutral Jing.pdf",
        "book": "Book II - The Spiral and the Block",
        "part": "Part 2 - The Mythology of Media",
        "chapter": "Chapter 18 - Neutral Jing",
    },
    {
        "src": os.path.join(os.pardir, "writings", "the-sokovia-problem.md"),
        "dst": "Book II - The Spiral and the Block/Part 2 - The Mythology of Media/Chapter 26 - The Sokovia Problem.pdf",
        "book": "Book II - The Spiral and the Block",
        "part": "Part 2 - The Mythology of Media",
        "chapter": "Chapter 26 - The Sokovia Problem",
    },
    {
        "src": "chapter_drafts/book3_ch02.md",
        "dst": "Book III - The Spiral Steward/Part 1 - The Industrial Error and the Living Age/Chapter 02 - The Men Who Made People Into Parts.pdf",
        "book": "Book III - The Spiral Steward",
        "part": "Part 1 - The Industrial Error and the Living Age",
        "chapter": "Chapter 02 - The Men Who Made People Into Parts",
    },
    {
        "src": "chapter_drafts/book3_ch03.md",
        "dst": "Book III - The Spiral Steward/Part 1 - The Industrial Error and the Living Age/Chapter 03 - The Death Pledge and the Cabin.pdf",
        "book": "Book III - The Spiral Steward",
        "part": "Part 1 - The Industrial Error and the Living Age",
        "chapter": "Chapter 03 - The Death Pledge and the Cabin",
    },
    {
        "src": "chapter_drafts/the_wild_is_true_order.md",
        "dst": "Book III - The Spiral Steward/Part 1 - The Industrial Error and the Living Age/Chapter 05 - The Wild Is the Place of True Order.pdf",
        "book": "Book III - The Spiral Steward",
        "part": "Part 1 - The Industrial Error and the Living Age",
        "chapter": "Chapter 05 - The Wild Is the Place of True Order",
    },
]

# ---------------------------------------------------------------------------
# 3. Rename existing files to match JSON numbering
#    Order: high-to-low within each group to avoid clobbering
# ---------------------------------------------------------------------------
RENAMES = []

# --- Book III Part 1: rename 04->07, 03->06, 02->04 (high to low target) ---
b3p1 = "Book III - The Spiral Steward/Part 1 - The Industrial Error and the Living Age"
renames_b3p1 = [
    ("Chapter 04 - The Green Flame - A Declaration", "Chapter 07 - The Green Flame - A Declaration"),
    ("Chapter 03 - The Necessary Death", "Chapter 06 - The Necessary Death"),
    ("Chapter 02 - Life Is Not a Machine", "Chapter 04 - Life Is Not a Machine"),
]
for old_name, new_name in renames_b3p1:
    RENAMES.append((f"{b3p1}/{old_name}.pdf", f"{b3p1}/{new_name}.pdf"))

# --- Book III Part 2: rename 11->14, 10->13, ..., 05->08 ---
b3p2 = "Book III - The Spiral Steward/Part 2 - Austrian Economics Meets Molecular Biology"
b3p2_chapters = [
    ("Chapter 11 - The Genome of Liberty", "Chapter 14 - The Genome of Liberty"),
    ("Chapter 10 - Diversity Is Functional", "Chapter 13 - Diversity Is Functional"),
    ("Chapter 09 - The Disease Is the State", "Chapter 12 - The Disease Is the State"),
    ("Chapter 08 - The Entrepreneur and the Central Planner in Biology", "Chapter 11 - The Entrepreneur and the Central Planner in Biology"),
    ("Chapter 07 - Your Cells Dont Have a King", "Chapter 10 - Your Cells Dont Have a King"),
    ("Chapter 06 - The Knowledge Problem Is Biological", "Chapter 09 - The Knowledge Problem Is Biological"),
    ("Chapter 05 - Spontaneous Order in the Cell", "Chapter 08 - Spontaneous Order in the Cell"),
]
for old_name, new_name in b3p2_chapters:
    RENAMES.append((f"{b3p2}/{old_name}.pdf", f"{b3p2}/{new_name}.pdf"))

# --- Book III Part 3: rename 15->18, 14->17, 13->16, 12->15 ---
b3p3 = "Book III - The Spiral Steward/Part 3 - How a Forest Becomes a Forest"
b3p3_chapters = [
    ("Chapter 15 - Bioinformatics as Stewardship of Living Order", "Chapter 18 - Bioinformatics as Stewardship of Living Order"),
    ("Chapter 14 - What Bioinformatics Taught Me About Freedom", "Chapter 17 - What Bioinformatics Taught Me About Freedom"),
    ("Chapter 13 - The Storm and the Seeds", "Chapter 16 - The Storm and the Seeds"),
    ("Chapter 12 - How a Forest Becomes a Forest", "Chapter 15 - How a Forest Becomes a Forest"),
]
for old_name, new_name in b3p3_chapters:
    RENAMES.append((f"{b3p3}/{old_name}.pdf", f"{b3p3}/{new_name}.pdf"))

# --- Book III Part 4: rename 20->23, 19->22, 18->21, 17->20, 16->19 ---
b3p4 = "Book III - The Spiral Steward/Part 4 - Living Algorithms"
b3p4_chapters = [
    ("Chapter 20 - The Fatal Conceit of Biology", "Chapter 23 - The Fatal Conceit of Biology"),
    ("Chapter 19 - The Immune Economy and the Fatal Syringe", "Chapter 22 - The Immune Economy and the Fatal Syringe"),
    ("Chapter 18 - Evolution as Gods Proactive Creation", "Chapter 21 - Evolution as Gods Proactive Creation"),
    ("Chapter 17 - Why Genome Browsers Are Hard to Use", "Chapter 20 - Why Genome Browsers Are Hard to Use"),
    ("Chapter 16 - Living Algorithms", "Chapter 19 - Living Algorithms"),
]
for old_name, new_name in b3p4_chapters:
    # These chapters have both .pdf and .md variants
    RENAMES.append((f"{b3p4}/{old_name}.pdf", f"{b3p4}/{new_name}.pdf"))
    # Check for .md variants
    md_old = os.path.join(BASE, f"{b3p4}/{old_name}.md")
    if os.path.exists(md_old):
        RENAMES.append((f"{b3p4}/{old_name}.md", f"{b3p4}/{new_name}.md"))

# --- Book III Part 5: rename 25->28, 24->27, 23->26, 22->25, 21->24 ---
b3p5 = "Book III - The Spiral Steward/Part 5 - LivingWorks - The Tool"
b3p5_chapters = [
    ("Chapter 25 - Why This Requires Many Disciplines", "Chapter 28 - Why This Requires Many Disciplines"),
    ("Chapter 24 - The Navigation", "Chapter 27 - The Navigation"),
    ("Chapter 23 - The Design", "Chapter 26 - The Design"),
    ("Chapter 22 - LivingWorks - The CAD System for the Living Age", "Chapter 25 - LivingWorks - The CAD System for the Living Age"),
    ("Chapter 21 - The Spiral Steward - A New Role", "Chapter 24 - The Spiral Steward - A New Role"),
]
for old_name, new_name in b3p5_chapters:
    RENAMES.append((f"{b3p5}/{old_name}.pdf", f"{b3p5}/{new_name}.pdf"))

# --- Book II Part 3: rename 30->33, 29->32, ..., 23->26 ---
b2p3 = "Book II - The Spiral and the Block/Part 3 - The Eight Pillars"
b2p3_chapters = [
    ("Chapter 30 - Pillar VIII - The Spiral Is the Pattern of Life", "Chapter 33 - Pillar VIII - The Spiral Is the Pattern of Life"),
    ("Chapter 29 - Pillar VII - The Individual Is Sacred", "Chapter 32 - Pillar VII - The Individual Is Sacred"),
    ("Chapter 28 - Pillar VI - Stories Shape Civilizations", "Chapter 31 - Pillar VI - Stories Shape Civilizations"),
    ("Chapter 27 - Pillar V - Wisdom Transcends Authority", "Chapter 30 - Pillar V - Wisdom Transcends Authority"),
    ("Chapter 26 - Pillar IV - Voluntary Cooperation Is Natural", "Chapter 29 - Pillar IV - Voluntary Cooperation Is Natural"),
    ("Chapter 25 - Pillar III - Power Corrupts Centralized Systems", "Chapter 28 - Pillar III - Power Corrupts Centralized Systems"),
    ("Chapter 24 - Pillar II - Truth Emerges from Individuals", "Chapter 27 - Pillar II - Truth Emerges from Individuals"),
    ("Chapter 23 - Pillar I - Life Is Decentralized", "Chapter 26 - Pillar I - Life Is Decentralized"),
]
for old_name, new_name in b2p3_chapters:
    RENAMES.append((f"{b2p3}/{old_name}.pdf", f"{b2p3}/{new_name}.pdf"))

# --- Book II Part 4: rename 32->35, 31->34 ---
b2p4 = "Book II - The Spiral and the Block/Part 4 - The Perfect Agent"
b2p4_chapters = [
    ("Chapter 32 - The Skywalker Spiral", "Chapter 35 - The Skywalker Spiral"),
    ("Chapter 31 - The Perfect Agent - Bible and Quran", "Chapter 34 - The Perfect Agent - Bible and Quran"),
]
for old_name, new_name in b2p4_chapters:
    RENAMES.append((f"{b2p4}/{old_name}.pdf", f"{b2p4}/{new_name}.pdf"))


def main():
    os.chdir(BASE)

    # --- Step 1: Rename existing files (high-to-low to avoid clobbering) ---
    print("=== Renaming existing files to match JSON numbering ===")
    for old_rel, new_rel in RENAMES:
        old_abs = os.path.join(BASE, old_rel)
        new_abs = os.path.join(BASE, new_rel)
        if os.path.exists(old_abs):
            os.makedirs(os.path.dirname(new_abs), exist_ok=True)
            os.rename(old_abs, new_abs)
            print(f"  {old_rel}  ->  {new_rel}")
        else:
            print(f"  SKIP (not found): {old_rel}")

    # --- Step 2: Generate new PDFs ---
    print("\n=== Generating new chapter PDFs ===")
    for ch in NEW_CHAPTERS:
        src = os.path.join(BASE, ch["src"])
        dst = os.path.join(BASE, ch["dst"])
        if not os.path.exists(src):
            print(f"  ERROR: source not found: {ch['src']}")
            continue
        md_to_pdf(src, dst, ch["book"], ch["part"], ch["chapter"])

    # --- Step 3: Verify ---
    print("\n=== Verification ===")
    import json
    with open(os.path.join(BASE, "chapters_content.json"), "r", encoding="utf-8") as f:
        data = json.load(f)

    missing = []
    found = 0
    for key in sorted(data.keys()):
        path = os.path.join(BASE, key)
        if os.path.exists(path):
            found += 1
        else:
            missing.append(key)

    print(f"  JSON entries: {len(data)}")
    print(f"  Found on disk: {found}")
    if missing:
        print(f"  Still missing ({len(missing)}):")
        for m in missing:
            print(f"    {m}")
    else:
        print("  All JSON entries have matching files on disk!")


if __name__ == "__main__":
    main()
