#!/usr/bin/env python3
"""
Fix two factual errors throughout the trilogy:
1. Joan Rock is Sage's stepmother, not mother
2. The Blockheads are red, not yellow
"""

import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Replacement rules
# ---------------------------------------------------------------------------

def fix_yellow_blockheads(text):
    """Replace 'yellow' with 'red' only in Blockhead contexts (not Yellowstone)."""
    count = 0

    def replace_yellow(m):
        nonlocal count
        # Check surrounding context (200 chars) for Blockhead-related words
        start = max(0, m.start() - 200)
        end = min(len(text), m.end() + 200)
        context = text[start:end].lower()
        blockhead_words = ['blockhead', 'block', 'gumby', 'geometric', 'rigid',
                           'flat', 'angular', 'rectangular', 'figure']
        if any(w in context for w in blockhead_words):
            count += 1
            # Preserve case
            word = m.group(0)
            if word == 'Yellow':
                return 'Red'
            elif word == 'YELLOW':
                return 'RED'
            else:
                return 'red'
        return m.group(0)

    result = re.sub(r'(?i)\byellow\b(?!stone)', replace_yellow, text)
    return result, count


def fix_joan_mother(text):
    """Replace 'my mother' with 'my stepmother' when referring to Joan Rock."""
    count = 0

    # Specific patterns to fix (Joan-related only)
    patterns = [
        # "my mother, Joan" -> "my stepmother, Joan"
        (r'my mother, Joan', 'my stepmother, Joan'),
        (r'My mother, Joan', 'My stepmother, Joan'),
        # "my mother Joan" -> "my stepmother Joan"
        (r'my mother Joan', 'my stepmother Joan'),
        (r'My mother Joan', 'My stepmother Joan'),
        # "Joan Rock Clokey -- my mother --" -> "Joan Rock Clokey -- my stepmother --"
        (r'Joan Rock Clokey -- my mother --', 'Joan Rock Clokey -- my stepmother --'),
        (r'Joan Rock Clokey \u2014 my mother \u2014', 'Joan Rock Clokey \u2014 my stepmother \u2014'),
        # In HTML: em-dash variants
        (r'Joan Rock Clokey \u2013 my mother \u2013', 'Joan Rock Clokey \u2013 my stepmother \u2013'),
        # "He married my mother" -> "He married my stepmother"
        (r'He married my mother, Joan Rock', 'He married my stepmother, Joan Rock'),
        (r'He married my mother Joan Rock', 'He married my stepmother Joan Rock'),
        # "my mother was suddenly a widow" - contextual, Joan related
        (r'My mother was suddenly a widow', 'My stepmother was suddenly a widow'),
        (r'my mother was suddenly a widow', 'my stepmother was suddenly a widow'),
        # "that my mother was wrong"
        (r'that my mother was wrong', 'that my stepmother was wrong'),
    ]

    for old, new in patterns:
        occurrences = text.count(old)
        if occurrences > 0:
            text = text.replace(old, new)
            count += occurrences

    return text, count


def process_file(filepath):
    """Apply both fixes to a single file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    original = text
    text, yellow_count = fix_yellow_blockheads(text)
    text, joan_count = fix_joan_mother(text)

    total = yellow_count + joan_count
    if total > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        rel = os.path.relpath(filepath, BASE)
        print(f"  {rel}: {yellow_count} yellow->red, {joan_count} mother->stepmother")

    return yellow_count, joan_count


def main():
    total_yellow = 0
    total_joan = 0

    # Fix markdown drafts
    print("=== Fixing chapter_drafts/*.md ===")
    drafts_dir = os.path.join(BASE, "chapter_drafts")
    for fn in sorted(os.listdir(drafts_dir)):
        if fn.endswith('.md'):
            y, j = process_file(os.path.join(drafts_dir, fn))
            total_yellow += y
            total_joan += j

    # Fix chapters_content.json
    print("\n=== Fixing chapters_content.json ===")
    y, j = process_file(os.path.join(BASE, "chapters_content.json"))
    total_yellow += y
    total_joan += j

    # Fix chapters_content.js
    print("\n=== Fixing chapters_content.js ===")
    y, j = process_file(os.path.join(BASE, "chapters_content.js"))
    total_yellow += y
    total_joan += j

    # Fix any .md files in Book folders
    print("\n=== Fixing Book */*.md files ===")
    for root, dirs, files in os.walk(BASE):
        if 'chapter_drafts' in root or '.git' in root:
            continue
        for fn in sorted(files):
            if fn.endswith('.md'):
                y, j = process_file(os.path.join(root, fn))
                total_yellow += y
                total_joan += j

    print(f"\n=== TOTAL: {total_yellow} yellow->red, {total_joan} mother->stepmother ===")


if __name__ == "__main__":
    main()
