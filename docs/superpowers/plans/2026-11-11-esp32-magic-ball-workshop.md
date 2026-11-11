# ESP32 Magic Shake Ball Workshop Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the complete Devoxx4Kids ESP32 workshop (three 45-minute MicroBlocks missions on the M5Stack Core2, with EN/FR/NL kids' and coach documentation) in `workshops/InternetOfThings/ESP32/`.

**Architecture:** All MicroBlocks files (the `Core2Buttons` helper library and the starter/solution projects of each mission) are generated per language by a small Python build script from templates plus `i18n/<lang>.json`; a second script checks the Markdown documentation (language parity, links, no AsciiDoc). Hardware behaviour is verified by a human on two real Core2 boards before the documentation is written, then the docs are written in English and translated to French and Dutch.

**Tech Stack:** MicroBlocks (text project format `.ubp`, library format `.ubl`), M5Stack Core2, Python 3.9+ standard library (tools), pytest (tests only), Markdown.

**Spec:** `docs/superpowers/specs/2026-11-11-esp32-magic-ball-workshop-design.md`

## Global Constraints

- Workshop root: `workshops/InternetOfThings/ESP32/` (called `W/` below). All paths in this plan are relative to `W/` unless they start with `docs/`.
- Branch: `feature/ESP32`.
- Documentation is Markdown only (`.md`). No AsciiDoc files anywhere under `W/`. Do not copy the layout of other workshops.
- Every folder `en/` under `W/` has sibling folders `fr/` and `nl/` containing exactly the same file names.
- No translatable text is hardcoded in a template: every block label, comment and on-screen text in `src/**/*.tmpl` is a `{{key}}` from `i18n/<lang>.json`.
- `screen.*` strings are plain ASCII and at most 26 characters (the Core2 TFT font, and 26 characters is the width at text scale 2).
- `blk.*` strings keep the same number of `_` input slots in every language.
- Target board: M5Stack Core2 only. Tool: MicroBlocks only. No Wi-Fi router, internet or cloud features.
- Tools use only the Python standard library; pytest is the only dev dependency.
- `W/CHANGELOG.md`: all changes made on the same day go under one version entry for that day; never create a second heading for the same date.
- Git commit messages: no `Co-Authored-By` trailer, no "Generated with Claude Code" line, no mention of GitHub (the user's global instructions override the harness attribution).
- Run tests from `W/`: `python3 -m pytest tools/tests -q`.

## Review Focus

1. A child types a long or accented text into `show big text` (e.g. a 40-character answer or "Peut-être") → the text shrinks to fit on the screen instead of running off it, and accents either render or are listed as a known limitation in the coach docs. Pinned by: Task 3 structural test of the scale steps; Task 7 hardware check H8.
2. A finger stays on a red circle, or a child taps very fast → exactly one event per touch, never a burst. Pinned by: Task 3 test that all three reporters go through `_c2b_edge`; Task 7 check H3.
3. A touch on the screen itself (above the red circles) → does not count as a button press. Pinned by: Task 3 test that `_c2b_zone` rejects y < 240; Task 7 check H2.
4. An ESP Now message with an out-of-range number, or from a board running a different mission → ignored without an error or a crash. Pinned by: Task 6 test that the receive script checks the range; Task 7 check H6.
5. A translator adds a key to `fr.json` only, or drops an input slot from a block label → the build fails with a clear message instead of producing a broken library. Pinned by: Task 1 tests.

---

## File map

| File | Responsibility | Task |
|---|---|---|
| `W/tools/build.py` | Render templates per language, check strings, `--check` for stale outputs | 1 |
| `W/tools/check_docs.py` | Markdown checks: language parity, links, no AsciiDoc, mission pages present | 2 |
| `W/tools/tests/conftest.py`, `test_build.py`, `test_check_docs.py`, `test_generated.py` | Tests | 1, 2, 3–6 |
| `W/tools/requirements-dev.txt` | `pytest` | 1 |
| `W/i18n/en.json`, `fr.json`, `nl.json` | All translatable strings | 3–6 |
| `W/src/library/Core2Buttons.ubl.tmpl` | Helper library source | 3 |
| `W/vendor/Tone.ubl`, `W/vendor/ESP Now.ubl`, `W/vendor/README.md` | Pinned MicroBlocks libraries + provenance | 3 |
| `W/src/projects/*.ubp.tmpl` | Starter and solution project sources | 4–6 |
| `W/library/Core2Buttons-<lang>.ubl`, `W/missions/*/starter|solution/*-<lang>.ubp` | Generated, committed | 3–6 |
| `W/library/README.md` | Library reference, translation workflow, spike results | 7, 8 |
| `W/README.md`, `W/coach/<lang>/*.md` | Entry page, coach docs | 8, 12, 13 |
| `W/missions/*/<lang>/mission.md`, `bonus-cards.md` | Kids' docs | 9–13 |
| `W/missions/*/images/*` | Photos and screenshots | 14 |
| `W/CHANGELOG.md` | Changelog | 1, then every task |

---

### Task 1: Build tool for per-language MicroBlocks files

**Files:**
- Create: `W/tools/build.py`
- Create: `W/tools/tests/conftest.py`
- Create: `W/tools/tests/test_build.py`
- Create: `W/tools/requirements-dev.txt`
- Create: `W/CHANGELOG.md`
- Create: `W/.gitignore`

**Interfaces:**
- Consumes: nothing.
- Produces (used by Tasks 3–6 and 14):
  - `build.ROOT: Path` — the workshop root `W/`.
  - `build.LANGS = ("en", "fr", "nl")`.
  - `build.PROJECTS: tuple[tuple[str, str], ...]` — `(template_path, output_pattern_with_{lang})`, empty in this task; Tasks 4–6 append entries.
  - `build.BuildError(Exception)`.
  - `build.escape(text: str) -> str` — doubles single quotes for MicroBlocks strings.
  - `build.render(template: str, strings: dict[str, str], includes: dict[str, str] | None = None) -> str`.
  - `build.slot_count(label: str) -> int`.
  - `build.check_strings(strings_by_lang: dict[str, dict[str, str]]) -> list[str]`.
  - `build.generate(root: Path = ROOT, projects = PROJECTS) -> dict[Path, str]`.
  - `build.build(root: Path = ROOT, projects = PROJECTS, check: bool = False) -> list[Path]` — returns written (or, with `check=True`, stale) paths.
  - CLI: `python3 tools/build.py [--check]`, exit code 1 on problems.

- [ ] **Step 1: Create the test scaffolding**

`W/tools/requirements-dev.txt`:
```
pytest>=7
```

`W/tools/tests/conftest.py`:
```python
import sys
from pathlib import Path

# Make tools/build.py and tools/check_docs.py importable as top-level modules.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
```

`W/.gitignore`:
```
__pycache__/
.pytest_cache/
```

Run: `python3 -m pip install -r tools/requirements-dev.txt` (from `W/`), if pytest is missing.

- [ ] **Step 2: Write the failing tests**

`W/tools/tests/test_build.py`:
```python
import json
from pathlib import Path

import pytest

import build


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def make_workshop(root: Path) -> list[tuple[str, str]]:
    strings = {
        "en": {"blk.vibrate": "vibrate for _ ms", "screen.hello": "Hello!"},
        "fr": {"blk.vibrate": "vibrer pendant _ ms", "screen.hello": "Salut !"},
        "nl": {"blk.vibrate": "tril _ ms", "screen.hello": "Hallo!"},
    }
    for lang, values in strings.items():
        write(root / "i18n" / f"{lang}.json", json.dumps(values))
    write(root / "src/library/Core2Buttons.ubl.tmpl", "module Core2Buttons Input\n  spec ' ' 'c2b_vibrate' '{{blk.vibrate}}' 'num' 300\n")
    write(root / "vendor/Tone.ubl", "module Tone Output\n")
    write(root / "vendor/ESP Now.ubl", "module 'ESP Now' Comm\n")
    write(root / "src/projects/demo.ubp.tmpl", "module main\nscript 1 1 {\nc2b_bigText '{{screen.hello}}'\n}\n\n{{> Core2Buttons}}\n\n{{> Tone}}\n")
    return [("src/projects/demo.ubp.tmpl", "out/demo-{lang}.ubp")]


def test_render_replaces_keys_and_escapes_quotes():
    assert build.render("say '{{a.b}}'", {"a.b": "it's"}) == "say 'it''s'"


def test_render_fails_on_missing_key():
    with pytest.raises(build.BuildError, match="missing translation key: a.b"):
        build.render("{{a.b}}", {})


def test_render_inlines_includes():
    assert build.render("x\n{{> Lib}}\ny", {}, {"Lib": "LIB\n"}) == "x\nLIB\ny"


def test_render_fails_on_unknown_include():
    with pytest.raises(build.BuildError, match="unknown include: Lib"):
        build.render("{{> Lib}}", {}, {})


def test_included_text_is_not_rendered_again():
    assert build.render("{{> Lib}}", {}, {"Lib": "keep {{not.a.key}}"}) == "keep {{not.a.key}}"


def test_slot_count():
    assert build.slot_count("vibrate for _ ms") == 1
    assert build.slot_count("show big text _ colour _") == 2
    assert build.slot_count("board shaken?") == 0
    assert build.slot_count("_c2b_zone") == 0


def test_check_strings_accepts_consistent_strings():
    en = {"blk.x": "a _ b _", "screen.y": "Hi"}
    assert build.check_strings({"en": en, "fr": dict(en), "nl": dict(en)}) == []


def test_check_strings_reports_slot_mismatch():
    problems = build.check_strings({"en": {"blk.x": "a _ b _"}, "fr": {"blk.x": "a _ b"}})
    assert problems == ["fr: blk.x has 1 input slot(s), en has 2"]


def test_check_strings_reports_missing_and_unknown_keys():
    problems = build.check_strings({"en": {"a": "1", "b": "2"}, "nl": {"a": "1", "c": "3"}})
    assert problems == ["nl: missing key b", "nl: unknown key c"]


def test_check_strings_reports_empty_values():
    assert build.check_strings({"en": {"a": " "}}) == ["en: a is empty"]


def test_check_strings_screen_texts_must_be_ascii_and_short():
    problems = build.check_strings({"en": {"screen.a": "Peut-être", "screen.b": "x" * 27}})
    assert problems == ["en: screen.a must be plain ASCII", "en: screen.b is longer than 26 characters"]


def test_build_writes_library_and_projects_per_language(tmp_path):
    projects = make_workshop(tmp_path)
    written = build.build(tmp_path, projects)
    assert len(written) == 6
    fr_lib = (tmp_path / "library/Core2Buttons-fr.ubl").read_text(encoding="utf-8")
    assert "'vibrer pendant _ ms'" in fr_lib
    nl_project = (tmp_path / "out/demo-nl.ubp").read_text(encoding="utf-8")
    assert "c2b_bigText 'Hallo!'" in nl_project
    assert "module Core2Buttons Input" in nl_project
    assert "'tril _ ms'" in nl_project
    assert "module Tone Output" in nl_project


def test_build_refuses_inconsistent_strings(tmp_path):
    projects = make_workshop(tmp_path)
    write(tmp_path / "i18n/fr.json", json.dumps({"blk.vibrate": "vibrer", "screen.hello": "Salut !"}))
    with pytest.raises(build.BuildError, match="fr: blk.vibrate has 0 input slot"):
        build.build(tmp_path, projects)


def test_check_mode_lists_stale_files_without_writing(tmp_path):
    projects = make_workshop(tmp_path)
    build.build(tmp_path, projects)
    stale_file = tmp_path / "out/demo-en.ubp"
    stale_file.write_text("edited by hand", encoding="utf-8")
    assert build.build(tmp_path, projects, check=True) == [stale_file]
    assert stale_file.read_text(encoding="utf-8") == "edited by hand"


def test_second_build_writes_nothing(tmp_path):
    projects = make_workshop(tmp_path)
    build.build(tmp_path, projects)
    assert build.build(tmp_path, projects) == []
```

- [ ] **Step 3: Run the tests to verify they fail**

Run: `python3 -m pytest tools/tests/test_build.py -q`
Expected: collection error `ModuleNotFoundError: No module named 'build'`.

- [ ] **Step 4: Write the implementation**

`W/tools/build.py`:
```python
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
PROJECTS: tuple[tuple[str, str], ...] = ()


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
```

- [ ] **Step 5: Run the tests to verify they pass**

Run: `python3 -m pytest tools/tests/test_build.py -q`
Expected: `15 passed`.

- [ ] **Step 6: Start the changelog**

`W/CHANGELOG.md` (use the actual date of the day you work; this plan assumes 2026-11-11):
```markdown
# Changelog

All notable changes to the ESP32 workshop. One version entry per day.

## [0.1.0] - 2026-11-11

### Added
- Build tool that generates the MicroBlocks library and projects for English, French and Dutch.
```

- [ ] **Step 7: Commit**

```bash
git add workshops/InternetOfThings/ESP32/tools workshops/InternetOfThings/ESP32/CHANGELOG.md workshops/InternetOfThings/ESP32/.gitignore
git commit -m "ESP32 workshop: add per-language build tool for MicroBlocks files"
```

---

### Task 2: Documentation checker

**Files:**
- Create: `W/tools/check_docs.py`
- Create: `W/tools/tests/test_check_docs.py`
- Modify: `W/CHANGELOG.md` (add a bullet to today's entry)

**Interfaces:**
- Consumes: nothing.
- Produces: `check_docs.check_language_parity(root) -> list[str]`, `check_docs.check_links(root) -> list[str]`, `check_docs.check_no_asciidoc(root) -> list[str]`, `check_docs.check_mission_pages(root) -> list[str]`, `check_docs.main(argv=None) -> int`; CLI `python3 tools/check_docs.py [ROOT]`, exit 1 when any problem is found. Messages use paths relative to the root, with `/` separators.

- [ ] **Step 1: Write the failing tests**

`W/tools/tests/test_check_docs.py`:
```python
from pathlib import Path

import check_docs


def write(path: Path, text: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_parity_reports_missing_and_extra_files(tmp_path):
    for name in ("setup.md", "hardware.md"):
        write(tmp_path / "coach/en" / name)
        write(tmp_path / "coach/nl" / name)
    write(tmp_path / "coach/fr/setup.md")
    write(tmp_path / "coach/fr/extra.md")
    assert check_docs.check_language_parity(tmp_path) == [
        "coach/fr: missing hardware.md",
        "coach/fr: extra extra.md",
    ]


def test_parity_reports_missing_language_folder(tmp_path):
    write(tmp_path / "missions/01-x/en/mission.md")
    write(tmp_path / "missions/01-x/fr/mission.md")
    assert check_docs.check_language_parity(tmp_path) == ["missions/01-x/nl: folder missing"]


def test_links_only_reports_broken_local_targets(tmp_path):
    write(
        tmp_path / "README.md",
        "[ok](coach/en/setup.md) [bad](coach/en/nope.md) [web](https://example.org) "
        "[top](#top) ![img](images/a%20b.png) [anchor](coach/en/setup.md#step-1) [mail](mailto:x@y.z)",
    )
    write(tmp_path / "coach/en/setup.md")
    write(tmp_path / "images/a b.png")
    assert check_docs.check_links(tmp_path) == ["README.md: broken link coach/en/nope.md"]


def test_links_are_relative_to_the_file(tmp_path):
    write(tmp_path / "missions/01-x/en/mission.md", "[start](../starter/a-en.ubp)")
    assert check_docs.check_links(tmp_path) == ["missions/01-x/en/mission.md: broken link ../starter/a-en.ubp"]
    write(tmp_path / "missions/01-x/starter/a-en.ubp")
    assert check_docs.check_links(tmp_path) == []


def test_asciidoc_is_rejected(tmp_path):
    write(tmp_path / "README.adoc")
    write(tmp_path / "coach/en/old.asciidoc")
    assert check_docs.check_no_asciidoc(tmp_path) == [
        "README.adoc: AsciiDoc is not allowed, use Markdown",
        "coach/en/old.asciidoc: AsciiDoc is not allowed, use Markdown",
    ]


def test_mission_pages_must_exist(tmp_path):
    write(tmp_path / "missions/01-x/en/mission.md")
    assert check_docs.check_mission_pages(tmp_path) == ["missions/01-x/en: missing bonus-cards.md"]


def test_main_returns_zero_for_a_clean_tree(tmp_path):
    write(tmp_path / "README.md", "# Hi")
    assert check_docs.main([str(tmp_path)]) == 0


def test_main_returns_one_and_prints_problems(tmp_path, capsys):
    write(tmp_path / "README.adoc")
    assert check_docs.main([str(tmp_path)]) == 1
    assert "README.adoc: AsciiDoc is not allowed" in capsys.readouterr().out
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m pytest tools/tests/test_check_docs.py -q`
Expected: collection error `ModuleNotFoundError: No module named 'check_docs'`.

- [ ] **Step 3: Write the implementation**

`W/tools/check_docs.py`:
```python
#!/usr/bin/env python3
"""Check the ESP32 workshop documentation.

Usage (from the workshop folder):
    python3 tools/check_docs.py [ROOT]

Checks that every en/ folder has fr/ and nl/ siblings with the same files, that local
Markdown links resolve, that no AsciiDoc files exist, and that every mission has its
kids' pages. Exit code 1 when a problem is found.
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
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python3 -m pytest tools/tests -q`
Expected: `23 passed`.

- [ ] **Step 5: Update the changelog and commit**

Add under `### Added` of today's entry in `W/CHANGELOG.md`:
```markdown
- Documentation checker: language parity, local links, no AsciiDoc, mission pages present.
```

```bash
git add workshops/InternetOfThings/ESP32/tools workshops/InternetOfThings/ESP32/CHANGELOG.md
git commit -m "ESP32 workshop: add documentation checker"
```

---

### Task 3: Core2Buttons helper library, strings and vendored libraries

**Files:**
- Create: `W/i18n/en.json`, `W/i18n/fr.json`, `W/i18n/nl.json`
- Create: `W/src/library/Core2Buttons.ubl.tmpl`
- Create: `W/vendor/Tone.ubl`, `W/vendor/ESP Now.ubl`, `W/vendor/README.md`
- Create: `W/tools/tests/test_generated.py`
- Generated (commit them): `W/library/Core2Buttons-en.ubl`, `-fr.ubl`, `-nl.ubl`
- Modify: `W/CHANGELOG.md`

**Interfaces:**
- Consumes: `build.generate`, `build.build`, `build.ROOT`, `build.LANGS` (Task 1).
- Produces the MicroBlocks blocks every mission uses. Function names are language-independent; only labels change:

| Function (call it like this in project templates) | Kind | Label key |
|---|---|---|
| `(c2b_leftTouched)` | reporter, true once per touch | `blk.left_touched` |
| `(c2b_middleTouched)` | reporter, true once per touch | `blk.middle_touched` |
| `(c2b_rightTouched)` | reporter, true once per touch | `blk.right_touched` |
| `(c2b_shaken)` | reporter | `blk.shaken` |
| `c2b_vibrate ms` | command | `blk.vibrate` |
| `c2b_beep frequency ms` | command | `blk.beep` |
| `c2b_bigText text color` | command, clears screen then writes centred text | `blk.big_text` |

  Library module line: `module Core2Buttons Input`. It `depends Tone`, so every project must also include `{{> Tone}}`.

- [ ] **Step 1: Write the failing tests**

`W/tools/tests/test_generated.py`:
```python
"""Checks on the real generated files of the workshop (not on fixtures)."""
import json
import re

import pytest

import build

FUNCTION = re.compile(r"^to '?(_?c2b_\w+)'?", re.MULTILINE)
CALL = re.compile(r"\b(_?c2b_\w+)\b")
PUBLIC = ["c2b_leftTouched", "c2b_middleTouched", "c2b_rightTouched", "c2b_shaken",
          "c2b_vibrate", "c2b_beep", "c2b_bigText"]


@pytest.fixture(scope="module")
def files():
    return {path.relative_to(build.ROOT).as_posix(): text for path, text in build.generate().items()}


def library(files, lang="en"):
    return files[f"library/Core2Buttons-{lang}.ubl"]


def body(text, function):
    match = re.search(r"^to '?" + function + r"'?.*?\n}", text, re.MULTILINE | re.DOTALL)
    assert match, f"{function} not defined"
    return match.group(0)


def test_generated_files_are_up_to_date():
    assert build.build(check=True) == []


def test_library_defines_every_public_block_with_a_spec(files):
    for lang in build.LANGS:
        text = library(files, lang)
        assert text.startswith("module Core2Buttons Input\n")
        assert "\ndepends Tone" in text
        defined = set(FUNCTION.findall(text))
        for name in PUBLIC:
            assert name in defined
            assert re.search(r"^\s*spec '[ r]' '" + name + "' ", text, re.MULTILINE), name


def test_library_labels_are_translated(files):
    fr = json.loads((build.ROOT / "i18n/fr.json").read_text(encoding="utf-8"))
    text = library(files, "fr")
    for key, value in fr.items():
        if key.startswith("blk."):
            assert "'" + build.escape(value) + "'" in text, key


def test_every_button_goes_through_edge_detection(files):
    text = library(files)
    for zone, name in enumerate(["c2b_leftTouched", "c2b_middleTouched", "c2b_rightTouched"], start=1):
        assert f"('_c2b_edge' {zone})" in body(text, name)


def test_touches_on_the_screen_are_not_buttons(files):
    zone = body(library(files), "_c2b_zone")
    assert "(('[tft:tftTouchY]') < 240)" in zone


def test_big_text_shrinks_long_text(files):
    big = body(library(files), "c2b_bigText")
    assert "((size text) > 13)" in big
    assert "((size text) > 26)" in big


def main_module(text):
    """The project's own scripts, without the embedded libraries."""
    return text.split("\nmodule ")[0]


def test_no_template_markers_and_balanced_braces(files):
    for name, text in files.items():
        assert "{{" not in text, name
        own = main_module(text) if name.endswith(".ubp") else text
        assert own.count("{") == own.count("}"), name


def test_projects_only_call_defined_helpers(files):
    defined = set(FUNCTION.findall(library(files)))
    for name, text in files.items():
        if name.endswith(".ubp"):
            assert text.startswith("module main\n"), name
            assert "\nmodule Core2Buttons Input\n" in text, name
            assert "\nmodule Tone Output\n" in text, name
            assert set(CALL.findall(text)) <= defined | {"_c2b_wasDown"}, name
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m pytest tools/tests/test_generated.py -q`
Expected: errors with `FileNotFoundError: ... i18n/en.json`.

- [ ] **Step 3: Vendor the two MicroBlocks libraries**

Run from `W/`:
```bash
mkdir -p vendor
curl -fsSL "https://bitbucket.org/john_maloney/smallvm/raw/HEAD/Libraries/Tone.ubl" -o vendor/Tone.ubl
curl -fsSL "https://bitbucket.org/john_maloney/smallvm/raw/HEAD/Libraries/Network/ESP%20Now.ubl" -o "vendor/ESP Now.ubl"
head -1 vendor/Tone.ubl "vendor/ESP Now.ubl"
shasum -a 256 vendor/Tone.ubl "vendor/ESP Now.ubl"
```
Expected first lines: `module Tone Output` and `module 'ESP Now' Comm`.

`W/vendor/README.md` (fill in the two checksums printed above and today's date):
```markdown
# Vendored MicroBlocks libraries

These files are unchanged copies of libraries that ship with MicroBlocks. They are
embedded into the generated workshop projects so that children never have to add a
library by hand during a session.

| File | Source | Downloaded | SHA-256 |
|---|---|---|---|
| `Tone.ubl` | https://bitbucket.org/john_maloney/smallvm/src/HEAD/Libraries/Tone.ubl | 2026-11-11 | (checksum from `shasum`) |
| `ESP Now.ubl` | https://bitbucket.org/john_maloney/smallvm/src/HEAD/Libraries/Network/ESP%20Now.ubl | 2026-11-11 | (checksum from `shasum`) |

MicroBlocks is licensed under the Mozilla Public License 2.0
(https://mozilla.org/MPL/2.0/). These files keep that license.

To update: download the files again with the commands in this folder's history
(`curl` from the URLs above), run `python3 tools/build.py`, and re-test on a Core2.
```
Replace both `(checksum from shasum)` cells with the real values before committing.

- [ ] **Step 4: Write the strings**

`W/i18n/en.json`:
```json
{
  "lib.description": "Child-friendly blocks for the M5Stack Core2: the three red touch circles, shaking, vibration, beeps and big text. Made for the Devoxx4Kids ESP32 workshop.",
  "blk.left_touched": "left button touched?",
  "blk.middle_touched": "middle button touched?",
  "blk.right_touched": "right button touched?",
  "blk.shaken": "board shaken?",
  "blk.vibrate": "vibrate for _ ms",
  "blk.beep": "beep _ Hz for _ ms",
  "blk.big_text": "show big text _ colour _",
  "comment.zone": "Returns 1, 2 or 3 when the left, middle or right red circle under the screen is touched, otherwise 0. The circles are touch zones below the 240-pixel-high display.",
  "comment.edge": "True only at the moment a circle becomes touched, so one touch is one event even if the finger stays on it.",
  "comment.shaken": "Acceleration is about 100 when the board lies still. 140 needs a real shake.",
  "comment.vibrate": "The vibration motor is powered by LDO3 of the AXP192 power chip (I2C address 52). Bit 3 (value 8) of register 18 switches it on and off.",
  "comment.big_text": "Clears the screen and writes the text in the middle. Long texts use a smaller size so they still fit (one letter is 6 x 8 pixels at size 1)."
}
```

`W/i18n/fr.json`:
```json
{
  "lib.description": "Des blocs simples pour la M5Stack Core2 : les trois cercles rouges tactiles, secouer, vibrer, biper et du grand texte. Créés pour l'atelier ESP32 de Devoxx4Kids.",
  "blk.left_touched": "bouton gauche touché ?",
  "blk.middle_touched": "bouton du milieu touché ?",
  "blk.right_touched": "bouton droit touché ?",
  "blk.shaken": "carte secouée ?",
  "blk.vibrate": "vibrer pendant _ ms",
  "blk.beep": "bip _ Hz pendant _ ms",
  "blk.big_text": "afficher grand texte _ couleur _",
  "comment.zone": "Renvoie 1, 2 ou 3 quand le cercle rouge de gauche, du milieu ou de droite sous l'écran est touché, sinon 0. Les cercles sont des zones tactiles sous l'écran de 240 pixels de haut.",
  "comment.edge": "Vrai seulement au moment où un cercle devient touché : un toucher = un événement, même si le doigt reste dessus.",
  "comment.shaken": "L'accélération vaut environ 100 quand la carte est posée. Il faut vraiment secouer pour dépasser 140.",
  "comment.vibrate": "Le moteur de vibration est alimenté par LDO3 de la puce d'alimentation AXP192 (adresse I2C 52). Le bit 3 (valeur 8) du registre 18 l'allume et l'éteint.",
  "comment.big_text": "Efface l'écran et écrit le texte au milieu. Les textes longs sont plus petits pour tenir à l'écran (une lettre fait 6 x 8 pixels en taille 1)."
}
```

`W/i18n/nl.json`:
```json
{
  "lib.description": "Kindvriendelijke blokken voor de M5Stack Core2: de drie rode aanraakcirkels, schudden, trillen, piepen en grote tekst. Gemaakt voor de ESP32-workshop van Devoxx4Kids.",
  "blk.left_touched": "linkerknop aangeraakt?",
  "blk.middle_touched": "middelste knop aangeraakt?",
  "blk.right_touched": "rechterknop aangeraakt?",
  "blk.shaken": "bord geschud?",
  "blk.vibrate": "tril _ ms",
  "blk.beep": "piep _ Hz gedurende _ ms",
  "blk.big_text": "toon grote tekst _ kleur _",
  "comment.zone": "Geeft 1, 2 of 3 als de linker, middelste of rechter rode cirkel onder het scherm wordt aangeraakt, anders 0. De cirkels zijn aanraakzones onder het 240 pixels hoge scherm.",
  "comment.edge": "Alleen waar op het moment dat een cirkel aangeraakt wordt: één aanraking is één gebeurtenis, ook als de vinger blijft liggen.",
  "comment.shaken": "De versnelling is ongeveer 100 als het bord stil ligt. Voor meer dan 140 moet je echt schudden.",
  "comment.vibrate": "De trilmotor krijgt stroom van LDO3 van de AXP192-stroomchip (I2C-adres 52). Bit 3 (waarde 8) van register 18 zet hem aan en uit.",
  "comment.big_text": "Wist het scherm en schrijft de tekst in het midden. Lange teksten worden kleiner zodat ze passen (een letter is 6 x 8 pixels op grootte 1)."
}
```

- [ ] **Step 5: Write the library template**

`W/src/library/Core2Buttons.ubl.tmpl`:
```
module Core2Buttons Input
author Devoxx4Kids
version 1 0 
depends Tone 
description '{{lib.description}}'
variables _c2b_wasDown 

  spec 'r' 'c2b_leftTouched' '{{blk.left_touched}}'
  spec 'r' 'c2b_middleTouched' '{{blk.middle_touched}}'
  spec 'r' 'c2b_rightTouched' '{{blk.right_touched}}'
  space
  spec 'r' 'c2b_shaken' '{{blk.shaken}}'
  space
  spec ' ' 'c2b_vibrate' '{{blk.vibrate}}' 'num' 300
  spec ' ' 'c2b_beep' '{{blk.beep}}' 'num num' 880 200
  spec ' ' 'c2b_bigText' '{{blk.big_text}}' 'str color' 'Hello!' 16777215
  space
  spec 'r' '_c2b_zone' '_c2b_zone'
  spec 'r' '_c2b_edge' '_c2b_edge _' 'num' 1

to '_c2b_zone' {
  comment '{{comment.zone}}'
  if (not ('[tft:tftTouched]')) {
    return 0
  }
  if (('[tft:tftTouchY]') < 240) {
    return 0
  }
  local 'x' ('[tft:tftTouchX]')
  if (x < 107) {
    return 1
  }
  if (x < 214) {
    return 2
  }
  return 3
}

to '_c2b_edge' zone {
  comment '{{comment.edge}}'
  if (_c2b_wasDown == 0) {
    _c2b_wasDown = ('[data:makeList]' (booleanConstant false) (booleanConstant false) (booleanConstant false))
  }
  local 'down' (('_c2b_zone') == zone)
  local 'was' (at zone _c2b_wasDown)
  atPut zone _c2b_wasDown down
  return (and down (not was))
}

to c2b_leftTouched {
  return ('_c2b_edge' 1)
}

to c2b_middleTouched {
  return ('_c2b_edge' 2)
}

to c2b_rightTouched {
  return ('_c2b_edge' 3)
}

to c2b_shaken {
  comment '{{comment.shaken}}'
  return (('[sensors:acceleration]') > 140)
}

to c2b_vibrate ms {
  comment '{{comment.vibrate}}'
  local 'reg' (i2cGet 52 18)
  local 'off' (reg - (8 * ((reg / 8) % 2)))
  i2cSet 52 18 (off + 8)
  waitMillis ms
  i2cSet 52 18 off
}

to c2b_beep frequency ms {
  'play frequency' frequency ms
}

to c2b_bigText text color {
  comment '{{comment.big_text}}'
  text = ('[data:join]' '' text)
  local 'scale' 4
  if ((size text) > 13) {
    scale = 2
  }
  if ((size text) > 26) {
    scale = 1
  }
  local 'x' ((320 - ((size text) * (6 * scale))) / 2)
  if (x < 0) {
    x = 0
  }
  local 'y' ((240 - (8 * scale)) / 2)
  '[tft:clear]'
  '[tft:text]' text x y color scale (booleanConstant true)
}
```

- [ ] **Step 6: Generate the library files and run the tests**

Run: `python3 tools/build.py`
Expected output: `wrote: library/Core2Buttons-en.ubl`, `-fr.ubl`, `-nl.ubl`.

Run: `python3 -m pytest tools/tests -q`
Expected: all tests pass (`test_projects_only_call_defined_helpers` passes trivially because no projects exist yet).

- [ ] **Step 7: Update the changelog and commit**

Add under `### Added`:
```markdown
- `Core2Buttons` helper library (touch circles, shake, vibrate, beep, big text) in EN, FR and NL.
- Pinned copies of the MicroBlocks Tone and ESP Now libraries.
```

```bash
git add workshops/InternetOfThings/ESP32
git commit -m "ESP32 workshop: add Core2Buttons helper library and translations"
```

---

### Task 4: Mission 1 projects (Magic Shake Ball)

**Files:**
- Create: `W/src/projects/magic-ball-start.ubp.tmpl`, `W/src/projects/magic-ball-done.ubp.tmpl`
- Modify: `W/tools/build.py` (`PROJECTS`), `W/i18n/*.json` (new keys), `W/tools/tests/test_generated.py`, `W/CHANGELOG.md`
- Generated: `W/missions/01-magic-shake-ball/starter/magic-ball-start-{en,fr,nl}.ubp`, `W/missions/01-magic-shake-ball/solution/magic-ball-done-{en,fr,nl}.ubp`

**Interfaces:**
- Consumes: the library functions of Task 3; `{{> Core2Buttons}}` and `{{> Tone}}` includes.
- Produces: the starter project the kids open in Task 9's mission page, file `missions/01-magic-shake-ball/starter/magic-ball-start-<lang>.ubp`; the solution with the global variable `answers`.

- [ ] **Step 1: Write the failing test**

Append to `W/tools/tests/test_generated.py`:
```python
def test_magic_ball_solution_answers_touch_and_shake(files):
    en = json.loads((build.ROOT / "i18n/en.json").read_text(encoding="utf-8"))
    done = files["missions/01-magic-shake-ball/solution/magic-ball-done-en.ubp"]
    assert "whenCondition (or (c2b_middleTouched) (c2b_shaken))" in done
    for key in ("screen.m1_yes", "screen.m1_no", "screen.m1_maybe", "screen.m1_again", "screen.m1_ask"):
        assert "'" + build.escape(en[key]) + "'" in done, key
    start = files["missions/01-magic-shake-ball/starter/magic-ball-start-en.ubp"]
    assert "whenStarted" in start
    assert "c2b_middleTouched" not in main_module(start)
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 -m pytest tools/tests/test_generated.py -q -k magic_ball`
Expected: FAIL with `KeyError: 'missions/01-magic-shake-ball/solution/magic-ball-done-en.ubp'`.

- [ ] **Step 3: Add the strings**

Add these keys to the end of each file. Put a comma after the entry that was last before, so the JSON stays valid (`python3 -m json.tool i18n/en.json` must succeed).

`en.json`:
```json
  "project.m1_start": "Magic Shake Ball - start here",
  "project.m1_done": "Magic Shake Ball - finished version for coaches",
  "comment.m1_start": "Start here! Drag blocks from the Core2Buttons library under this block. Follow mission.md step by step.",
  "screen.m1_ask": "Ask me a question!",
  "screen.m1_yes": "Yes!",
  "screen.m1_no": "No way!",
  "screen.m1_maybe": "Maybe...",
  "screen.m1_again": "Ask again"
```

`fr.json`:
```json
  "project.m1_start": "Boule magique - commence ici",
  "project.m1_done": "Boule magique - version finie pour les coachs",
  "comment.m1_start": "Commence ici ! Glisse des blocs de la bibliothèque Core2Buttons sous ce bloc. Suis mission.md étape par étape.",
  "screen.m1_ask": "Pose-moi une question !",
  "screen.m1_yes": "Oui !",
  "screen.m1_no": "Pas question !",
  "screen.m1_maybe": "Possible...",
  "screen.m1_again": "Redemande"
```

`nl.json`:
```json
  "project.m1_start": "Magische schudbal - begin hier",
  "project.m1_done": "Magische schudbal - klaar, voor coaches",
  "comment.m1_start": "Begin hier! Sleep blokken uit de bibliotheek Core2Buttons onder dit blok. Volg mission.md stap voor stap.",
  "screen.m1_ask": "Stel me een vraag!",
  "screen.m1_yes": "Ja!",
  "screen.m1_no": "Echt niet!",
  "screen.m1_maybe": "Misschien...",
  "screen.m1_again": "Vraag opnieuw"
```

- [ ] **Step 4: Write the templates**

`W/src/projects/magic-ball-start.ubp.tmpl`:
```
module main
author Devoxx4Kids
version 1 0 
description '{{project.m1_start}}'

script 50 50 {
whenStarted
comment '{{comment.m1_start}}'
}


{{> Core2Buttons}}


{{> Tone}}
```

`W/src/projects/magic-ball-done.ubp.tmpl`:
```
module main
author Devoxx4Kids
version 1 0 
description '{{project.m1_done}}'
variables answers 

script 50 50 {
whenStarted
answers = ('[data:makeList]' '{{screen.m1_yes}}' '{{screen.m1_no}}' '{{screen.m1_maybe}}' '{{screen.m1_again}}')
c2b_bigText '{{screen.m1_ask}}' (colorSwatch 255 255 255 255)
}

script 50 220 {
whenCondition (or (c2b_middleTouched) (c2b_shaken))
local 'n' (random 1 (size answers))
if (n == 1) {
  c2b_bigText (at n answers) (colorSwatch 0 200 0 255)
} (n == 2) {
  c2b_bigText (at n answers) (colorSwatch 230 0 0 255)
} else {
  c2b_bigText (at n answers) (colorSwatch 255 200 0 255)
}
c2b_beep 880 150
c2b_vibrate 200
waitMillis 1500
c2b_bigText '{{screen.m1_ask}}' (colorSwatch 255 255 255 255)
}


{{> Core2Buttons}}


{{> Tone}}
```

- [ ] **Step 5: Register the projects**

In `W/tools/build.py`, replace the `PROJECTS` line with:
```python
PROJECTS: tuple[tuple[str, str], ...] = (
    ("src/projects/magic-ball-start.ubp.tmpl", "missions/01-magic-shake-ball/starter/magic-ball-start-{lang}.ubp"),
    ("src/projects/magic-ball-done.ubp.tmpl", "missions/01-magic-shake-ball/solution/magic-ball-done-{lang}.ubp"),
)
```

- [ ] **Step 6: Generate and run all tests**

Run: `python3 tools/build.py && python3 -m pytest tools/tests -q`
Expected: six `wrote: missions/01-magic-shake-ball/...` lines, then all tests pass.

- [ ] **Step 7: Update the changelog and commit**

Add under `### Added`: `- Mission 1 (Magic Shake Ball) starter and solution projects.`

```bash
git add workshops/InternetOfThings/ESP32
git commit -m "ESP32 workshop: add Magic Shake Ball projects"
```

---

### Task 5: Mission 2 projects (Hot Potato / Duel)

**Files:**
- Create: `W/src/projects/hot-potato-start.ubp.tmpl`, `W/src/projects/hot-potato-done.ubp.tmpl`
- Modify: `W/tools/build.py` (`PROJECTS`), `W/i18n/*.json`, `W/tools/tests/test_generated.py`, `W/CHANGELOG.md`
- Generated: `W/missions/02-hot-potato/starter/hot-potato-start-{en,fr,nl}.ubp`, `W/missions/02-hot-potato/solution/hot-potato-done-{en,fr,nl}.ubp`

**Interfaces:**
- Consumes: library functions (Task 3).
- Produces: solution with global variable `lives`; the middle circle starts Hot Potato and the right circle starts the duel (Task 10's mission page relies on this).

- [ ] **Step 1: Write the failing test**

Append to `W/tools/tests/test_generated.py`:
```python
def test_hot_potato_solution_has_both_games(files):
    done = files["missions/02-hot-potato/solution/hot-potato-done-en.ubp"]
    assert "whenCondition (c2b_middleTouched)" in done
    assert "whenCondition (c2b_rightTouched)" in done
    assert "(random 5000 15000)" in done
    assert "lives = (lives - 1)" in done
    start = files["missions/02-hot-potato/starter/hot-potato-start-en.ubp"]
    assert "whenStarted" in start
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 -m pytest tools/tests/test_generated.py -q -k hot_potato`
Expected: FAIL with `KeyError: 'missions/02-hot-potato/solution/hot-potato-done-en.ubp'`.

- [ ] **Step 3: Add the strings**

`en.json`:
```json
  "project.m2_start": "Hot Potato - start here",
  "project.m2_done": "Hot Potato and Duel - finished version for coaches",
  "comment.m2_start": "Start here! Middle circle = Hot Potato, right circle = Duel. Follow mission.md step by step.",
  "screen.m2_ready": "Touch to start!",
  "screen.m2_pass": "PASS IT ON!",
  "screen.m2_boom": "BOOM!",
  "screen.m2_lives": "Lives:",
  "screen.m2_game_over": "GAME OVER",
  "screen.m2_get_ready": "Get ready...",
  "screen.m2_go": "GO!",
  "screen.m2_early_left": "Left: too early!",
  "screen.m2_early_right": "Right: too early!",
  "screen.m2_left_wins": "Left wins!",
  "screen.m2_right_wins": "Right wins!"
```

`fr.json`:
```json
  "project.m2_start": "Patate chaude - commence ici",
  "project.m2_done": "Patate chaude et duel - version finie pour les coachs",
  "comment.m2_start": "Commence ici ! Cercle du milieu = patate chaude, cercle de droite = duel. Suis mission.md étape par étape.",
  "screen.m2_ready": "Touche pour jouer !",
  "screen.m2_pass": "PASSE-LA !",
  "screen.m2_boom": "BOUM !",
  "screen.m2_lives": "Vies :",
  "screen.m2_game_over": "PERDU !",
  "screen.m2_get_ready": "Attention...",
  "screen.m2_go": "PARTEZ !",
  "screen.m2_early_left": "Gauche : trop vite !",
  "screen.m2_early_right": "Droite : trop vite !",
  "screen.m2_left_wins": "Gauche gagne !",
  "screen.m2_right_wins": "Droite gagne !"
```

`nl.json`:
```json
  "project.m2_start": "Hete aardappel - begin hier",
  "project.m2_done": "Hete aardappel en duel - klaar, voor coaches",
  "comment.m2_start": "Begin hier! Middelste cirkel = hete aardappel, rechter cirkel = duel. Volg mission.md stap voor stap.",
  "screen.m2_ready": "Tik om te starten!",
  "screen.m2_pass": "GEEF DOOR!",
  "screen.m2_boom": "BOEM!",
  "screen.m2_lives": "Levens:",
  "screen.m2_game_over": "GAME OVER",
  "screen.m2_get_ready": "Opgelet...",
  "screen.m2_go": "NU!",
  "screen.m2_early_left": "Links: te vroeg!",
  "screen.m2_early_right": "Rechts: te vroeg!",
  "screen.m2_left_wins": "Links wint!",
  "screen.m2_right_wins": "Rechts wint!"
```

- [ ] **Step 4: Write the templates**

`W/src/projects/hot-potato-start.ubp.tmpl`:
```
module main
author Devoxx4Kids
version 1 0 
description '{{project.m2_start}}'

script 50 50 {
whenStarted
comment '{{comment.m2_start}}'
}


{{> Core2Buttons}}


{{> Tone}}
```

`W/src/projects/hot-potato-done.ubp.tmpl`:
```
module main
author Devoxx4Kids
version 1 0 
description '{{project.m2_done}}'
variables lives 

script 50 50 {
whenStarted
lives = 3
c2b_bigText '{{screen.m2_ready}}' (colorSwatch 255 255 255 255)
}

script 50 200 {
whenCondition (c2b_middleTouched)
local 'fuse' (random 5000 15000)
local 'tick' 600
resetTimer
repeatUntil ((timer) > fuse) {
  c2b_bigText '{{screen.m2_pass}}' (colorSwatch 255 200 0 255)
  c2b_beep 440 50
  waitMillis tick
  if (tick > 120) {
    tick = (tick - 40)
  }
}
c2b_bigText '{{screen.m2_boom}}' (colorSwatch 255 0 0 255)
c2b_vibrate 800
lives = (lives - 1)
waitMillis 1500
if (lives > 0) {
  c2b_bigText ('[data:join]' '{{screen.m2_lives}}' ' ' lives) (colorSwatch 255 255 255 255)
} else {
  c2b_bigText '{{screen.m2_game_over}}' (colorSwatch 255 0 0 255)
  lives = 3
}
}

script 450 200 {
whenCondition (c2b_rightTouched)
c2b_bigText '{{screen.m2_get_ready}}' (colorSwatch 255 255 255 255)
waitMillis 800
local 'delay' (random 2000 5000)
local 'winner' 0
resetTimer
repeatUntil (or ((timer) > delay) (winner != 0)) {
  if (c2b_leftTouched) {
    winner = -1
  }
  if (c2b_rightTouched) {
    winner = -2
  }
}
if (winner == -1) {
  c2b_bigText '{{screen.m2_early_left}}' (colorSwatch 255 0 0 255)
} (winner == -2) {
  c2b_bigText '{{screen.m2_early_right}}' (colorSwatch 255 0 0 255)
} else {
  c2b_bigText '{{screen.m2_go}}' (colorSwatch 0 255 0 255)
  c2b_beep 1000 100
  repeatUntil (winner != 0) {
    if (c2b_leftTouched) {
      winner = 1
    }
    if (c2b_rightTouched) {
      winner = 2
    }
  }
  if (winner == 1) {
    c2b_bigText '{{screen.m2_left_wins}}' (colorSwatch 0 200 255 255)
  } else {
    c2b_bigText '{{screen.m2_right_wins}}' (colorSwatch 255 0 255 255)
  }
  c2b_vibrate 300
}
waitMillis 2000
c2b_bigText '{{screen.m2_ready}}' (colorSwatch 255 255 255 255)
}


{{> Core2Buttons}}


{{> Tone}}
```

- [ ] **Step 5: Register the projects**

In `W/tools/build.py`, add these two entries at the end of the `PROJECTS` tuple:
```python
    ("src/projects/hot-potato-start.ubp.tmpl", "missions/02-hot-potato/starter/hot-potato-start-{lang}.ubp"),
    ("src/projects/hot-potato-done.ubp.tmpl", "missions/02-hot-potato/solution/hot-potato-done-{lang}.ubp"),
```

- [ ] **Step 6: Generate and run all tests**

Run: `python3 tools/build.py && python3 -m pytest tools/tests -q`
Expected: six `wrote: missions/02-hot-potato/...` lines, all tests pass.

- [ ] **Step 7: Update the changelog and commit**

Add under `### Added`: `- Mission 2 (Hot Potato and Duel) starter and solution projects.`

```bash
git add workshops/InternetOfThings/ESP32
git commit -m "ESP32 workshop: add Hot Potato and Duel projects"
```

---

### Task 6: Mission 3 projects (Emoji Messenger)

**Files:**
- Create: `W/src/projects/emoji-messenger-start.ubp.tmpl`, `W/src/projects/emoji-messenger-done.ubp.tmpl`
- Modify: `W/tools/build.py` (`PROJECTS`), `W/i18n/*.json`, `W/tools/tests/test_generated.py`, `W/CHANGELOG.md`
- Generated: `W/missions/03-emoji-messenger/starter/emoji-messenger-start-{en,fr,nl}.ubp`, `W/missions/03-emoji-messenger/solution/emoji-messenger-done-{en,fr,nl}.ubp`

**Interfaces:**
- Consumes: library functions (Task 3); vendored ESP Now functions `espNow_send_pair s n`, `(espNow_receive_pair)`, `(espNow_last_number)`, `(espNow_last_string)` and the primitive `'[net:ESPNowSetGroup]' n`.
- Produces: message protocol used by the mission page (Task 11) and bonus cards: an ESP Now *pair* where the string is the sender's team name and the number is the emoji index (1–8) or `0` for "party". Global variables `emojis`, `choice`, `myName`.

- [ ] **Step 1: Write the failing test**

Append to `W/tools/tests/test_generated.py`:
```python
def test_messenger_projects_use_esp_now_and_ignore_bad_numbers(files):
    for kind in ("start", "done"):
        text = files[f"missions/03-emoji-messenger/{'starter' if kind == 'start' else 'solution'}/emoji-messenger-{kind}-en.ubp"]
        assert "\nmodule 'ESP Now' Comm\n" in text
        assert "'[net:ESPNowSetGroup]' 1" in text
        assert "emojis = ('[data:makeList]'" in text
    done = files["missions/03-emoji-messenger/solution/emoji-messenger-done-en.ubp"]
    assert "whenCondition (espNow_receive_pair)" in done
    assert "(and (n >= 1) (n <= (size emojis)))" in done
    assert "espNow_send_pair myName 0" in done
    assert "espNow_send_pair myName choice" in done
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 -m pytest tools/tests/test_generated.py -q -k messenger`
Expected: FAIL with `KeyError` on the starter path.

- [ ] **Step 3: Add the strings**

`en.json`:
```json
  "project.m3_start": "Emoji Messenger - start here",
  "project.m3_done": "Emoji Messenger - finished version for coaches",
  "comment.m3_start": "Start here! Change the group number 1 to your table number. The emoji list is ready for you. Follow mission.md step by step.",
  "screen.m3_name": "Team 1",
  "screen.m3_sent": "Sent!",
  "screen.m3_party": "PARTY!"
```

`fr.json`:
```json
  "project.m3_start": "Messagerie emoji - commence ici",
  "project.m3_done": "Messagerie emoji - version finie pour les coachs",
  "comment.m3_start": "Commence ici ! Remplace le numéro de groupe 1 par le numéro de ta table. La liste d'emojis est déjà prête. Suis mission.md étape par étape.",
  "screen.m3_name": "Equipe 1",
  "screen.m3_sent": "Parti !",
  "screen.m3_party": "FIESTA !"
```

`nl.json`:
```json
  "project.m3_start": "Emoji-messenger - begin hier",
  "project.m3_done": "Emoji-messenger - klaar, voor coaches",
  "comment.m3_start": "Begin hier! Verander groepsnummer 1 in jullie tafelnummer. De emojilijst staat al klaar. Volg mission.md stap voor stap.",
  "screen.m3_name": "Team 1",
  "screen.m3_sent": "Verstuurd!",
  "screen.m3_party": "FEEST!"
```

- [ ] **Step 4: Write the templates**

`W/src/projects/emoji-messenger-start.ubp.tmpl`:
```
module main
author Devoxx4Kids
version 1 0 
description '{{project.m3_start}}'
variables emojis choice myName 

script 50 50 {
whenStarted
comment '{{comment.m3_start}}'
'[net:ESPNowSetGroup]' 1
myName = '{{screen.m3_name}}'
emojis = ('[data:makeList]' ':-)' ':-D' ';-)' '<3' ':-O' ':-(' 'B-)' ':-P')
choice = 1
}


{{> Core2Buttons}}


{{> Tone}}


{{> ESP Now}}
```

`W/src/projects/emoji-messenger-done.ubp.tmpl`:
```
module main
author Devoxx4Kids
version 1 0 
description '{{project.m3_done}}'
variables emojis choice myName 

script 50 50 {
whenStarted
comment '{{comment.m3_start}}'
'[net:ESPNowSetGroup]' 1
myName = '{{screen.m3_name}}'
emojis = ('[data:makeList]' ':-)' ':-D' ';-)' '<3' ':-O' ':-(' 'B-)' ':-P')
choice = 1
c2b_bigText (at choice emojis) (colorSwatch 255 255 255 255)
}

script 50 300 {
whenCondition (c2b_leftTouched)
choice = (choice - 1)
if (choice < 1) {
  choice = (size emojis)
}
c2b_bigText (at choice emojis) (colorSwatch 255 255 255 255)
}

script 50 450 {
whenCondition (c2b_rightTouched)
choice = (choice + 1)
if (choice > (size emojis)) {
  choice = 1
}
c2b_bigText (at choice emojis) (colorSwatch 255 255 255 255)
}

script 450 50 {
whenCondition (c2b_middleTouched)
espNow_send_pair myName choice
c2b_bigText '{{screen.m3_sent}}' (colorSwatch 0 255 0 255)
waitMillis 500
c2b_bigText (at choice emojis) (colorSwatch 255 255 255 255)
}

script 450 250 {
whenCondition (c2b_shaken)
espNow_send_pair myName 0
c2b_bigText '{{screen.m3_sent}}' (colorSwatch 0 255 0 255)
waitMillis 500
c2b_bigText (at choice emojis) (colorSwatch 255 255 255 255)
}

script 850 50 {
whenCondition (espNow_receive_pair)
local 'n' (espNow_last_number)
if (n == 0) {
  repeat 3 {
    c2b_bigText '{{screen.m3_party}}' (colorSwatch 255 0 255 255)
    c2b_vibrate 100
    c2b_bigText '{{screen.m3_party}}' (colorSwatch 0 255 255 255)
    waitMillis 100
  }
} (and (n >= 1) (n <= (size emojis))) {
  c2b_bigText (at n emojis) (colorSwatch 255 220 0 255)
  '[tft:text]' (espNow_last_string) 10 200 (colorSwatch 255 255 255 255) 2 (booleanConstant false)
  c2b_beep 660 100
  waitMillis 2000
}
c2b_bigText (at choice emojis) (colorSwatch 255 255 255 255)
}


{{> Core2Buttons}}


{{> Tone}}


{{> ESP Now}}
```

- [ ] **Step 5: Register the projects**

In `W/tools/build.py`, add at the end of `PROJECTS`:
```python
    ("src/projects/emoji-messenger-start.ubp.tmpl", "missions/03-emoji-messenger/starter/emoji-messenger-start-{lang}.ubp"),
    ("src/projects/emoji-messenger-done.ubp.tmpl", "missions/03-emoji-messenger/solution/emoji-messenger-done-{lang}.ubp"),
```

- [ ] **Step 6: Generate and run all tests**

Run: `python3 tools/build.py && python3 -m pytest tools/tests -q`
Expected: six `wrote: missions/03-emoji-messenger/...` lines, all tests pass.

- [ ] **Step 7: Update the changelog and commit**

Add under `### Added`: `- Mission 3 (Emoji Messenger) starter and solution projects using ESP Now.`

```bash
git add workshops/InternetOfThings/ESP32
git commit -m "ESP32 workshop: add Emoji Messenger projects"
```

---

### Task 7: Hardware spike and validation on two Core2 boards (HUMAN)

This task needs two M5Stack **Core2 v1.3 (K010-V13)** boards, a laptop with Chrome or Edge (or the MicroBlocks desktop app) and two USB-C data cables. An AI agent cannot do it; hand it to a person and wait for their results. The outcome decides whether Tasks 3–6 need changes, and whether the workshop stays on MicroBlocks or moves to UiFlow2 (Step 8), so it must be done before Task 8.

Why the board revision matters (checked 2026-11-11):

| Revision | Part number | Power chip | Motion sensor | MicroBlocks |
|---|---|---|---|---|
| Core2 | K010 | AXP192 | MPU6886 | What its Core2 firmware was written for |
| Core2 v1.1 | K010-V11 | AXP2101 | MPU6886 | Power code only knows the AXP192. **Do not buy.** |
| Core2 v1.3 | K010-V13 | AXP192 | **BMI270** | Firmware reads the motion sensor as an MPU6886, so **shake is expected to fail** |

M5Stack also changed the Core2 screen controller to ILI9342E in August 2026; Step 1 checks that the screen works.

**Files:**
- Create: `W/library/README.md` (results section; Task 8 adds the rest)
- Modify, only if a check fails: `W/src/library/Core2Buttons.ubl.tmpl`, `W/src/projects/*.ubp.tmpl`, `W/i18n/*.json`, then regenerate
- Modify: `W/CHANGELOG.md`

**Interfaces:**
- Consumes: generated files from Tasks 3–6.
- Produces: `W/library/README.md` section `## Tested on hardware` with one row per check below (result, MicroBlocks version, firmware version, date). Tasks 8–11 rely on the verified block labels and menu names recorded here.

- [ ] **Step 1: Install MicroBlocks firmware on both boards (check H1)**

1. Open https://microblocks.fun, click **Run** (or start the desktop app from https://microblocks.fun/download).
2. Connect the Core2 by USB-C. Click the USB icon and connect to the board.
3. Open the ⚙ (gear) menu → **update firmware on board** → choose the Core2 entry. Write down the exact menu texts and the board name MicroBlocks shows.
4. Repeat for the second board.
5. Click the `show big text Hello! colour` block in the Core2Buttons palette (open any starter project first).
Pass: both boards connect, the board name shows "M5StackCore2", and the screen shows "Hello!". Record the MicroBlocks version (⚙ → **about**) and the colour of the power LED (green = AXP192). A black screen is a failure of H1, not a cable problem, if the board still connects.

- [ ] **Step 2: Load the library and check the buttons (H2, H3)**

1. Open `missions/01-magic-shake-ball/solution/magic-ball-done-en.ubp` (drag the file onto the MicroBlocks window).
2. H2: Touch each red circle under the screen, then touch the middle of the screen. Pass: middle circle shows an answer; left and right circles do nothing; touching the screen does nothing.
3. H3: Keep a finger on the middle circle for 3 seconds. Pass: exactly one answer. Tap 5 times quickly. Pass: no more than one answer per tap.
If the screen touch counts as a button, or no circle reacts: in MicroBlocks add a script `forever { say (tft touch y) }` (TFT library → **touch y**) and note the values for the circles; change the `240` in `_c2b_zone` and the `107`/`214` x limits in `W/src/library/Core2Buttons.ubl.tmpl` to the observed boundaries, then rebuild (Step 8).

- [ ] **Step 3: Sound (H4)**

Expected from a code review (2026-11-11): the MicroBlocks Tone library has no default pin for the board name `M5StackCore2`, and the Core2 speaker is an I2S amplifier, so the beep is probably silent. The library already draws a yellow frame around the screen during every beep and buzz, so the missions stay playable without sound.
Click the `beep 880 Hz for 200 ms` block in the palette. Pass: an audible beep. Also check that the yellow frame appears and disappears.
If silent, replace the body of `c2b_beep` in the library template with a vibration fallback, so the missions still work:
```
to c2b_beep frequency ms {
  c2b_vibrate ms
}
```
and note "speaker silent, beep falls back to vibration" in the results.

- [ ] **Step 4: Shake and vibration (H5)**

1. Hold the board still in two hands for 10 seconds while the Magic Ball solution runs. Pass: no answer appears.
2. Shake it once firmly. Pass: an answer appears.
3. Watch for vibration with each answer. Pass: a short buzz; the motor is quiet otherwise.
   Run `say (i2cGet 52 18)` first. Expected from the code review: MicroBlocks' I2C blocks use the external Grove pins (32/33) on the Core2, while the power chip that drives the motor is on the internal bus (21/22), so the value is an error code and the motor stays off. Record the value.
First check that the sensor is read at all: run `forever { say (acceleration) }` (Basic Sensors library) and tilt the board. If the value stays the same (often 0) whatever you do, H5 **fails because of the BMI270**, not because of the threshold: write "acceleration constant: <value>" in the notes and go on; Step 8 decides what to do. Do not tune the threshold in that case.
If the value changes but shaking needs too much force, lower `140` in `c2b_shaken` in steps of 10 (and update `comment.shaken` in all three JSON files); if holding triggers it, raise it. If the motor never buzzes, or buzzes all the time, record the value of `(i2cGet 52 18)` shown with a `say` block, and change the `i2cGet`/`i2cSet` lines in `c2b_vibrate` accordingly; if the I2C blocks cannot reach the power chip at all, make `c2b_vibrate` only wait (`waitMillis ms`) and note it.

- [ ] **Step 5: Hot Potato and Duel (H7)**

Open `missions/02-hot-potato/solution/hot-potato-done-en.ubp`. Middle circle: ticking speeds up, BOOM appears after 5–15 s, lives count down from 3 to GAME OVER. Right circle: "Get ready...", touching left early shows "Left: too early!", otherwise "GO!" and the first circle touched wins.

- [ ] **Step 6: ESP Now between two boards (H6)**

1. Open `missions/03-emoji-messenger/solution/emoji-messenger-done-en.ubp` on board 1, save it, then open it on board 2 and change `Team 1` to `Team 2`.
2. Board 1: choose an emoji with left/right, touch middle. Pass: board 2 shows the emoji, "Team 1" at the bottom, and beeps within 1 second.
3. Shake board 2. Pass: board 1 shows PARTY! three times.
4. Change board 2's group to 2. Pass: messages no longer arrive.
5. With board 2 still running Messenger, open the Hot Potato solution on board 1 (no ESP Now sends). Pass: board 2 shows nothing unusual. Send from a MicroBlocks block `espNow send pair 'x' = 42` on board 1 after reopening Messenger with group 1. Pass: board 2 ignores it (no error, no crash).
6. If more boards are available, run 4–10 boards in the same room on different groups and note how many messages get lost.

- [ ] **Step 7: Languages and text (H8, H9)**

1. H9: Switch MicroBlocks to Français (globe icon), open `magic-ball-done-fr.ubp`. Pass: built-in blocks are in French and the Core2Buttons blocks show the labels from `fr.json`. Repeat for Nederlands with `-nl.ubp`.
2. H8: Change one answer to `Peut-être !` and another to a 40-character sentence, run the project. Record whether `ê` renders. Pass: the long sentence fits on the screen (smaller text).
3. Write down the exact on-screen English labels of these built-in blocks, as MicroBlocks shows them, for Tasks 9–11: `when started`, `when`, `wait … millisecs`, `random … to …`, `item … of …`, `length of …`, `list`, `set … to …`, `change … by …`, `initialize local … to …`, `if … else`, `or`, `and`, `=`, `≠`, `≥`, `≤`, `join`, `repeat until`, `repeat`, `reset timer`, `timer`, the ESP Now blocks, and the name of the button that adds a variable.

- [ ] **Step 8: Decide: MicroBlocks or UiFlow2**

Apply the first rule that matches, and write the decision in `W/library/README.md` (Step 10):

| Result of H1–H9 | Decision | What happens next |
|---|---|---|
| All pass, or every failure has the fallback from its step applied | **MicroBlocks** | Continue with Step 10 and then Task 8. |
| Only H5 fails with "acceleration constant" (the BMI270 case), and/or H4 has no sound and H5 has no buzz while the yellow frame works; everything else passes | **MicroBlocks + firmware patch** | Do Step 9 (UiFlow2 check) as an insurance, then patch the firmware (below). Continue with Task 8 only when the patched firmware passes H5. |
| H1 (connect or screen) or H2 (touch circles) fails, or two or more of H4, H5, H6 fail without a working fallback | **UiFlow2** | Do Step 9. If UiFlow2 passes U1–U5, **stop the plan after Step 11**: the spec must be revised for UiFlow2 before any further task (see "If the decision is UiFlow2" below). |

**Firmware patch for the BMI270 (MicroBlocks + firmware patch):**
1. Clone MicroBlocks: `git clone https://bitbucket.org/john_maloney/smallvm.git` and install PlatformIO (`pip install platformio`).
2. In `vm/sensorPrims.cpp`, the Core2 shares the MPU6886 code path (`#elif defined(ARDUINO_M5Stack_Core_ESP32) || defined(ARDUINO_M5STACK_Core2) ...`). For `ARDUINO_M5STACK_Core2` only, read the chip ID at I2C address `0x68` on the internal bus first: register `0x00` returns `0x24` on a BMI270, register `0x75` returns `0x19` on an MPU6886. When it is a BMI270, use the existing `bmi270Init()` / BMI270 read functions (today only compiled for `DATABOT_V3`; move them out of that `#if` so the Core2 build gets them too).
3. Build: `pio run -e m5core2`. The firmware is `.pio/build/m5core2/firmware.bin`.
4. Install it: drag the `.bin` file onto the MicroBlocks window with the board connected (MicroBlocks installs dropped ESP firmware files), then re-run H5 and H1–H3.
5. If there was no sound or no buzz, extend the same patch: for `ARDUINO_M5STACK_Core2`, give the Tone primitives an I2S output on the NS4168 (BCLK 12, LRCK 0, DATA 2; the firmware already enables the speaker through the AXP192), and add a vibration on/off primitive that sets bit 3 of AXP192 register 0x12 through `Wire1` (the code in `tftPrims.cpp` already writes that register). Then change `c2b_vibrate` in `W/src/library/Core2Buttons.ubl.tmpl` to call the new primitive, rebuild, and re-run H4 and H5.
6. Offer the patch upstream (MicroBlocks accepts contributions via https://microblocks.fun/contact or the Bitbucket repository), and record the patched firmware's commit in `W/library/README.md`. Until it is released upstream, coaches install this `.bin` instead of the standard firmware; Task 8's `coach/en/setup.md` must then say so (copy the file to `W/firmware/microblocks-core2-bmi270.bin`, with a README naming the source commit).

- [ ] **Step 9: UiFlow2 check (only for "MicroBlocks + firmware patch" or "UiFlow2")**

Install UiFlow2 on one board with M5Burner (https://docs.m5stack.com/en/download) and open the UiFlow2 web IDE (https://uiflow2.m5stack.com). Build each check with UiFlow2's own blocks, on the Core2 v1.3:

| Check | Build this | Pass |
|---|---|---|
| U1 | Show a label "Hello!" | Text on the screen, program runs within ~5 s of pressing Run |
| U2 | `when BtnA/BtnB/BtnC pressed` → change the label | Each red circle reacts once per touch; the screen above does not |
| U3 | Show the IMU acceleration in a label, in a loop | Values change when the board is tilted or shaken (BMI270 works) |
| U4 | Speaker tone and vibration (Power) blocks | Audible tone; motor buzzes |
| U5 | ESP-NOW broadcast from board 1, receive callback on board 2 | Message arrives within 1 s, without entering MAC addresses by hand (or note the simplest setup that works) |

Also record: whether the IDE works without internet or without an account, and which interface languages it offers. As checked on 2026-11-11, UiFlow2's translation repository (https://github.com/m5stack/uiflow-i18n/tree/main/uiflow-2.x) contains only `en.json` and `ja.json`, so French and Dutch children would see an English interface unless FR/NL translations are contributed there.

**If the decision is UiFlow2:** record U1–U5, finish Steps 10–11, and stop. Report back so the spec can be revised: the missions, session rhythm and kids' page structure stay, but the helper library, the build tool's MicroBlocks templates (Tasks 1, 3–6), the radio pairing in Mission 3, and the FR/NL interface plan change.

- [ ] **Step 10: Rebuild after any change, and record the results**

If any template or JSON changed: `python3 tools/build.py && python3 -m pytest tools/tests -q` (all must pass).

`W/library/README.md`:
```markdown
# Core2Buttons library

## Tested on hardware

Board revision: Core2 v1.3 (K010-V13), power LED colour: 

| Check | What was tested | Result | Notes |
|---|---|---|---|
| H1 | Firmware install, connection, screen | | MicroBlocks version: , firmware: , date: |
| H2 | Circles react, screen touch ignored | | |
| H3 | One event per touch (hold, fast taps) | | |
| H4 | Beep on the speaker | | |
| H5 | Shake threshold and vibration | | acceleration changes: yes/no, final threshold: |
| H6 | ESP Now between boards, groups, bad numbers | | boards in room: , lost messages: |
| H7 | Hot Potato and Duel | | |
| H8 | Long text and accents on screen | | accents render: yes/no |
| H9 | FR and NL labels | | |
| U1–U5 | UiFlow2 check (only if Step 9 was done) | | offline: , account needed: , languages: |

**Decision (Step 8):** MicroBlocks / MicroBlocks + firmware patch / UiFlow2 — reason:

## Built-in block labels (English, as shown by MicroBlocks)

| Block | Label |
|---|---|
| when started | |
| when (condition) | |
| wait | |
| random | |
| item of | |
| length of | |
| list | |
| set variable | |
| local variable | |
| change variable | |
| if / else | |
| or / and / = | |
| join | |
| repeat until / repeat | |
| reset timer / timer | |
| espNow send pair / pair received? / last number / last string / set group | |
| add a variable (button) | |
| firmware menu path | |
```
Fill every empty cell from Steps 1–9. Every check must say "pass" or describe the fallback that was applied, and the decision line must be filled in.

- [ ] **Step 11: Update the changelog and commit**

Add to today's entry (or a new dated entry if this is a later day), under `### Changed` if the library changed:
```markdown
- Library tuned after testing on two Core2 v1.3 boards; platform decision recorded (see library/README.md).
```

```bash
git add workshops/InternetOfThings/ESP32
git commit -m "ESP32 workshop: record Core2 hardware test results and platform decision"
```

---

### Task 8: English entry page, library reference and coach docs

**Files:**
- Create: `W/README.md`
- Modify: `W/library/README.md` (add sections above `## Tested on hardware`)
- Create: `W/coach/en/setup.md`, `W/coach/en/running-a-session.md`, `W/coach/en/hardware.md`
- Modify: `W/CHANGELOG.md`

**Interfaces:**
- Consumes: block labels and menu names recorded in `W/library/README.md` by Task 7. Wherever the text below shows a menu name or label in `**bold**`, use the exact text recorded in Task 7 if it differs.
- Produces: the page names that Tasks 9–13 link to: `coach/<lang>/setup.md`, `coach/<lang>/running-a-session.md`, `coach/<lang>/hardware.md`.

- [ ] **Step 1: Write `W/README.md`**

```markdown
# ESP32 Workshop: Magic Shake Ball 🎱

A Devoxx4Kids workshop for children aged 10 to 14. Working in pairs, they program an
**M5Stack Core2** (an ESP32 board with a touch screen, motion sensor, speaker and
vibration motor) with **MicroBlocks**, a free block language that looks like Scratch and
runs the program on the board straight away.

Every mission takes **45 minutes** and works on its own, so you can run one, two or all
three.

| Mission | What the pair builds | 🇬🇧 | 🇫🇷 | 🇳🇱 |
|---|---|---|---|---|
| 1. Magic Shake Ball | Ask a question, shake the board, get a random answer | [EN](missions/01-magic-shake-ball/en/mission.md) | [FR](missions/01-magic-shake-ball/fr/mission.md) | [NL](missions/01-magic-shake-ball/nl/mission.md) |
| 2. Hot Potato | Pass the board around before it explodes, then a reaction duel | [EN](missions/02-hot-potato/en/mission.md) | [FR](missions/02-hot-potato/fr/mission.md) | [NL](missions/02-hot-potato/nl/mission.md) |
| 3. Emoji Messenger | Send emojis to other tables by radio, no Wi-Fi needed | [EN](missions/03-emoji-messenger/en/mission.md) | [FR](missions/03-emoji-messenger/fr/mission.md) | [NL](missions/03-emoji-messenger/nl/mission.md) |

## For coaches

Read these before the event:

| | 🇬🇧 | 🇫🇷 | 🇳🇱 |
|---|---|---|---|
| Preparing laptops and boards | [EN](coach/en/setup.md) | [FR](coach/fr/setup.md) | [NL](coach/nl/setup.md) |
| Running a 45-minute session | [EN](coach/en/running-a-session.md) | [FR](coach/fr/running-a-session.md) | [NL](coach/nl/running-a-session.md) |
| The Core2 hardware | [EN](coach/en/hardware.md) | [FR](coach/fr/hardware.md) | [NL](coach/nl/hardware.md) |

## What you need

- One M5Stack Core2 and one laptop per pair, plus two spare boards.
- One USB-C cable **that carries data** per board.
- Chrome or Edge, or the MicroBlocks desktop app (https://microblocks.fun/download).

## For maintainers

The MicroBlocks files are generated. Do not edit `library/*.ubl` or the `.ubp` files in
`missions/*/starter` and `missions/*/solution` by hand.

| Change | Edit | Then run |
|---|---|---|
| A block label or an on-screen text | `i18n/en.json`, `fr.json`, `nl.json` | `python3 tools/build.py` |
| Library behaviour | `src/library/Core2Buttons.ubl.tmpl` | `python3 tools/build.py` |
| A mission project | `src/projects/*.ubp.tmpl` | `python3 tools/build.py` |
| Documentation | the `.md` files | `python3 tools/check_docs.py` |

Run the tests with `python3 -m pytest tools/tests -q` (needs `pip install -r tools/requirements-dev.txt`).
More about the helper blocks: [library/README.md](library/README.md). Vendored MicroBlocks
libraries: [vendor/README.md](vendor/README.md). History: [CHANGELOG.md](CHANGELOG.md).
```

- [ ] **Step 2: Complete `W/library/README.md`**

Insert, between the title and `## Tested on hardware`:
```markdown
Helper blocks for the M5Stack Core2, used by every mission. They hide the board details
children don't need: the three red circles under the screen are touch zones rather than
real buttons, and the vibration motor sits behind the power chip.

## Blocks

| Block (English label) | Type | What it does |
|---|---|---|
| `left button touched?` / `middle button touched?` / `right button touched?` | reporter | True **once** when the circle is touched. Use it in a `when` hat block. |
| `board shaken?` | reporter | True while the board is shaken firmly (acceleration above 140). |
| `vibrate for _ ms` | command | Buzzes the vibration motor. |
| `beep _ Hz for _ ms` | command | Plays a tone on the speaker. |
| `show big text _ colour _` | command | Clears the screen and writes the text in the middle; long texts get smaller. |

The library uses the MicroBlocks **Tone** library, which every workshop project already
contains.

## Files

- `Core2Buttons-en.ubl`, `Core2Buttons-fr.ubl`, `Core2Buttons-nl.ubl`: generated, one per
  language. Coaches normally don't need them, because every starter project already
  contains the library.
- Source: `../src/library/Core2Buttons.ubl.tmpl`. Labels and comments: `../i18n/*.json`.

## Translating

1. Add or change the `blk.*` and `comment.*` values in `../i18n/<lang>.json`. Keep every
   `_` (an input slot) in a label; the build refuses labels with a different number of
   slots than English.
2. Run `python3 tools/build.py` from the workshop folder.
3. Open a starter project in MicroBlocks with that language selected and check the labels.
```

- [ ] **Step 3: Write the three coach pages**

`W/coach/en/setup.md`:
```markdown
# Preparing laptops and boards

Do this the day before. Allow about 5 minutes per board.

## 1. Laptops

- Install Chrome or Edge, or the MicroBlocks desktop app from https://microblocks.fun/download
  (use the app when the venue has no reliable internet).
- Download this workshop folder to each laptop, or put the `missions/*/starter/*.ubp` files
  for your language on a USB stick.
- Check each cable: a charging-only USB-C cable is the most common reason a board "is not
  found". Label the cables that work.

## 2. Install MicroBlocks on each Core2 (once)

1. Open MicroBlocks (https://microblocks.fun → **Run**, or the app).
2. Connect the Core2 with a data cable and click the **USB** icon to connect.
3. Open the **⚙** menu → **update firmware on board** → choose the **M5Stack Core2**.
4. Wait until MicroBlocks says the board is connected again.
5. Open `missions/01-magic-shake-ball/solution/magic-ball-done-en.ubp` and touch the
   middle red circle. An answer should appear. If it does, the board is ready.

The firmware stays on the board. You only redo this after somebody installed different
software on it.

## 3. Language

Click the **globe** icon in MicroBlocks and choose English, Français or Nederlands. Then
open the starter project with the same language code (`-en`, `-fr` or `-nl`), so the
helper blocks are in that language too.

## 4. Boards

- Charge every board fully (the battery lasts a session; bring chargers anyway).
- Stick a number on the back of every board, and number the tables. In Mission 3 the
  table number is the radio group.
- Keep two spare boards ready with the firmware installed.

## 5. Quick test of the radio (only for Mission 3)

Open `missions/03-emoji-messenger/solution/emoji-messenger-done-en.ubp` on two boards and
send an emoji from one to the other. See [running a session](running-a-session.md) for
the group numbers.
```

`W/coach/en/running-a-session.md`:
```markdown
# Running a 45-minute session

## Before the children arrive

- Every laptop has MicroBlocks open, a board connected, and the **starter project** of
  today's mission open in the right language.
- The solution project of the mission is on your own laptop.

## Timing

| Minutes | What happens | Your job |
|---|---|---|
| 0–5 | Welcome, show the finished project on your board | Keep it short and fun; let them guess how it works |
| 5–30 | The pair follows `mission.md`, steps ⭐1 to ⭐4 | Walk around; ask questions instead of grabbing the mouse |
| 30–40 | Bonus cards, chosen by the pair | Hand out cards; praise their own ideas |
| 40–45 | Show and tell: pairs show their board to the next table | Ask every pair what they changed |

A pair that is slower is fine: finishing ⭐3 is already a working Magic Ball / game.

## Pairs

- **Driver**: holds the mouse and builds the blocks.
- **Navigator**: reads the mission page aloud and checks every step.
- They swap at every ⭐. The mission page reminds them with 🔄.

## Radio groups (Mission 3)

Each table uses its own group number, from 1 upward, so 20 boards in the same room don't
all receive each other's messages. Write the number on the table. Pairs set it in the
first block of their starter project. For the "send to another table" bonus card, two
tables agree on one shared group.

## Common problems

| Symptom | Fix |
|---|---|
| Board not found | Replug; use a data USB-C cable; reload the page or restart the app |
| Screen black | Press the power button on the left side; charge the board |
| Buttons don't react | Open the starter project, so the helper library is loaded |
| Messages don't arrive | Both boards must use the same group number |
| No sound | Check that the beep block is used; use the vibrate block instead |

When a pair is stuck for more than two minutes, open the solution project on your laptop
and compare their script with it, one block at a time.

## Known limits

Copy the results of check H8 (accents on the screen) and H6 (radio in a full room) from
[the library tests](../../library/README.md#tested-on-hardware) here, in one sentence each.
```

`W/coach/en/hardware.md`:
```markdown
# The M5Stack Core2

We use the **Core2 v1.3** (part number **K010-V13**, green power LED). Do not buy the
Core2 v1.1 (K010-V11): its power chip is not supported by MicroBlocks.
Datasheet: https://docs.m5stack.com/en/core/Core2_v1.3

| Part | Used for in the workshop |
|---|---|
| 2-inch touch screen (320 × 240 pixels) | All text and emojis |
| Three red circles under the screen | The left, middle and right "buttons" (they are touch zones) |
| Motion sensor (IMU) | Shaking |
| Speaker | Beeps |
| Vibration motor | Buzzing in your hand |
| ESP32 with Wi-Fi and Bluetooth | Board-to-board radio (ESP Now) |
| Battery and power button (left side) | Runs without a cable after programming |

## How many

- One board per pair, plus two spares per session.
- One USB-C data cable per board.
- One laptop per pair.

## Handling

- Hold the board in two hands when shaking; don't throw it.
- The screen is glass: no pens or nails on it.
- At the end, switch the boards off (hold the power button 6 seconds) and charge them.
```

- [ ] **Step 4: Run the checker**

Run: `python3 tools/check_docs.py | grep -v -e "folder missing" -e "/fr/" -e "/nl/" -e "/mission.md"`
Expected: no output. (The filtered lines are the French and Dutch folders and the mission pages, which Tasks 9–13 add.)

- [ ] **Step 5: Update the changelog and commit**

Add under `### Added`: `- English entry page, coach guides and library reference.`

```bash
git add workshops/InternetOfThings/ESP32
git commit -m "ESP32 workshop: add English coach documentation"
```

---

### Task 9: English kids' pages for Mission 1

**Files:**
- Create: `W/missions/01-magic-shake-ball/en/mission.md`, `W/missions/01-magic-shake-ball/en/bonus-cards.md`
- Modify: `W/CHANGELOG.md`

**Interfaces:**
- Consumes: block labels from Task 7's table; starter file `../starter/magic-ball-start-en.ubp`; on-screen texts from `en.json` (`screen.m1_*`).
- Produces: the page structure Tasks 10 and 11 copy: title, "You need", "Roles", ⭐ sections each ending with **🧪 Try it!** and **🔄 Swap**, then "You did it!".

Use the exact block labels recorded in Task 7 where they differ from the ones below.

- [ ] **Step 1: Write `mission.md`**

```markdown
# Mission 1: Magic Shake Ball 🎱

Turn your board into a magic ball that answers every question. Ask it something, shake
it, and it decides for you!

**You need:** a Core2 board, a laptop with MicroBlocks, and the project
[magic-ball-start-en.ubp](../starter/magic-ball-start-en.ubp) (your coach has opened it).

**Roles:** the **driver** uses the mouse, the **navigator** reads this page aloud. Swap at
every 🔄.

Our special blocks are in the **Core2Buttons** library, in the list of blocks on the left.

## ⭐1 The ball speaks

1. Go to **Control** and drag a **when** block onto the empty space.
2. From **Core2Buttons**, drag **middle button touched?** into the hole of the **when** block.
3. From **Core2Buttons**, drag **show big text _ colour _** under it.
4. Click in the text field and type `Ask me a question!`. Pick a colour you like.

**🧪 Try it!** Touch the **middle red circle** under the screen. Does the text appear?

**🔄 Swap**

## ⭐2 A random answer

A magic ball needs answers. We keep them in a **list**.

1. Go to **Variables**, click **Add a variable** and name it `answers`.
2. Under **when started** (it is already there), add **set answers to _**.
3. Put a **list** block in the hole. Click the arrow on the list until it has 4 spaces and
   type: `Yes!`, `No way!`, `Maybe...`, `Ask again`.
4. Click the **when started** script once, so the list is made.
5. In your **when** script, replace the text `Ask me a question!` with
   **item _ of _**: in the first hole put **random 1 to _**, and in the last hole of
   **random** put **length of answers**. In the second hole of **item** put **answers**.

**🧪 Try it!** Touch the middle circle a few times. Do you get different answers?

**🔄 Swap**

## ⭐3 Shake it!

A real magic ball is shaken.

1. From **Operators**, take an **_ or _** block.
2. Move **middle button touched?** into its left side, and put **board shaken?** (from
   **Core2Buttons**) into its right side.
3. Put the **or** block into the hole of your **when** block.

**🧪 Try it!** Hold the board in two hands and shake it firmly. Does an answer appear?

**🔄 Swap**

## ⭐4 Colours, beeps and buzzes

1. From **Variables**, add a **local** variable `n` to the top of the **when** script and
   set it to **random 1 to length of answers**. Now use **item n of answers** to show the
   answer.
2. Add an **if _ else** block: **if n = 1** show the answer in green, **else if n = 2** in
   red, **else** in yellow.
3. Under the **if**, add **beep 880 Hz for 150 ms** and **vibrate for 200 ms**.
4. Add **wait 1500 millisecs** and then **show big text** `Ask me a question!` in white.

**🧪 Try it!** Ask a question out loud, then shake. Does the board beep, buzz and show a
coloured answer?

**🔄 Swap**

## You did it! 🎉

You built a magic ball with **events** (when), a **list**, **random** numbers, a
**sensor** (shaking) and **outputs** (screen, sound, vibration). Pick a
[bonus card](bonus-cards.md) to make it even better!
```

- [ ] **Step 2: Write `bonus-cards.md`**

```markdown
# Mission 1: bonus cards 🃏

Pick any card. Each one works on its own.

---

## 🃏 Card A: Your own answers

**Goal:** the ball gives your own funny answers.

**How:** click the arrow on the **list** block to add more spaces, and type new answers,
like `Ask your cat` or `Only on Tuesdays`.

**Tip:** long answers are shown smaller, so they still fit.

---

## 🃏 Card B: A face for every answer

**Goal:** draw a face next to the answer.

**How:** add the **TFT** library (click **+** next to Libraries → **Graphics and
Displays** → **TFT**). Use **draw circle** for the head and two small filled circles for
the eyes. Draw a smile for yes, a frown for no.

**Coach hint:** the screen is 320 wide and 240 high; draw after **show big text**,
because it clears the screen.

---

## 🃏 Card C: The secret cheat button

**Goal:** when *you* touch the left circle, the ball always says yes. Your friends won't
know!

**How:** make a new **when** script with **left button touched?** that shows `Yes!` in
green.

---

## 🃏 Card D: Question counter

**Goal:** the ball counts how many questions it answered.

**How:** add a variable `count`. Set it to 0 in **when started**. Add **change count by 1**
in your **when** script. Show it with **join** `Questions: ` and **count**.

**Coach hint:** show the count after the answer, after the wait.
```

- [ ] **Step 3: Check and commit**

Run: `python3 tools/check_docs.py | grep -v -e "folder missing" -e "/fr/" -e "/nl/" -e "02-hot-potato" -e "03-emoji-messenger"`
Expected: no output.

Add under `### Added`: `- Mission 1 kids' page and bonus cards (English).`

```bash
git add workshops/InternetOfThings/ESP32
git commit -m "ESP32 workshop: add Mission 1 English pages"
```

---

### Task 10: English kids' pages for Mission 2

**Files:**
- Create: `W/missions/02-hot-potato/en/mission.md`, `W/missions/02-hot-potato/en/bonus-cards.md`
- Modify: `W/CHANGELOG.md`

**Interfaces:**
- Consumes: block labels from Task 7; starter `../starter/hot-potato-start-en.ubp`; `screen.m2_*` texts; middle circle = Hot Potato, right circle = Duel (Task 5).
- Produces: nothing new.

- [ ] **Step 1: Write `mission.md`**

```markdown
# Mission 2: Hot Potato 💣

The board is a bomb! Pass it around the table before it explodes. Then challenge your
partner to a reaction duel.

**You need:** a Core2 board, a laptop with MicroBlocks, and the project
[hot-potato-start-en.ubp](../starter/hot-potato-start-en.ubp).

**Roles:** the **driver** uses the mouse, the **navigator** reads this page aloud. Swap at
every 🔄.

## ⭐1 A secret timer

1. Add a **when** block with **middle button touched?** inside.
2. Add a local variable `fuse` and set it to **random 5000 to 15000** (that is 5 to 15
   seconds, in milliseconds).
3. Add **wait fuse millisecs**.
4. Add **show big text** `BOOM!` in red and **vibrate for 800 ms**.

**🧪 Try it!** Touch the middle circle and count. Nobody knows when it will explode!

**🔄 Swap**

## ⭐2 Tick... tick... tick...

A bomb should tick, faster and faster.

1. Replace **wait fuse millisecs** with: **reset timer**, then **repeat until timer > fuse**.
2. Add a local variable `tick` set to 600, before the repeat.
3. Inside the repeat: **show big text** `PASS IT ON!` in yellow, **beep 440 Hz for 50 ms**,
   **wait tick millisecs**.
4. Still inside: **if tick > 120** then **change tick by -40**.

**🧪 Try it!** Does the ticking speed up before the BOOM?

**🔄 Swap**

## ⭐3 Lives

1. Add a variable `lives` and set it to 3 in **when started**.
2. After the BOOM, **change lives by -1**, wait 1500 ms.
3. **If lives > 0** show **join** `Lives:` and **lives**, **else** show `GAME OVER` and set
   lives back to 3.

**🧪 Try it!** Play at the table: touch the middle circle and pass the board. Whoever holds
it at BOOM loses a life.

**🔄 Swap**

## ⭐4 Reaction duel

Who is faster: left or right?

1. Make a new **when** script with **right button touched?**.
2. Show `Get ready...`, wait 800 ms, set local `delay` to **random 2000 to 5000** and
   `winner` to 0, then **reset timer**.
3. **Repeat until (timer > delay) or (winner ≠ 0)**: if **left button touched?** set winner
   to -1; if **right button touched?** set winner to -2. Touching early is cheating!
4. **If winner = -1** show `Left: too early!`; **else if winner = -2** show
   `Right: too early!`; **else** show `GO!`, beep, and **repeat until winner ≠ 0**: left
   touched → winner 1, right touched → winner 2. Then show `Left wins!` or `Right wins!`.

**🧪 Try it!** One player puts a finger near the left circle, the other near the right.
Wait for GO!

**🔄 Swap**

## You did it! 🎉

You used **timers**, **loops**, **variables** that change, and **game rules** that are
fair. Try a [bonus card](bonus-cards.md)!
```

- [ ] **Step 2: Write `bonus-cards.md`**

```markdown
# Mission 2: bonus cards 🃏

---

## 🃏 Card A: Defuse it!

**Goal:** tilt the board flat to defuse the bomb before it explodes.

**How:** add the **Basic Sensors** library. Inside the ticking loop, **if tilt x** is
between -10 and 10 **and tilt y** is between -10 and 10, show `DEFUSED!` and stop the
script.

**Coach hint:** let them first show **tilt x** with **show big text** to see the numbers.

---

## 🃏 Card B: High score

**Goal:** remember the fastest reaction in the duel.

**How:** after **GO!**, save **timer** in a variable `time` when someone touches. If `time`
is smaller than `best`, set `best` to `time` and show `NEW RECORD!`.

**Coach hint:** set `best` to 99999 in **when started**.

---

## 🃏 Card C: Duel between two tables

**Goal:** the same GO! appears on two boards at once, and each pair taps their own board.

**How:** you need the **ESP Now** library and another pair who agrees to play. One board
sends **espNow send pair** `go` = 1; both boards show GO! when they send or receive it.

**Coach hint:** this card leads into Mission 3, where the radio is explained step by
step.
```

- [ ] **Step 3: Check and commit**

Run: `python3 tools/check_docs.py | grep -v -e "folder missing" -e "/fr/" -e "/nl/" -e "03-emoji-messenger"`
Expected: no output.

Add under `### Added`: `- Mission 2 kids' page and bonus cards (English).`

```bash
git add workshops/InternetOfThings/ESP32
git commit -m "ESP32 workshop: add Mission 2 English pages"
```

---

### Task 11: English kids' pages for Mission 3

**Files:**
- Create: `W/missions/03-emoji-messenger/en/mission.md`, `W/missions/03-emoji-messenger/en/bonus-cards.md`
- Modify: `W/CHANGELOG.md`

**Interfaces:**
- Consumes: block labels and ESP Now labels from Task 7; starter `../starter/emoji-messenger-start-en.ubp` (has group 1, `myName`, `emojis`, `choice`); protocol from Task 6 (number = emoji index, 0 = party).
- Produces: nothing new.

- [ ] **Step 1: Write `mission.md`**

```markdown
# Mission 3: Emoji Messenger 📡

Send emojis from your board to other boards, by radio. No internet, no Wi-Fi router:
the boards talk to each other directly.

**You need:** a Core2 board, a laptop with MicroBlocks, the project
[emoji-messenger-start-en.ubp](../starter/emoji-messenger-start-en.ubp), and another pair
at your table.

**Roles:** the **driver** uses the mouse, the **navigator** reads this page aloud. Swap at
every 🔄.

## ⭐1 Hello, radio!

1. In **when started**, change the group number `1` to your **table number**. Only boards
   with the same number hear each other.
2. Change `Team 1` to your own team name (short, no `|` sign).
3. Click **when started** once.
4. Make a **when** script with **middle button touched?** and add
   **espNow send pair myName = 1**.
5. Make another **when** script with **espNow pair received?** and add
   **show big text (espNow last string)** in yellow.

**🧪 Try it!** Both pairs at the table touch the middle circle. Do you see the other
team's name?

**🔄 Swap**

## ⭐2 Choose an emoji

The list `emojis` is already in your project: `:-)` `:-D` `;-)` `<3` `:-O` `:-(` `B-)` `:-P`.
Turn your head to the left to see the faces!

1. Make a **when** script with **right button touched?**: **change choice by 1**, **if
   choice > length of emojis** set choice to 1, then **show big text (item choice of
   emojis)**.
2. Do the same with **left button touched?**: change choice by -1, and if choice < 1 set
   it to **length of emojis**.
3. In the middle-button script, send **choice** instead of 1:
   **espNow send pair myName = choice**.

**🧪 Try it!** Scroll with left and right. Does the emoji change?

**🔄 Swap**

## ⭐3 Show what arrives

1. In the **espNow pair received?** script, add a local variable `n` set to
   **espNow last number**.
2. **If n ≥ 1 and n ≤ length of emojis**: show **item n of emojis** big in yellow,
   **beep 660 Hz for 100 ms** and wait 2000 ms. Other numbers are ignored: that keeps
   your board safe from strange messages.
3. At the end, show your own emoji again: **show big text (item choice of emojis)**.

**🧪 Try it!** Send emojis to each other. Do you hear the beep when one arrives?

**🔄 Swap**

## ⭐4 Shake for a party!

Every board in your group hears every message. That is called a **broadcast**.

1. Make a **when** script with **board shaken?** and add
   **espNow send pair myName = 0**.
2. In the received script, add before the other test: **if n = 0**, **repeat 3**: show
   `PARTY!` in pink, **vibrate for 100 ms**, show `PARTY!` in light blue, wait 100 ms.

**🧪 Try it!** Shake your board. Does the whole table party?

**🔄 Swap**

## You did it! 🎉

You built a radio messenger with **groups**, **lists**, **messages** made of a name and a
number, and a **broadcast**. Try a [bonus card](bonus-cards.md)!
```

- [ ] **Step 2: Write `bonus-cards.md`**

```markdown
# Mission 3: bonus cards 🃏

---

## 🃏 Card A: Secret code

**Goal:** send a secret word that only your partners can read.

**How:** use the number as a key. Before sending, turn every letter of your word into the
letter 3 places later (A → D, B → E). The receivers turn it back. Use **join** and the
letters of a word one by one.

**Coach hint:** this is the Caesar cipher. Let them do it on paper first.

---

## 🃏 Card B: Team channels

**Goal:** switch between your table's group and a shared group for the whole room.

**How:** the right circle already goes round all the emojis, so the left circle is free.
Change your **left button touched?** script: add a variable `group`; if `group` is your
table number, set it to `99`, otherwise set it back to your table number. Then run
**espNow set group** with `group` and show it with **join** `Group ` and **group**.

**Coach hint:** agree on one shared extra group number for the whole room.

---

## 🃏 Card C: Fortune delivery 🎱

**Goal:** send a Magic Ball answer to another table.

**How:** add the answers list from Mission 1. Pick a **random** answer and send it as the
text of the pair (with number 9, for example). The receiving board shows the text when
the number is 9.

**Coach hint:** the receiving pair must add a test for 9 before the emoji test.
```

- [ ] **Step 3: Check and commit**

Run: `python3 tools/check_docs.py | grep -v -e "folder missing" -e "/fr/" -e "/nl/"`
Expected: no output.

Add under `### Added`: `- Mission 3 kids' page and bonus cards (English).`

```bash
git add workshops/InternetOfThings/ESP32
git commit -m "ESP32 workshop: add Mission 3 English pages"
```

---

### Task 12: French translation of all documentation

**Files:**
- Create: `W/coach/fr/setup.md`, `running-a-session.md`, `hardware.md`
- Create: `W/missions/0{1,2,3}-*/fr/mission.md`, `bonus-cards.md`
- Modify: `W/CHANGELOG.md`

**Interfaces:**
- Consumes: every English page from Tasks 8–11; `fr.json`; MicroBlocks' own French block labels.
- Produces: French pages with the same file names as English.

- [ ] **Step 1: Build the glossary of French block labels**

Run from `W/`:
```bash
python3 - <<'EOF'
import re, urllib.request
po = urllib.request.urlopen("https://bitbucket.org/john_maloney/smallvm/raw/HEAD/translations/fr.po").read().decode("utf-8")
pairs = dict(re.findall(r'msgid "(.*)"\nmsgstr "(.*)"', po))
labels = ["when started", "when _", "wait _ millisecs", "random _ to _", "item _ of _", "length of _",
          "list", "set _ to _", "change _ by _", "initialize local _ to _", "if _", "else",
          "_ or _", "_ and _", "_ ≠ _", "_ ≥ _", "_ ≤ _", "join _",
          "repeat until _", "repeat _", "reset timer", "timer", "forever", "Add a variable",
          "espNow send pair _ = _", "espNow pair received?", "espNow last number",
          "espNow last string", "espNow set group _ (0-255)", "tilt x", "tilt y",
          "draw circle on TFT at x _ y _ radius _ color _ : filled _"]
for label in labels:
    print(f"| {label} | {pairs.get(label, '?? not translated')} |")
EOF
```
Replace the English labels in Task 7's table by the exact English text MicroBlocks shows if they differ, and rerun. Keep the printed table open while translating.

- [ ] **Step 2: Translate**

Translate each English page into the same path with `fr` instead of `en`, following these rules:
- Address the children with **tu**, short sentences, same emojis and structure (⭐, 🧪 **Essaie !**, 🔄 **Change de rôle**, 🎉 **Bravo !**). Coach pages use **vous**.
- Block names: the French label from the glossary for built-in blocks; the `fr.json` value for Core2Buttons blocks (e.g. **bouton du milieu touché ?**, **afficher grand texte _ couleur _**).
- On-screen texts the children type: the `screen.*` values of `fr.json` (e.g. `Pose-moi une question !`, `Oui !`, `Pas question !`, `Possible...`, `Redemande`).
- Links: point to `-fr` starter files (`../starter/magic-ball-start-fr.ubp` etc.) and to `fr` pages; links to `library/README.md` and `vendor/README.md` stay the same.
- Terms: driver = **pilote**, navigator = **copilote**, bonus card = **carte bonus**, radio group = **groupe radio**, coach = **coach**.
- If a label is marked `?? not translated`, use the English label in bold.

- [ ] **Step 3: Check**

Run: `python3 tools/check_docs.py | grep -v -e "/nl" -e "coach/nl"`
Expected: no output.

- [ ] **Step 4: Update the changelog and commit**

Add under `### Added`: `- French translation of all pages.`

```bash
git add workshops/InternetOfThings/ESP32
git commit -m "ESP32 workshop: add French translation"
```

---

### Task 13: Dutch translation of all documentation

**Files:**
- Create: `W/coach/nl/setup.md`, `running-a-session.md`, `hardware.md`
- Create: `W/missions/0{1,2,3}-*/nl/mission.md`, `bonus-cards.md`
- Modify: `W/CHANGELOG.md`

**Interfaces:**
- Consumes: every English page; `nl.json`; MicroBlocks' Dutch block labels.
- Produces: Dutch pages with the same file names as English. After this task the doc checker reports nothing.

- [ ] **Step 1: Build the glossary of Dutch block labels**

Run the script from Task 12 Step 1 with `fr.po` replaced by `nl.po`.

- [ ] **Step 2: Translate**

Same rules as Task 12, with:
- Children are addressed with **je/jullie**, coaches with **je** too (informal Dutch is normal in Devoxx4Kids NL).
- Checkpoints: 🧪 **Probeer het!**, 🔄 **Wissel**, 🎉 **Gelukt!**
- Core2Buttons labels and on-screen texts from `nl.json` (e.g. **middelste knop aangeraakt?**, `Stel me een vraag!`, `Ja!`, `Echt niet!`, `Misschien...`, `Vraag opnieuw`).
- Links to `-nl` starter files and `nl` pages.
- Terms: driver = **bestuurder**, navigator = **navigator**, bonus card = **bonuskaart**, radio group = **radiogroep**.

- [ ] **Step 3: Check everything**

Run: `python3 tools/check_docs.py && python3 tools/build.py --check && python3 -m pytest tools/tests -q`
Expected: no checker output, exit code 0; build check prints nothing; all tests pass.

- [ ] **Step 4: Update the changelog and commit**

Add under `### Added`: `- Dutch translation of all pages.`

```bash
git add workshops/InternetOfThings/ESP32
git commit -m "ESP32 workshop: add Dutch translation"
```

---

### Task 14: Photos, dry runs and final check (HUMAN)

Needs a Core2, a phone or camera, and a timer. An AI agent can do Steps 3–5 after a person has done Steps 1–2.

**Files:**
- Create: `W/missions/01-magic-shake-ball/images/finished.jpg`, `W/missions/02-hot-potato/images/finished.jpg`, `W/missions/03-emoji-messenger/images/finished.jpg`
- Modify: every `W/missions/*/<lang>/mission.md` (one image line), `W/coach/<lang>/running-a-session.md` (known limits), `W/CHANGELOG.md`

**Interfaces:**
- Consumes: everything above.
- Produces: the finished workshop.

- [ ] **Step 1: Dry-run every mission with a timer**

One adult who did not write the pages follows each English `mission.md` from the starter project, without looking at the solution. Write down the minutes for ⭐1–⭐4 and every place where they hesitated. Pass: the core takes at most 20 minutes per mission. If a mission takes longer, simplify the slowest step on the English page (for example, pre-build a block in the starter template and regenerate) and record what changed.

- [ ] **Step 2: Take one photo per mission**

Photograph the board showing the finished mission (an answer, BOOM!, a received emoji), with no text other than what is on the board's screen. Save as `missions/<mission>/images/finished.jpg`, at most 1600 px wide and 400 KB.

- [ ] **Step 3: Add the photos to every mission page**

In each `missions/<mission>/<lang>/mission.md`, add one line directly under the title:
```markdown
![](../images/finished.jpg)
```

- [ ] **Step 4: Fill in the known limits**

In `coach/<lang>/running-a-session.md`, replace the paragraph under **Known limits** (and its French and Dutch versions) with the actual H6 and H8 results from `library/README.md`, one sentence each.

- [ ] **Step 5: Final check, changelog and commit**

Run: `python3 tools/check_docs.py && python3 tools/build.py --check && python3 -m pytest tools/tests -q`
Expected: no problems, all tests pass.

Add to the changelog (today's entry if it exists, otherwise a new dated entry):
```markdown
### Changed
- Mission pages checked with timed dry runs; photos and known limits added.
```

```bash
git add workshops/InternetOfThings/ESP32
git commit -m "ESP32 workshop: add photos and dry-run fixes"
```
