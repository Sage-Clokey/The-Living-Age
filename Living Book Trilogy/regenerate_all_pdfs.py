#!/usr/bin/env python3
"""
Regenerate ALL chapter PDFs from markdown drafts.
Uses the same styling as the original build_and_renumber.py.
"""

import os
import markdown
from weasyprint import HTML

BASE = os.path.dirname(os.path.abspath(__file__))
DRAFTS = os.path.join(BASE, "chapter_drafts")

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

# Complete mapping: markdown draft -> (PDF path relative to BASE, book, part, chapter labels)
MAPPING = [
    # ===== BOOK I =====
    ("book1_prologue.md",
     "Book I - The Sagent Creed/Prologue/Prologue - Hello, This Is Sage.pdf",
     "Book I - The Sagent Creed", "Prologue", "Prologue - Hello, This Is Sage"),
    ("book1_ch01.md",
     "Book I - The Sagent Creed/Part 1 - The Name, the Nature, and the Calling/Chapter 01 - The First Job Was Gardener, Not King.pdf",
     "Book I - The Sagent Creed", "Part 1 - The Name, the Nature, and the Calling", "Chapter 01 - The First Job Was Gardener, Not King"),
    ("book1_ch02.md",
     "Book I - The Sagent Creed/Part 1 - The Name, the Nature, and the Calling/Chapter 02 - Surrender and Strength.pdf",
     "Book I - The Sagent Creed", "Part 1 - The Name, the Nature, and the Calling", "Chapter 02 - Surrender and Strength"),
    ("book1_ch03.md",
     "Book I - The Sagent Creed/Part 1 - The Name, the Nature, and the Calling/Chapter 03 - The Green Lightsaber.pdf",
     "Book I - The Sagent Creed", "Part 1 - The Name, the Nature, and the Calling", "Chapter 03 - The Green Lightsaber"),
    ("book1_ch04.md",
     "Book I - The Sagent Creed/Part 1 - The Name, the Nature, and the Calling/Chapter 04 - Dancing to Music No One Else Hears.pdf",
     "Book I - The Sagent Creed", "Part 1 - The Name, the Nature, and the Calling", "Chapter 04 - Dancing to Music No One Else Hears"),
    ("book1_ch05.md",
     "Book I - The Sagent Creed/Part 2 - The Shaken Jar/Chapter 05 - The Shaken Jar.pdf",
     "Book I - The Sagent Creed", "Part 2 - The Shaken Jar", "Chapter 05 - The Shaken Jar"),
    ("book1_ch06.md",
     "Book I - The Sagent Creed/Part 2 - The Shaken Jar/Chapter 06 - The Hidden War.pdf",
     "Book I - The Sagent Creed", "Part 2 - The Shaken Jar", "Chapter 06 - The Hidden War"),
    ("book1_ch07.md",
     "Book I - The Sagent Creed/Part 2 - The Shaken Jar/Chapter 07 - The Thornbush King.pdf",
     "Book I - The Sagent Creed", "Part 2 - The Shaken Jar", "Chapter 07 - The Thornbush King"),
    ("book1_ch08.md",
     "Book I - The Sagent Creed/Part 2 - The Shaken Jar/Chapter 08 - The King They Asked For.pdf",
     "Book I - The Sagent Creed", "Part 2 - The Shaken Jar", "Chapter 08 - The King They Asked For"),
    ("book1_ch09.md",
     "Book I - The Sagent Creed/Part 3 - The Architecture of a Free Conscience/Chapter 09 - No Chain of Command Between Humans.pdf",
     "Book I - The Sagent Creed", "Part 3 - The Architecture of a Free Conscience", "Chapter 09 - No Chain of Command Between Humans"),
    ("book1_ch10.md",
     "Book I - The Sagent Creed/Part 3 - The Architecture of a Free Conscience/Chapter 10 - Persuasion Over Force.pdf",
     "Book I - The Sagent Creed", "Part 3 - The Architecture of a Free Conscience", "Chapter 10 - Persuasion Over Force"),
    ("book1_ch11.md",
     "Book I - The Sagent Creed/Part 3 - The Architecture of a Free Conscience/Chapter 11 - The Builder and the Pink Cow.pdf",
     "Book I - The Sagent Creed", "Part 3 - The Architecture of a Free Conscience", "Chapter 11 - The Builder and the Pink Cow"),
    ("book1_ch12.md",
     "Book I - The Sagent Creed/Part 3 - The Architecture of a Free Conscience/Chapter 12 - Principled Love.pdf",
     "Book I - The Sagent Creed", "Part 3 - The Architecture of a Free Conscience", "Chapter 12 - Principled Love"),
    ("book1_ch13.md",
     "Book I - The Sagent Creed/Part 3 - The Architecture of a Free Conscience/Chapter 13 - Power as Stewardship.pdf",
     "Book I - The Sagent Creed", "Part 3 - The Architecture of a Free Conscience", "Chapter 13 - Power as Stewardship"),
    ("book1_ch14.md",
     "Book I - The Sagent Creed/Part 4 - The Fibonacci Spiral Through the Generations/Chapter 14 - The Seed Over Sword.pdf",
     "Book I - The Sagent Creed", "Part 4 - The Fibonacci Spiral Through the Generations", "Chapter 14 - The Seed Over Sword"),
    ("book1_ch15.md",
     "Book I - The Sagent Creed/Part 4 - The Fibonacci Spiral Through the Generations/Chapter 15 - The Names That Wrote Themselves.pdf",
     "Book I - The Sagent Creed", "Part 4 - The Fibonacci Spiral Through the Generations", "Chapter 15 - The Names That Wrote Themselves"),
    ("book1_ch16.md",
     "Book I - The Sagent Creed/Part 4 - The Fibonacci Spiral Through the Generations/Chapter 16 - Art and the Green Knight.pdf",
     "Book I - The Sagent Creed", "Part 4 - The Fibonacci Spiral Through the Generations", "Chapter 16 - Art and the Green Knight"),
    ("book1_ch17.md",
     "Book I - The Sagent Creed/Part 4 - The Fibonacci Spiral Through the Generations/Chapter 17 - Joe and the Storm.pdf",
     "Book I - The Sagent Creed", "Part 4 - The Fibonacci Spiral Through the Generations", "Chapter 17 - Joe and the Storm"),
    ("book1_ch18.md",
     "Book I - The Sagent Creed/Part 4 - The Fibonacci Spiral Through the Generations/Chapter 18 - The Storm Spreads the Seeds.pdf",
     "Book I - The Sagent Creed", "Part 4 - The Fibonacci Spiral Through the Generations", "Chapter 18 - The Storm Spreads the Seeds"),
    # Note: Chapter 19 (Gumby and the Cartel) is NOT in the JSON — it was removed/restructured
    ("book1_ch20.md",
     "Book I - The Sagent Creed/Part 5 - Sheep Among Wolves/Chapter 20 - The Enemy That Feeds on Conflict.pdf",
     "Book I - The Sagent Creed", "Part 5 - Sheep Among Wolves", "Chapter 20 - The Enemy That Feeds on Conflict"),
    ("book1_ch21.md",
     "Book I - The Sagent Creed/Part 5 - Sheep Among Wolves/Chapter 21 - Roots, Not Branches.pdf",
     "Book I - The Sagent Creed", "Part 5 - Sheep Among Wolves", "Chapter 21 - Roots, Not Branches"),
    ("book1_ch22.md",
     "Book I - The Sagent Creed/Part 5 - Sheep Among Wolves/Chapter 22 - The Blue to the Green.pdf",
     "Book I - The Sagent Creed", "Part 5 - Sheep Among Wolves", "Chapter 22 - The Blue to the Green"),
    ("book1_ch23.md",
     "Book I - The Sagent Creed/Part 5 - Sheep Among Wolves/Chapter 23 - The Sagent Narrative.pdf",
     "Book I - The Sagent Creed", "Part 5 - Sheep Among Wolves", "Chapter 23 - The Sagent Narrative"),

    # ===== BOOK II =====
    ("book2_prologue.md",
     "Book II - The Spiral and the Block/Prologue/Prologue - The Stories Already Know.pdf",
     "Book II - The Spiral and the Block", "Prologue", "Prologue - The Stories Already Know"),
    ("book2_ch01.md",
     "Book II - The Spiral and the Block/Part 1 - The True Republic/Chapter 01 - Why Empires Always Collapse.pdf",
     "Book II - The Spiral and the Block", "Part 1 - The True Republic", "Chapter 01 - Why Empires Always Collapse"),
    ("book2_ch02.md",
     "Book II - The Spiral and the Block/Part 1 - The True Republic/Chapter 02 - The Spiral vs the Block.pdf",
     "Book II - The Spiral and the Block", "Part 1 - The True Republic", "Chapter 02 - The Spiral vs the Block"),
    ("book2_ch03.md",
     "Book II - The Spiral and the Block/Part 1 - The True Republic/Chapter 03 - Civilization Is a Living System.pdf",
     "Book II - The Spiral and the Block", "Part 1 - The True Republic", "Chapter 03 - Civilization Is a Living System"),
    ("book2_ch04.md",
     "Book II - The Spiral and the Block/Part 1 - The True Republic/Chapter 04 - Is Government Authority Real.pdf",
     "Book II - The Spiral and the Block", "Part 1 - The True Republic", "Chapter 04 - Is Government Authority Real"),
    ("book2_ch05.md",
     "Book II - The Spiral and the Block/Part 1 - The True Republic/Chapter 05 - Who Owns Your Life.pdf",
     "Book II - The Spiral and the Block", "Part 1 - The True Republic", "Chapter 05 - Who Owns Your Life"),
    ("book2_ch06.md",
     "Book II - The Spiral and the Block/Part 1 - The True Republic/Chapter 06 - Would Society Collapse Without Government.pdf",
     "Book II - The Spiral and the Block", "Part 1 - The True Republic", "Chapter 06 - Would Society Collapse Without Government"),
    ("book2_ch07.md",
     "Book II - The Spiral and the Block/Part 1 - The True Republic/Chapter 07 - Do Laws Create Morality.pdf",
     "Book II - The Spiral and the Block", "Part 1 - The True Republic", "Chapter 07 - Do Laws Create Morality"),
    ("book2_ch08.md",
     "Book II - The Spiral and the Block/Part 1 - The True Republic/Chapter 08 - What Is a True Republic.pdf",
     "Book II - The Spiral and the Block", "Part 1 - The True Republic", "Chapter 08 - What Is a True Republic"),
    ("book2_ch09.md",
     "Book II - The Spiral and the Block/Part 1 - The True Republic/Chapter 09 - Where Does Law Come From.pdf",
     "Book II - The Spiral and the Block", "Part 1 - The True Republic", "Chapter 09 - Where Does Law Come From"),
    ("book2_ch10.md",
     "Book II - The Spiral and the Block/Part 2 - The Mythology of Media/Chapter 10 - Star Wars - The Backwards Fibonacci Spiral.pdf",
     "Book II - The Spiral and the Block", "Part 2 - The Mythology of Media", "Chapter 10 - Star Wars - The Backwards Fibonacci Spiral"),
    ("book2_ch11.md",
     "Book II - The Spiral and the Block/Part 2 - The Mythology of Media/Chapter 11 - The Three Skywalkers.pdf",
     "Book II - The Spiral and the Block", "Part 2 - The Mythology of Media", "Chapter 11 - The Three Skywalkers"),
    ("book2_ch12.md",
     "Book II - The Spiral and the Block/Part 2 - The Mythology of Media/Chapter 12 - Luke and the Will of the Force.pdf",
     "Book II - The Spiral and the Block", "Part 2 - The Mythology of Media", "Chapter 12 - Luke and the Will of the Force"),
    ("maul_shadow_lord.md",
     "Book II - The Spiral and the Block/Part 2 - The Mythology of Media/Chapter 13 - Maul the Shadow Lord.pdf",
     "Book II - The Spiral and the Block", "Part 2 - The Mythology of Media", "Chapter 13 - Maul the Shadow Lord"),
    ("book2_ch14.md",
     "Book II - The Spiral and the Block/Part 2 - The Mythology of Media/Chapter 14 - The Force Dyad and the Scattered Temple.pdf",
     "Book II - The Spiral and the Block", "Part 2 - The Mythology of Media", "Chapter 14 - The Force Dyad and the Scattered Temple"),
    ("book2_ch15.md",
     "Book II - The Spiral and the Block/Part 2 - The Mythology of Media/Chapter 15 - Unshake the Jar.pdf",
     "Book II - The Spiral and the Block", "Part 2 - The Mythology of Media", "Chapter 15 - Unshake the Jar"),
    ("book2_ch16.md",
     "Book II - The Spiral and the Block/Part 2 - The Mythology of Media/Chapter 16 - Avatar - Balance vs Domination.pdf",
     "Book II - The Spiral and the Block", "Part 2 - The Mythology of Media", "Chapter 16 - Avatar - Balance vs Domination"),
    ("book2_ch17.md",
     "Book II - The Spiral and the Block/Part 2 - The Mythology of Media/Chapter 17 - The Green Flame.pdf",
     "Book II - The Spiral and the Block", "Part 2 - The Mythology of Media", "Chapter 17 - The Green Flame"),
    ("neutral_jing.md",
     "Book II - The Spiral and the Block/Part 2 - The Mythology of Media/Chapter 18 - Neutral Jing.pdf",
     "Book II - The Spiral and the Block", "Part 2 - The Mythology of Media", "Chapter 18 - Neutral Jing"),
    ("book2_ch19.md",
     "Book II - The Spiral and the Block/Part 2 - The Mythology of Media/Chapter 19 - Lord of the Rings - The Ring of Centralized Power.pdf",
     "Book II - The Spiral and the Block", "Part 2 - The Mythology of Media", "Chapter 19 - Lord of the Rings - The Ring of Centralized Power"),
    ("book2_ch20.md",
     "Book II - The Spiral and the Block/Part 2 - The Mythology of Media/Chapter 20 - The Hobbit and the Shire.pdf",
     "Book II - The Spiral and the Block", "Part 2 - The Mythology of Media", "Chapter 20 - The Hobbit and the Shire"),
    ("book2_ch21.md",
     "Book II - The Spiral and the Block/Part 2 - The Mythology of Media/Chapter 21 - Loki - The Sacred Trickster.pdf",
     "Book II - The Spiral and the Block", "Part 2 - The Mythology of Media", "Chapter 21 - Loki - The Sacred Trickster"),
    ("book2_ch22.md",
     "Book II - The Spiral and the Block/Part 2 - The Mythology of Media/Chapter 22 - Thor and Asgard - The Fall of Arrogant Gods.pdf",
     "Book II - The Spiral and the Block", "Part 2 - The Mythology of Media", "Chapter 22 - Thor and Asgard - The Fall of Arrogant Gods"),
    ("book2_ch23.md",
     "Book II - The Spiral and the Block/Part 2 - The Mythology of Media/Chapter 23 - Ragnarok, Arthur, and the Green Return.pdf",
     "Book II - The Spiral and the Block", "Part 2 - The Mythology of Media", "Chapter 23 - Ragnarok, Arthur, and the Green Return"),
    ("book2_ch24.md",
     "Book II - The Spiral and the Block/Part 2 - The Mythology of Media/Chapter 24 - The Matrix - The Architecture of Control.pdf",
     "Book II - The Spiral and the Block", "Part 2 - The Mythology of Media", "Chapter 24 - The Matrix - The Architecture of Control"),
    ("book2_ch25.md",
     "Book II - The Spiral and the Block/Part 2 - The Mythology of Media/Chapter 25 - Nothing Is True, Everything Is Permitted.pdf",
     "Book II - The Spiral and the Block", "Part 2 - The Mythology of Media", "Chapter 25 - Nothing Is True, Everything Is Permitted"),
    ("book2_ch26.md",
     "Book II - The Spiral and the Block/Part 2 - The Mythology of Media/Chapter 26 - The Sokovia Problem.pdf",
     "Book II - The Spiral and the Block", "Part 2 - The Mythology of Media", "Chapter 26 - The Sokovia Problem"),
    ("book2_ch27.md",
     "Book II - The Spiral and the Block/Part 3 - The Eight Pillars/Chapter 26 - Pillar I - Life Is Decentralized.pdf",
     "Book II - The Spiral and the Block", "Part 3 - The Eight Pillars", "Chapter 26 - Pillar I - Life Is Decentralized"),
    ("book2_ch28.md",
     "Book II - The Spiral and the Block/Part 3 - The Eight Pillars/Chapter 27 - Pillar II - Truth Emerges from Individuals.pdf",
     "Book II - The Spiral and the Block", "Part 3 - The Eight Pillars", "Chapter 27 - Pillar II - Truth Emerges from Individuals"),
    ("book2_ch29.md",
     "Book II - The Spiral and the Block/Part 3 - The Eight Pillars/Chapter 28 - Pillar III - Power Corrupts Centralized Systems.pdf",
     "Book II - The Spiral and the Block", "Part 3 - The Eight Pillars", "Chapter 28 - Pillar III - Power Corrupts Centralized Systems"),
    ("book2_ch30.md",
     "Book II - The Spiral and the Block/Part 3 - The Eight Pillars/Chapter 29 - Pillar IV - Voluntary Cooperation Is Natural.pdf",
     "Book II - The Spiral and the Block", "Part 3 - The Eight Pillars", "Chapter 29 - Pillar IV - Voluntary Cooperation Is Natural"),
    ("book2_ch31.md",
     "Book II - The Spiral and the Block/Part 3 - The Eight Pillars/Chapter 30 - Pillar V - Wisdom Transcends Authority.pdf",
     "Book II - The Spiral and the Block", "Part 3 - The Eight Pillars", "Chapter 30 - Pillar V - Wisdom Transcends Authority"),
    ("book2_ch32.md",
     "Book II - The Spiral and the Block/Part 3 - The Eight Pillars/Chapter 31 - Pillar VI - Stories Shape Civilizations.pdf",
     "Book II - The Spiral and the Block", "Part 3 - The Eight Pillars", "Chapter 31 - Pillar VI - Stories Shape Civilizations"),
    ("book2_ch33.md",
     "Book II - The Spiral and the Block/Part 3 - The Eight Pillars/Chapter 32 - Pillar VII - The Individual Is Sacred.pdf",
     "Book II - The Spiral and the Block", "Part 3 - The Eight Pillars", "Chapter 32 - Pillar VII - The Individual Is Sacred"),
    ("book2_ch34.md",
     "Book II - The Spiral and the Block/Part 3 - The Eight Pillars/Chapter 33 - Pillar VIII - The Spiral Is the Pattern of Life.pdf",
     "Book II - The Spiral and the Block", "Part 3 - The Eight Pillars", "Chapter 33 - Pillar VIII - The Spiral Is the Pattern of Life"),
    ("book2_ch18.md",
     "Book II - The Spiral and the Block/Part 4 - The Perfect Agent/Chapter 34 - The Perfect Agent - Bible and Quran.pdf",
     "Book II - The Spiral and the Block", "Part 4 - The Perfect Agent", "Chapter 34 - The Perfect Agent - Bible and Quran"),
    ("book2_ch13.md",
     "Book II - The Spiral and the Block/Part 4 - The Perfect Agent/Chapter 35 - The Skywalker Spiral.pdf",
     "Book II - The Spiral and the Block", "Part 4 - The Perfect Agent", "Chapter 35 - The Skywalker Spiral"),

    # ===== BOOK III =====
    ("book3_prologue.md",
     "Book III - The Spiral Steward/Prologue/Prologue - A Note Before the First Word.pdf",
     "Book III - The Spiral Steward", "Prologue", "Prologue - A Note Before the First Word"),
    ("book3_ch01.md",
     "Book III - The Spiral Steward/Part 1 - The Industrial Error and the Living Age/Chapter 01 - The Industrial Error.pdf",
     "Book III - The Spiral Steward", "Part 1 - The Industrial Error and the Living Age", "Chapter 01 - The Industrial Error"),
    ("book3_ch02.md",
     "Book III - The Spiral Steward/Part 1 - The Industrial Error and the Living Age/Chapter 02 - The Men Who Made People Into Parts.pdf",
     "Book III - The Spiral Steward", "Part 1 - The Industrial Error and the Living Age", "Chapter 02 - The Men Who Made People Into Parts"),
    ("book3_ch03.md",
     "Book III - The Spiral Steward/Part 1 - The Industrial Error and the Living Age/Chapter 03 - The Death Pledge and the Cabin.pdf",
     "Book III - The Spiral Steward", "Part 1 - The Industrial Error and the Living Age", "Chapter 03 - The Death Pledge and the Cabin"),
    ("book3_ch04.md",
     "Book III - The Spiral Steward/Part 1 - The Industrial Error and the Living Age/Chapter 04 - Life Is Not a Machine.pdf",
     "Book III - The Spiral Steward", "Part 1 - The Industrial Error and the Living Age", "Chapter 04 - Life Is Not a Machine"),
    ("book3_ch05.md",
     "Book III - The Spiral Steward/Part 1 - The Industrial Error and the Living Age/Chapter 05 - The Wild Is the Place of True Order.pdf",
     "Book III - The Spiral Steward", "Part 1 - The Industrial Error and the Living Age", "Chapter 05 - The Wild Is the Place of True Order"),
    ("book3_ch06.md",
     "Book III - The Spiral Steward/Part 1 - The Industrial Error and the Living Age/Chapter 06 - The Necessary Death.pdf",
     "Book III - The Spiral Steward", "Part 1 - The Industrial Error and the Living Age", "Chapter 06 - The Necessary Death"),
    ("book3_ch07.md",
     "Book III - The Spiral Steward/Part 1 - The Industrial Error and the Living Age/Chapter 07 - The Green Flame - A Declaration.pdf",
     "Book III - The Spiral Steward", "Part 1 - The Industrial Error and the Living Age", "Chapter 07 - The Green Flame - A Declaration"),
    ("book3_ch08.md",
     "Book III - The Spiral Steward/Part 2 - Austrian Economics Meets Molecular Biology/Chapter 08 - Spontaneous Order in the Cell.pdf",
     "Book III - The Spiral Steward", "Part 2 - Austrian Economics Meets Molecular Biology", "Chapter 08 - Spontaneous Order in the Cell"),
    ("book3_ch09.md",
     "Book III - The Spiral Steward/Part 2 - Austrian Economics Meets Molecular Biology/Chapter 09 - The Knowledge Problem Is Biological.pdf",
     "Book III - The Spiral Steward", "Part 2 - Austrian Economics Meets Molecular Biology", "Chapter 09 - The Knowledge Problem Is Biological"),
    ("book3_ch10.md",
     "Book III - The Spiral Steward/Part 2 - Austrian Economics Meets Molecular Biology/Chapter 10 - Your Cells Dont Have a King.pdf",
     "Book III - The Spiral Steward", "Part 2 - Austrian Economics Meets Molecular Biology", "Chapter 10 - Your Cells Dont Have a King"),
    ("book3_ch11.md",
     "Book III - The Spiral Steward/Part 2 - Austrian Economics Meets Molecular Biology/Chapter 11 - The Entrepreneur and the Central Planner in Biology.pdf",
     "Book III - The Spiral Steward", "Part 2 - Austrian Economics Meets Molecular Biology", "Chapter 11 - The Entrepreneur and the Central Planner in Biology"),
    ("book3_ch12.md",
     "Book III - The Spiral Steward/Part 2 - Austrian Economics Meets Molecular Biology/Chapter 12 - The Disease Is the State.pdf",
     "Book III - The Spiral Steward", "Part 2 - Austrian Economics Meets Molecular Biology", "Chapter 12 - The Disease Is the State"),
    ("book3_ch13.md",
     "Book III - The Spiral Steward/Part 2 - Austrian Economics Meets Molecular Biology/Chapter 13 - Diversity Is Functional.pdf",
     "Book III - The Spiral Steward", "Part 2 - Austrian Economics Meets Molecular Biology", "Chapter 13 - Diversity Is Functional"),
    ("book3_ch14.md",
     "Book III - The Spiral Steward/Part 2 - Austrian Economics Meets Molecular Biology/Chapter 14 - The Genome of Liberty.pdf",
     "Book III - The Spiral Steward", "Part 2 - Austrian Economics Meets Molecular Biology", "Chapter 14 - The Genome of Liberty"),
    ("book3_ch15.md",
     "Book III - The Spiral Steward/Part 3 - How a Forest Becomes a Forest/Chapter 15 - How a Forest Becomes a Forest.pdf",
     "Book III - The Spiral Steward", "Part 3 - How a Forest Becomes a Forest", "Chapter 15 - How a Forest Becomes a Forest"),
    ("book3_ch16.md",
     "Book III - The Spiral Steward/Part 3 - How a Forest Becomes a Forest/Chapter 16 - The Storm and the Seeds.pdf",
     "Book III - The Spiral Steward", "Part 3 - How a Forest Becomes a Forest", "Chapter 16 - The Storm and the Seeds"),
    ("book3_ch17.md",
     "Book III - The Spiral Steward/Part 3 - How a Forest Becomes a Forest/Chapter 17 - What Bioinformatics Taught Me About Freedom.pdf",
     "Book III - The Spiral Steward", "Part 3 - How a Forest Becomes a Forest", "Chapter 17 - What Bioinformatics Taught Me About Freedom"),
    ("book3_ch18.md",
     "Book III - The Spiral Steward/Part 3 - How a Forest Becomes a Forest/Chapter 18 - Bioinformatics as Stewardship of Living Order.pdf",
     "Book III - The Spiral Steward", "Part 3 - How a Forest Becomes a Forest", "Chapter 18 - Bioinformatics as Stewardship of Living Order"),
    ("book3_ch19.md",
     "Book III - The Spiral Steward/Part 4 - Living Algorithms/Chapter 19 - Living Algorithms.pdf",
     "Book III - The Spiral Steward", "Part 4 - Living Algorithms", "Chapter 19 - Living Algorithms"),
    ("book3_ch20.md",
     "Book III - The Spiral Steward/Part 4 - Living Algorithms/Chapter 20 - Why Genome Browsers Are Hard to Use.pdf",
     "Book III - The Spiral Steward", "Part 4 - Living Algorithms", "Chapter 20 - Why Genome Browsers Are Hard to Use"),
    ("book3_ch21.md",
     "Book III - The Spiral Steward/Part 4 - Living Algorithms/Chapter 21 - Evolution as Gods Proactive Creation.pdf",
     "Book III - The Spiral Steward", "Part 4 - Living Algorithms", "Chapter 21 - Evolution as Gods Proactive Creation"),
    ("book3_ch22.md",
     "Book III - The Spiral Steward/Part 4 - Living Algorithms/Chapter 22 - The Immune Economy and the Fatal Syringe.pdf",
     "Book III - The Spiral Steward", "Part 4 - Living Algorithms", "Chapter 22 - The Immune Economy and the Fatal Syringe"),
    ("book3_ch23.md",
     "Book III - The Spiral Steward/Part 4 - Living Algorithms/Chapter 23 - The Fatal Conceit of Biology.pdf",
     "Book III - The Spiral Steward", "Part 4 - Living Algorithms", "Chapter 23 - The Fatal Conceit of Biology"),
    ("book3_ch24.md",
     "Book III - The Spiral Steward/Part 5 - LivingWorks - The Tool/Chapter 24 - The Spiral Steward - A New Role.pdf",
     "Book III - The Spiral Steward", "Part 5 - LivingWorks - The Tool", "Chapter 24 - The Spiral Steward - A New Role"),
    ("book3_ch25.md",
     "Book III - The Spiral Steward/Part 5 - LivingWorks - The Tool/Chapter 25 - LivingWorks - The CAD System for the Living Age.pdf",
     "Book III - The Spiral Steward", "Part 5 - LivingWorks - The Tool", "Chapter 25 - LivingWorks - The CAD System for the Living Age"),
    ("book3_epilogue.md",
     "Book III - The Spiral Steward/Epilogue/Epilogue - The Living Age.pdf",
     "Book III - The Spiral Steward", "Epilogue", "Epilogue - The Living Age"),

    # ===== APPENDICES =====
    ("appendix_b.md",
     "Appendices/Appendix B - Parallel Cases.pdf",
     "Appendices", "", "Appendix B - Parallel Cases"),
    ("appendix_c.md",
     "Appendices/Appendix C - The Sagent Creed (Unabridged).pdf",
     "Appendices", "", "Appendix C - The Sagent Creed (Unabridged)"),
    ("appendix_d.md",
     "Appendices/Appendix D - Spirals and Squares - The Visual Language.pdf",
     "Appendices", "", "Appendix D - Spirals and Squares - The Visual Language"),
]


def md_to_pdf(md_path, pdf_path, book_label, part_label, chapter_label):
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    html_body = markdown.markdown(md_text, extensions=["tables", "smarty"])

    parts = [book_label]
    if part_label:
        parts.append(part_label)
    parts.append(chapter_label)
    header = f'<div class="header-meta">{"<br>".join(parts)}</div>'

    full_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>{CSS}</style></head>
<body>{header}{html_body}</body></html>"""

    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    HTML(string=full_html).write_pdf(pdf_path)


def main():
    os.chdir(BASE)
    total = len(MAPPING)
    success = 0
    errors = []

    for i, (md_file, pdf_rel, book, part, chapter) in enumerate(MAPPING, 1):
        md_path = os.path.join(DRAFTS, md_file)
        pdf_path = os.path.join(BASE, pdf_rel)

        if not os.path.exists(md_path):
            errors.append(f"Source not found: {md_file}")
            print(f"  [{i}/{total}] SKIP (no source): {md_file}")
            continue

        try:
            md_to_pdf(md_path, pdf_path, book, part, chapter)
            success += 1
            print(f"  [{i}/{total}] OK: {pdf_rel}")
        except Exception as e:
            errors.append(f"{md_file}: {e}")
            print(f"  [{i}/{total}] ERROR: {md_file}: {e}")

    print(f"\n=== Done: {success}/{total} PDFs generated ===")
    if errors:
        print(f"Errors ({len(errors)}):")
        for e in errors:
            print(f"  {e}")


if __name__ == "__main__":
    main()
