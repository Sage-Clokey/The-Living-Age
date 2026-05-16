#!/usr/bin/env python3
"""
Add 5 new chapter entries to chapters_content.js by converting
markdown files to simple HTML matching the existing style.
"""

import json
import re
import os

CHAPTERS = [
    {
        "key": "Book I - The Sagent Creed/Part 2 - The Shaken Jar/Chapter 06 - The Hidden War.pdf",
        "src": "book1_ch06.md",
    },
    {
        "key": "Book I - The Sagent Creed/Part 2 - The Shaken Jar/Chapter 08 - The King They Asked For.pdf",
        "src": "book1_ch08.md",
    },
    {
        "key": "Book I - The Sagent Creed/Part 4 - The Fibonacci Spiral Through the Generations/Chapter 15 - The Names That Wrote Themselves.pdf",
        "src": "book1_ch15.md",
    },
    {
        "key": "Book I - The Sagent Creed/Part 5 - Sheep Among Wolves/Chapter 23 - The Sagent Narrative.pdf",
        "src": "book1_ch23.md",
    },
    {
        "key": "Book II - The Spiral and the Block/Part 4 - The Perfect Agent/Chapter 34 - The Perfect Agent - Bible and Quran.pdf",
        "src": "book2_ch34.md",
    },
]

DRAFT_DIR = os.path.dirname(os.path.abspath(__file__))
JS_FILE = os.path.join(DRAFT_DIR, "..", "chapters_content.js")


def md_to_html(md_text: str) -> str:
    """Convert markdown to simple HTML matching the existing chapter style."""
    lines = md_text.split("\n")
    html_parts = []
    in_blockquote = False
    in_ul = False
    in_table = False
    table_rows = []

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Skip empty lines (they just separate blocks)
        if not stripped:
            if in_blockquote:
                in_blockquote = False
            if in_ul:
                html_parts.append("</ul>")
                in_ul = False
            if in_table:
                _flush_table(html_parts, table_rows)
                table_rows = []
                in_table = False
            i += 1
            continue

        # Horizontal rule
        if stripped == "---" or stripped == "***" or stripped == "___":
            if in_ul:
                html_parts.append("</ul>")
                in_ul = False
            if in_table:
                _flush_table(html_parts, table_rows)
                table_rows = []
                in_table = False
            html_parts.append("<hr>")
            i += 1
            continue

        # Table rows
        if "|" in stripped and stripped.startswith("|"):
            # Check if it's a separator row like |---|---|
            if re.match(r"^\|[\s\-:|]+\|$", stripped):
                i += 1
                continue
            if not in_table:
                if in_ul:
                    html_parts.append("</ul>")
                    in_ul = False
                in_table = True
            table_rows.append(stripped)
            i += 1
            continue

        if in_table:
            _flush_table(html_parts, table_rows)
            table_rows = []
            in_table = False

        # Headers
        if stripped.startswith("### "):
            if in_ul:
                html_parts.append("</ul>")
                in_ul = False
            content = _inline_format(stripped[4:])
            html_parts.append(f"<h3>{content}</h3>")
            i += 1
            continue
        if stripped.startswith("## "):
            if in_ul:
                html_parts.append("</ul>")
                in_ul = False
            content = _inline_format(stripped[3:])
            html_parts.append(f"<h2>{content}</h2>")
            i += 1
            continue
        if stripped.startswith("# "):
            if in_ul:
                html_parts.append("</ul>")
                in_ul = False
            content = _inline_format(stripped[2:])
            html_parts.append(f"<h1>{content}</h1>")
            i += 1
            continue

        # Blockquote
        if stripped.startswith("> "):
            if in_ul:
                html_parts.append("</ul>")
                in_ul = False
            content = _inline_format(stripped[2:])
            html_parts.append(f"<blockquote>{content}</blockquote>")
            in_blockquote = True
            i += 1
            continue

        # Unordered list
        if stripped.startswith("- ") or stripped.startswith("* "):
            if not in_ul:
                in_ul = True
                html_parts.append("<ul>")
            content = _inline_format(stripped[2:])
            html_parts.append(f"<li>{content}</li>")
            i += 1
            continue

        # Regular paragraph
        if in_ul:
            html_parts.append("</ul>")
            in_ul = False

        content = _inline_format(stripped)
        html_parts.append(f"<p>{content}\n</p>")
        i += 1

    if in_ul:
        html_parts.append("</ul>")
    if in_table:
        _flush_table(html_parts, table_rows)

    return "\n".join(html_parts)


def _flush_table(html_parts, rows):
    """Convert collected table rows to HTML table."""
    if not rows:
        return
    html_parts.append("<table>")
    for idx, row in enumerate(rows):
        cells = [c.strip() for c in row.strip("|").split("|")]
        tag = "th" if idx == 0 else "td"
        row_html = "<tr>" + "".join(f"<{tag}>{_inline_format(c)}</{tag}>" for c in cells) + "</tr>"
        html_parts.append(row_html)
    html_parts.append("</table>")


def _inline_format(text: str) -> str:
    """Apply inline formatting: bold, italic."""
    # Bold: **text**
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    # Italic: *text*
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    return text


def main():
    # Read existing JS file
    with open(JS_FILE, "r", encoding="utf-8") as f:
        js_content = f.read()

    # Strip prefix and trailing semicolon to get JSON
    prefix = "chapterContent = "
    if not js_content.startswith(prefix):
        raise ValueError("File does not start with expected prefix")

    json_str = js_content[len(prefix):]
    if json_str.endswith(";"):
        json_str = json_str[:-1]

    data = json.loads(json_str)

    print(f"Existing entries: {len(data)}")

    # Process each chapter
    for ch in CHAPTERS:
        src_path = os.path.join(DRAFT_DIR, ch["src"])
        with open(src_path, "r", encoding="utf-8") as f:
            md_text = f.read()

        html = md_to_html(md_text)
        data[ch["key"]] = html
        print(f"Added: {ch['key']} ({len(html)} chars)")

    print(f"Total entries: {len(data)}")

    # Write back
    json_str = json.dumps(data, ensure_ascii=False)
    with open(JS_FILE, "w", encoding="utf-8") as f:
        f.write(prefix + json_str + ";")

    print("Done. File written.")


if __name__ == "__main__":
    main()
