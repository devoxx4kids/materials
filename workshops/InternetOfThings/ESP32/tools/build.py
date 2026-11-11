#!/usr/bin/env python3
"""Generate the per-language MicroBlocks files of the ESP32 workshop.

Usage (from the workshop folder):
    python3 tools/build.py          write all generated files
    python3 tools/build.py --check  exit 1 if a generated file is missing or out of date

Templates use {{key}} for a translated string from i18n/<lang>.json, and a line
{{> Name}} to inline a library: Core2Buttons (rendered from src/library) or a
vendored MicroBlocks library from vendor/<Name>.ubl.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LANGS = ("en", "fr", "nl")
REFERENCE_LANG = "en"
SCREEN_MAX = 26

KEY = re.compile(r"\{\{\s*([a-z0-9_.]+)\s*\}\}")
INCLUDE = re.compile(r"^\{\{>\s*([A-Za-z0-9 _-]+?)\s*\}\}$", re.MULTILINE)
SLOT = re.compile(r"(?<!\S)_(?!\S)")

LIBRARY_TEMPLATE = "src/library/Core2Buttons.ubl.tmpl"
LIBRARY_OUTPUT = "library/Core2Buttons-{lang}.ubl"
VENDORED = ("Tone", "ESP Now")

# (template, output pattern). Each mission task adds its starter and solution here.
PROJECTS: tuple[tuple[str, str], ...] = (
    ("src/projects/magic-ball-start.ubp.tmpl", "missions/01-magic-shake-ball/starter/magic-ball-start-{lang}.ubp"),
    ("src/projects/magic-ball-done.ubp.tmpl", "missions/01-magic-shake-ball/solution/magic-ball-done-{lang}.ubp"),
    ("src/projects/hot-potato-start.ubp.tmpl", "missions/02-hot-potato/starter/hot-potato-start-{lang}.ubp"),
    ("src/projects/hot-potato-done.ubp.tmpl", "missions/02-hot-potato/solution/hot-potato-done-{lang}.ubp"),
)


class BuildError(Exception):
    """A template or translation problem that stops the build."""


def escape(text: str) -> str:
    """Escape a value for use inside a single-quoted MicroBlocks string."""
    return text.replace("'", "''")


def render(template: str, strings: dict[str, str], includes: dict[str, str] | None = None) -> str:
    def key(match: re.Match) -> str:
        name = match.group(1)
        if name not in strings:
            raise BuildError(f"missing translation key: {name}")
        return escape(strings[name])

    def include(match: re.Match) -> str:
        name = match.group(1)
        if not includes or name not in includes:
            raise BuildError(f"unknown include: {name}")
        return includes[name].rstrip("\n")

    # Keys first, so included (already rendered) text is never rendered twice.
    return INCLUDE.sub(include, KEY.sub(key, template))


def slot_count(label: str) -> int:
    return len(SLOT.findall(label))


def check_strings(strings_by_lang: dict[str, dict[str, str]]) -> list[str]:
    reference = strings_by_lang[REFERENCE_LANG]
    problems = []
    for lang, strings in strings_by_lang.items():
        problems += [f"{lang}: missing key {k}" for k in reference if k not in strings]
        for k, value in strings.items():
            if k not in reference:
                problems.append(f"{lang}: unknown key {k}")
                continue
            if not value.strip():
                problems.append(f"{lang}: {k} is empty")
                continue
            if k.startswith("blk.") and slot_count(value) != slot_count(reference[k]):
                problems.append(
                    f"{lang}: {k} has {slot_count(value)} input slot(s), "
                    f"{REFERENCE_LANG} has {slot_count(reference[k])}"
                )
            if k.startswith("screen."):
                if not value.isascii():
                    problems.append(f"{lang}: {k} must be plain ASCII")
                if len(value) > SCREEN_MAX:
                    problems.append(f"{lang}: {k} is longer than {SCREEN_MAX} characters")
    return problems


def load_strings(root: Path) -> dict[str, dict[str, str]]:
    return {lang: json.loads((root / "i18n" / f"{lang}.json").read_text(encoding="utf-8")) for lang in LANGS}


def generate(root: Path = ROOT, projects=PROJECTS) -> dict[Path, str]:
    strings = load_strings(root)
    problems = check_strings(strings)
    if problems:
        raise BuildError("\n".join(problems))
    vendored = {name: (root / "vendor" / f"{name}.ubl").read_text(encoding="utf-8") for name in VENDORED}
    library_template = (root / LIBRARY_TEMPLATE).read_text(encoding="utf-8")
    files: dict[Path, str] = {}
    for lang in LANGS:
        library = render(library_template, strings[lang])
        files[root / LIBRARY_OUTPUT.format(lang=lang)] = library
        includes = {"Core2Buttons": library, **vendored}
        for template, output in projects:
            text = (root / template).read_text(encoding="utf-8")
            files[root / output.format(lang=lang)] = render(text, strings[lang], includes)
    return files


def build(root: Path = ROOT, projects=PROJECTS, check: bool = False) -> list[Path]:
    """Write the generated files; with check=True only list missing or stale ones."""
    changed = []
    for path, content in generate(root, projects).items():
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current == content:
            continue
        changed.append(path)
        if not check:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    return changed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="only report missing or stale files")
    args = parser.parse_args(argv)
    try:
        changed = build(check=args.check)
    except BuildError as error:
        print(error, file=sys.stderr)
        return 1
    prefix = "out of date: " if args.check else "wrote: "
    for path in changed:
        print(prefix + path.relative_to(ROOT).as_posix())
    return 1 if args.check and changed else 0


if __name__ == "__main__":
    sys.exit(main())
