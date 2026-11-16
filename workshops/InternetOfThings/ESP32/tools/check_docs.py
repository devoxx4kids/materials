#!/usr/bin/env python3
"""Check the ESP32 workshop documentation.

Usage (from the workshop folder):
    python3 tools/check_docs.py [ROOT]

Checks that every en/ folder has fr/ and nl/ siblings with the same files, that local
Markdown links resolve (except in design/, the specs and plans), that no AsciiDoc files
exist, and that every mission has its kids' pages. Exit code 1 when a problem is found.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
LANGS = ("en", "fr", "nl")
MISSION_PAGES = ("mission.md", "bonus-cards.md")
LINK = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
EXTERNAL = ("http://", "https://", "mailto:", "#")
NOT_LINK_CHECKED = ("design",)  # specs and plans: their code blocks hold example links


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def file_names(folder: Path) -> set[str]:
    return {p.name for p in folder.iterdir() if p.is_file()}


def check_language_parity(root: Path) -> list[str]:
    problems = []
    for en in sorted(p for p in root.rglob("en") if p.is_dir()):
        expected = file_names(en)
        for lang in LANGS[1:]:
            folder = en.parent / lang
            if not folder.is_dir():
                problems.append(f"{rel(folder, root)}: folder missing")
                continue
            found = file_names(folder)
            problems += [f"{rel(folder, root)}: missing {n}" for n in sorted(expected - found)]
            problems += [f"{rel(folder, root)}: extra {n}" for n in sorted(found - expected)]
    return problems


def check_links(root: Path) -> list[str]:
    problems = []
    for page in sorted(root.rglob("*.md")):
        if page.relative_to(root).parts[0] in NOT_LINK_CHECKED:
            continue
        for target in LINK.findall(page.read_text(encoding="utf-8")):
            if target.startswith(EXTERNAL):
                continue
            path = unquote(target.split("#", 1)[0])
            if not (page.parent / path).exists():
                problems.append(f"{rel(page, root)}: broken link {target}")
    return problems


def check_no_asciidoc(root: Path) -> list[str]:
    found = sorted(p for p in root.rglob("*") if p.suffix in (".adoc", ".asciidoc"))
    return [f"{rel(p, root)}: AsciiDoc is not allowed, use Markdown" for p in found]


def check_mission_pages(root: Path) -> list[str]:
    problems = []
    for en in sorted((root / "missions").glob("*/en")):
        problems += [f"{rel(en, root)}: missing {n}" for n in MISSION_PAGES if not (en / n).is_file()]
    return problems


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    root = Path(args[0]).resolve() if args else ROOT
    problems = (
        check_language_parity(root)
        + check_links(root)
        + check_no_asciidoc(root)
        + check_mission_pages(root)
    )
    for problem in problems:
        print(problem)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
