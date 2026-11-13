# ESP32 Workshop, Part 2: Bomb Mission, Image Firmware and Closing the Hardware Test — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace Mission 2 (Hot Potato) with the Bomb mission, using Noto animated images drawn on the Core2 v1.3, ship the images together with the patched MicroBlocks firmware, close the hardware test, and update the remaining documentation tasks of the first plan.

**Architecture:** A Pillow-based maintainer tool converts the two Noto GIFs into raw 8-bit frame files plus a generated library part (shared 256-colour palette and frame table). The frame files go into a LittleFS image that is flashed next to the patched firmware. Three new `Core2Buttons` blocks draw the frames row by row from those files (`[file:readBytes]` + `[tft:pixelRow]`), so no frame is ever held in the board's 37 KB object store. The Bomb starter and solution projects are generated like the other missions.

**Tech Stack:** MicroBlocks pilot (VM 424) + Devoxx4Kids Core2 v1.3 firmware patch, Python 3.9+, Pillow (maintainer tool only), pytest, PlatformIO, esptool, Markdown.

**Spec:** `docs/superpowers/specs/2026-11-11-esp32-magic-ball-workshop-design.md` (Mission 2 Bomb amendment, Images and Bomb spike sections, platform status of 2026-11-13).
**First plan (still valid for its remaining tasks, amended by Task 7 here):** `docs/superpowers/plans/2026-11-11-esp32-magic-ball-workshop.md`.

## Global Constraints

All Global Constraints of the first plan apply, with these additions and one change:

- Workshop root: `workshops/InternetOfThings/ESP32/` (`W/` below). Tests: `python3 -m pytest tools/tests -q` from `W/`.
- **Changed:** `tools/build.py` and `tools/check_docs.py` stay standard-library only. `tools/convert_images.py` may use **Pillow**; it is a maintainer tool whose outputs are committed, so workshop users never run it. Add `Pillow>=10` to `tools/requirements-dev.txt`.
- Image licence: Noto Animated Emoji by Google, **CC BY 4.0**. Credit text, verbatim: "Bomb and explosion animations: Noto Animated Emoji by Google, CC BY 4.0 (https://googlefonts.github.io/noto-emoji-animation/)".
- Frame sets (from the spec): calm = bomb frame 6; nervous = bomb frames 10–21; safe = bomb frames from 25 (confetti); explode = 💥 collision. Sizes: calm and nervous 140 px, explode and safe 200 px.
- Danger meter (spec): nervous at 50, explode at 100; starting values, tuned in Task 5.
- Children carry the board with two hands, walking; this text appears in the coach docs.
- Board firmware: our patched MicroBlocks build, base `b40b74d` of `codeberg.org/MicroBlocks/smallvm` (`dev`), patch `W/firmware/microblocks-core2-v1.3.patch`.
- Commit messages: no `Co-Authored-By`, no "Generated with Claude Code", no GitHub mentions.
- `W/CHANGELOG.md`: one version entry per day; add to the existing entry for the day.

## Review Focus

1. The firmware is flashed **without** `bomb-images.bin` (a coach skips the second file) → the bomb blocks draw nothing, but the program keeps running and the danger meter, beeps, texts and buzz still work. Pinned by: Task 5 check B5.
2. The board is jolted while a frame is being drawn (the loop samples `jolt` less often while drawing) → a clumsy walk must still reach 100; a careful one must stay below 50. Pinned by: Task 5 checks B3–B4 (tuning).
3. The middle circle is touched again after BOOM or SAFE → a new round starts cleanly (danger 0, timer reset, calm bomb). Pinned by: Task 3 test `test_bomb_restart_resets_the_round`.
4. A translator gives two bomb menu items the same word (e.g. FR "calme" twice) → the wrong picture would show. Pinned by: Task 2 test `test_bomb_menu_items_are_distinct`.
5. A conversion bug writes frames whose byte count is not size × size → garbled pictures. Pinned by: Task 1 test `test_frames_are_size_squared_bytes`.

---

## File map

| File | Responsibility | Task |
|---|---|---|
| `W/src/images/noto-bomb.gif`, `noto-collision.gif`, `README.md` | Source animations and their licence | 1 |
| `W/tools/convert_images.py` | GIFs → frame files + generated library part | 1 |
| `W/tools/tests/test_convert_images.py` | Tests on synthetic GIFs | 1 |
| `W/firmware/images/bomb_<set>_<n>.data` | Raw 8-bit frames (generated, committed) | 1 |
| `W/src/library/BombAssets.ubl.part` | Generated: `_c2b_bombPalette`, `_c2b_bombSet` | 1 |
| `W/tools/build.py` | Includes `BombAssets` into the library | 2 |
| `W/src/library/Core2Buttons.ubl.tmpl`, `W/i18n/*.json` | `show bomb`, `jolt`, `show danger bar` | 2 |
| `W/src/projects/bomb-start.ubp.tmpl`, `bomb-done.ubp.tmpl` | Mission 2 projects | 3 |
| `W/missions/02-bomb/…` (generated) | Replaces `W/missions/02-hot-potato/` (deleted) | 3 |
| `W/firmware/build.sh`, `W/firmware/bomb-images.bin`, `W/firmware/README.md` | Reproducible firmware + image build | 4 |
| `W/library/README.md` | Hardware results, decision, Bomb spike values | 5, 6 |
| `docs/superpowers/plans/2026-11-11-esp32-magic-ball-workshop.md` | Remaining tasks amended | 7 |

---

### Task 1: Image conversion tool and frame files

**Files:**
- Create: `W/src/images/noto-bomb.gif`, `W/src/images/noto-collision.gif`, `W/src/images/README.md`
- Create: `W/tools/convert_images.py`, `W/tools/tests/test_convert_images.py`
- Generated (commit): `W/firmware/images/*.data`, `W/src/library/BombAssets.ubl.part`
- Modify: `W/tools/requirements-dev.txt`, `W/CHANGELOG.md`

**Interfaces:**
- Consumes: nothing.
- Produces:
  - `convert_images.FRAMESETS: dict[str, tuple[str, list[int], int]]` = `{set_name: (gif_file_name, frame_indices, size_px)}`.
  - `convert_images.convert(src_dir: Path, out_dir: Path, part_path: Path, framesets=FRAMESETS) -> list[Path]` (written frame files).
  - Frame files named `bomb_<set>_<n>.data`, `n` from 1; each exactly `size * size` bytes of palette indices, row by row from the top.
  - `BombAssets.ubl.part` defines two MicroBlocks functions: `'_c2b_bombPalette'` → list of 256 RGB integers (index 0 = black `0`), and `'_c2b_bombSet' name` → `('[data:makeList]' frameCount sizePx)` for `name` in `calm`, `nervous`, `explode`, `safe`, otherwise `('[data:makeList]' 0 0)`.

- [ ] **Step 1: Add the source images and their licence note**

From `W/`:
```bash
mkdir -p src/images
curl -fsSL https://fonts.gstatic.com/s/e/notoemoji/latest/1f4a3/512.gif -o src/images/noto-bomb.gif
curl -fsSL https://fonts.gstatic.com/s/e/notoemoji/latest/1f4a5/512.gif -o src/images/noto-collision.gif
shasum -a 256 src/images/*.gif
```
(If shell `curl` is blocked in your environment, download the same URLs with any HTTP client.)

`W/src/images/README.md` (put the two checksums in the table):
```markdown
# Source images

| File | What | Source |
|---|---|---|
| `noto-bomb.gif` | 💣 bomb, 67 frames, 512 × 512 | https://fonts.gstatic.com/s/e/notoemoji/latest/1f4a3/512.gif |
| `noto-collision.gif` | 💥 collision, 38 frames, 512 × 512 | https://fonts.gstatic.com/s/e/notoemoji/latest/1f4a5/512.gif |

Bomb and explosion animations: Noto Animated Emoji by Google, CC BY 4.0
(https://googlefonts.github.io/noto-emoji-animation/). Licence text:
https://creativecommons.org/licenses/by/4.0/

The frames used by the workshop are made with `python3 tools/convert_images.py`.
```

- [ ] **Step 2: Write the failing tests**

`W/tools/tests/test_convert_images.py`:
```python
from pathlib import Path

import pytest

PIL = pytest.importorskip("PIL")
from PIL import Image  # noqa: E402

import convert_images  # noqa: E402


def make_gif(path: Path, colors) -> None:
    frames = [Image.new("RGBA", (32, 32), c) for c in colors]
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=50, loop=0)


@pytest.fixture
def sources(tmp_path):
    src = tmp_path / "src"
    src.mkdir()
    make_gif(src / "a.gif", [(255, 0, 0, 255), (0, 255, 0, 255), (0, 0, 255, 255)])
    make_gif(src / "b.gif", [(255, 255, 0, 255), (0, 0, 0, 0)])
    return src


FRAMESETS = {"calm": ("a.gif", [0], 8), "nervous": ("a.gif", [1, 2], 8), "explode": ("b.gif", [0, 1], 12)}


def run(sources, tmp_path):
    out = tmp_path / "out"
    part = tmp_path / "BombAssets.ubl.part"
    written = convert_images.convert(sources, out, part, FRAMESETS)
    return out, part, written


def test_writes_one_file_per_frame(sources, tmp_path):
    out, _, written = run(sources, tmp_path)
    assert sorted(p.name for p in written) == [
        "bomb_calm_1.data", "bomb_explode_1.data", "bomb_explode_2.data",
        "bomb_nervous_1.data", "bomb_nervous_2.data",
    ]
    assert all(p.parent == out for p in written)


def test_frames_are_size_squared_bytes(sources, tmp_path):
    out, _, _ = run(sources, tmp_path)
    assert len((out / "bomb_calm_1.data").read_bytes()) == 8 * 8
    assert len((out / "bomb_explode_2.data").read_bytes()) == 12 * 12


def test_transparent_pixels_become_black():
    clear = Image.new("RGBA", (16, 16), (255, 0, 0, 0))
    rendered = convert_images.render(clear, 8)
    assert rendered.size == (8, 8)
    assert set(rendered.getdata()) == {(0, 0, 0)}


def test_part_defines_palette_and_frame_table(sources, tmp_path):
    _, part, _ = run(sources, tmp_path)
    text = part.read_text(encoding="utf-8")
    assert "to '_c2b_bombPalette' {" in text
    assert "to '_c2b_bombSet' name {" in text
    assert "if (name == 'nervous') {\n    return ('[data:makeList]' 2 8)\n  }" in text
    assert "if (name == 'explode') {\n    return ('[data:makeList]' 2 12)\n  }" in text
    hex_line = next(line for line in text.splitlines() if line.strip().startswith("local 'hex'"))
    hex_digits = hex_line.split("'")[3]
    assert len(hex_digits) == 256 * 6
    assert hex_digits.startswith("000000")


def test_red_pixels_map_to_a_red_palette_entry(sources, tmp_path):
    out, part, _ = run(sources, tmp_path)
    text = part.read_text(encoding="utf-8")
    hex_digits = next(l for l in text.splitlines() if "local 'hex'" in l).split("'")[3]
    index = (out / "bomb_calm_1.data").read_bytes()[0]
    r = int(hex_digits[index * 6:index * 6 + 2], 16)
    g = int(hex_digits[index * 6 + 2:index * 6 + 4], 16)
    assert r > 200 and g < 60
```

Add to `W/tools/requirements-dev.txt`:
```
Pillow>=10
```

- [ ] **Step 3: Run the tests to verify they fail**

Run: `python3 -m pip install -r tools/requirements-dev.txt && python3 -m pytest tools/tests/test_convert_images.py -q`
Expected: collection error `ModuleNotFoundError: No module named 'convert_images'`.

- [ ] **Step 4: Write the implementation**

`W/tools/convert_images.py`:
```python
#!/usr/bin/env python3
"""Convert the Noto bomb animations into frame files for the Core2 and a library part.

Usage (from the workshop folder):
    python3 tools/convert_images.py

Reads src/images/*.gif and writes:
- firmware/images/bomb_<set>_<n>.data: one raw frame, size*size palette indices, row by row
- src/library/BombAssets.ubl.part: the shared 256-colour palette and the frame table,
  included into the Core2Buttons library by tools/build.py

Maintainer tool: needs Pillow. Its outputs are committed.
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageSequence

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "images"
OUT = ROOT / "firmware" / "images"
PART = ROOT / "src" / "library" / "BombAssets.ubl.part"

# set name: (source GIF, frame indices, size in pixels)
FRAMESETS: dict[str, tuple[str, list[int], int]] = {
    "calm": ("noto-bomb.gif", [6], 140),
    "nervous": ("noto-bomb.gif", [10, 12, 14, 16, 18, 20], 140),
    "explode": ("noto-collision.gif", [0, 4, 8, 12, 16, 20, 26, 32], 200),
    "safe": ("noto-bomb.gif", [25, 28, 31, 34, 37, 40], 200),
}


def load_frames(path: Path) -> list[Image.Image]:
    return [frame.convert("RGBA") for frame in ImageSequence.Iterator(Image.open(path))]


def render(frame: Image.Image, size: int) -> Image.Image:
    """The frame scaled to size x size on a black background (the Core2 screen colour)."""
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 255))
    canvas.alpha_composite(frame.resize((size, size), Image.LANCZOS))
    return canvas.convert("RGB")


def build_palette(images: list[Image.Image]) -> Image.Image:
    """A 'P' image whose palette has black at index 0 and 255 colours for the frames."""
    strip = Image.new("RGB", (sum(i.width for i in images), max(i.height for i in images)))
    x = 0
    for image in images:
        strip.paste(image, (x, 0))
        x += image.width
    quantized = strip.quantize(colors=255, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    colors = quantized.getpalette()[: 255 * 3]
    colors += [255, 0, 255] * (255 - len(colors) // 3)  # unused entries: magenta, never black
    palette_image = Image.new("P", (1, 1))
    palette_image.putpalette([0, 0, 0] + colors)
    return palette_image


def to_indices(image: Image.Image, palette_image: Image.Image) -> bytes:
    return image.quantize(palette=palette_image, dither=Image.Dither.NONE).tobytes()


def palette_hex(palette_image: Image.Image) -> str:
    values = palette_image.getpalette()[: 256 * 3]
    values += [0] * (256 * 3 - len(values))
    return "".join(f"{v:02x}" for v in values)


def part_text(hex_digits: str, framesets: dict[str, tuple[str, list[int], int]]) -> str:
    lines = [
        "to '_c2b_bombPalette' {",
        "  comment 'Generated by tools/convert_images.py: 256 colours, 6 hex digits each.'",
        f"  local 'hex' '{hex_digits}'",
        "  local 'result' ('[data:makeList]')",
        "  for i 256 {",
        "    '[data:addLast]' (hexToInt ('[data:copyFromTo]' hex ((i * 6) - 5) (i * 6))) result",
        "  }",
        "  return result",
        "}",
        "",
        "to '_c2b_bombSet' name {",
        "  comment 'Generated by tools/convert_images.py: frame count and size in pixels per set.'",
    ]
    for name, (_, indices, size) in framesets.items():
        lines += [f"  if (name == '{name}') {{", f"    return ('[data:makeList]' {len(indices)} {size})", "  }"]
    lines += ["  return ('[data:makeList]' 0 0)", "}", ""]
    return "\n".join(lines)


def convert(src_dir: Path = SRC, out_dir: Path = OUT, part_path: Path = PART, framesets=FRAMESETS) -> list[Path]:
    cache: dict[str, list[Image.Image]] = {}
    rendered: dict[str, list[Image.Image]] = {}
    for name, (gif, indices, size) in framesets.items():
        frames = cache.setdefault(gif, load_frames(src_dir / gif))
        rendered[name] = [render(frames[i], size) for i in indices]
    palette_image = build_palette([image for images in rendered.values() for image in images])
    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("bomb_*.data"):
        old.unlink()
    written = []
    for name, images in rendered.items():
        for n, image in enumerate(images, start=1):
            path = out_dir / f"bomb_{name}_{n}.data"
            path.write_bytes(to_indices(image, palette_image))
            written.append(path)
    part_path.parent.mkdir(parents=True, exist_ok=True)
    part_path.write_text(part_text(palette_hex(palette_image), framesets), encoding="utf-8")
    return written


def main() -> int:
    written = convert()
    total = sum(p.stat().st_size for p in written)
    print(f"wrote {len(written)} frames ({total // 1024} KB) and {PART.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 5: Run the tests to verify they pass**

Run: `python3 -m pytest tools/tests -q`
Expected: all tests pass (the 5 new ones included).

- [ ] **Step 6: Convert the real images**

Run: `python3 tools/convert_images.py`
Expected: `wrote 21 frames (748 KB) and src/library/BombAssets.ubl.part` (the KB figure may differ slightly).

- [ ] **Step 7: Update the changelog and commit**

Add under today's `### Added`: `- Bomb images (Noto Animated Emoji, CC BY 4.0) converted to Core2 frames by tools/convert_images.py.`

```bash
git add workshops/InternetOfThings/ESP32
git commit -m "ESP32 workshop: convert Noto bomb animations into Core2 frame files"
```

---

### Task 2: Bomb blocks in the Core2Buttons library

**Files:**
- Modify: `W/tools/build.py`, `W/src/library/Core2Buttons.ubl.tmpl`, `W/i18n/en.json`, `fr.json`, `nl.json`
- Modify: `W/tools/tests/test_build.py`, `W/tools/tests/test_generated.py`, `W/CHANGELOG.md`
- Generated: `W/library/Core2Buttons-*.ubl` and all mission projects

**Interfaces:**
- Consumes: `BombAssets.ubl.part` functions `'_c2b_bombPalette'` and `'_c2b_bombSet' name` (Task 1).
- Produces (used by Task 3 templates):
  - `c2b_showBomb state` — `state` is one of the four translated menu labels `{{menu.bomb_calm}}`, `{{menu.bomb_nervous}}`, `{{menu.bomb_explode}}`, `{{menu.bomb_safe}}`. Calm draws one frame; each call with nervous draws the next nervous frame; explode and safe clear the screen and play their set once.
  - `(c2b_jolt)` — reporter: `|acceleration − 100|`.
  - `c2b_dangerBar value` — bar along the bottom 16 px; green < 50, orange 50–99, red ≥ 100.
  - `build.LIBRARY_PARTS = ("BombAssets",)`, read from `src/library/<name>.ubl.part` and included into the library template with `{{> BombAssets}}`.

- [ ] **Step 1: Write the failing tests**

Append to `W/tools/tests/test_build.py`:
```python
def test_library_parts_are_included_into_the_library(tmp_path):
    projects = make_workshop(tmp_path)
    write(tmp_path / "src/library/Core2Buttons.ubl.tmpl", "module Core2Buttons Input\n{{> BombAssets}}\n")
    write(tmp_path / "src/library/BombAssets.ubl.part", "to '_c2b_bombSet' name {\n}\n")
    build.build(tmp_path, projects)
    assert "to '_c2b_bombSet' name {" in (tmp_path / "library/Core2Buttons-en.ubl").read_text(encoding="utf-8")
```
In `make_workshop` in the same file, add one line before `return`, so every fixture workshop has the part:
```python
    write(root / "src/library/BombAssets.ubl.part", "")
```

Append to `W/tools/tests/test_generated.py`:
```python
BOMB_MENU = ("menu.bomb_calm", "menu.bomb_nervous", "menu.bomb_explode", "menu.bomb_safe")


def strings(lang):
    return json.loads((build.ROOT / "i18n" / f"{lang}.json").read_text(encoding="utf-8"))


def test_bomb_blocks_are_defined(files):
    text = library(files)
    for name in ("c2b_showBomb", "c2b_jolt", "c2b_dangerBar"):
        assert re.search(r"^\s*spec '[ r]' '" + name + "' ", text, re.MULTILINE), name
    assert "to '_c2b_bombPalette' {" in text and "to '_c2b_bombSet' name {" in text


def test_bomb_menu_lists_the_four_translated_states(files):
    for lang in build.LANGS:
        s = strings(lang)
        choices = next(l for l in library(files, lang).splitlines() if l.startswith("choices c2b_bombMenu"))
        for key in BOMB_MENU:
            assert "'" + build.escape(s[key]) + "'" in choices, (lang, key)
            assert "(state == '" + build.escape(s[key]) + "')" in body(library(files, lang), "c2b_showBomb"), (lang, key)


def test_bomb_menu_items_are_distinct():
    for lang in build.LANGS:
        s = strings(lang)
        labels = [s[k] for k in BOMB_MENU]
        assert len(set(labels)) == 4, lang


def test_frames_are_drawn_row_by_row_from_files(files):
    draw = body(library(files), "_c2b_drawFrame")
    assert "'[file:open]' file" in draw
    assert "'[tft:pixelRow]' ('[file:readBytes]' size file) x y 1 _c2b_palette" in draw
    assert "'[file:close]' file" in draw


def test_jolt_is_distance_from_one_g(files):
    assert "(absoluteValue (('[sensors:acceleration]') - 100))" in body(library(files), "c2b_jolt")
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m pytest tools/tests -q`
Expected: `test_library_parts_are_included_into_the_library` fails with `BuildError: unknown include: BombAssets` or a missing-text assertion, and the five new `test_generated.py` tests fail (`spec ... c2b_showBomb` not found).

- [ ] **Step 3: Teach the build tool about library parts**

In `W/tools/build.py`, after the line `VENDORED = ("Tone", "ESP Now")`, add:
```python
LIBRARY_PARTS = ("BombAssets",)  # generated parts of the library, from src/library/<name>.ubl.part
```
In `generate()`, replace:
```python
    library_template = (root / LIBRARY_TEMPLATE).read_text(encoding="utf-8")
```
with:
```python
    library_template = (root / LIBRARY_TEMPLATE).read_text(encoding="utf-8")
    parts = {name: (root / "src" / "library" / f"{name}.ubl.part").read_text(encoding="utf-8") for name in LIBRARY_PARTS}
```
and replace:
```python
        library = render(library_template, strings[lang])
```
with:
```python
        library = render(library_template, strings[lang], parts)
```

- [ ] **Step 4: Add the strings**

Add to the end of each JSON file (comma after the previous last entry).

`en.json`:
```json
  "blk.show_bomb": "show bomb _",
  "blk.jolt": "jolt",
  "blk.danger_bar": "show danger bar _",
  "menu.bomb_calm": "calm",
  "menu.bomb_nervous": "nervous",
  "menu.bomb_explode": "explode",
  "menu.bomb_safe": "safe",
  "comment.show_bomb": "Draws the bomb pictures (Noto Animated Emoji by Google, CC BY 4.0). The frames are files on the board, installed with the workshop firmware. Nervous shows the next frame each time it runs; explode and safe play their whole animation.",
  "comment.jolt": "How hard the board is moving right now: 0 when it is still, more when it is shaken. It is the distance between the acceleration and 100 (= 1 g).",
  "comment.danger_bar": "A bar along the bottom of the screen: green below 50, orange from 50, red at 100."
```

`fr.json`:
```json
  "blk.show_bomb": "afficher la bombe _",
  "blk.jolt": "secousse",
  "blk.danger_bar": "afficher la barre de danger _",
  "menu.bomb_calm": "calme",
  "menu.bomb_nervous": "nerveuse",
  "menu.bomb_explode": "explose",
  "menu.bomb_safe": "en sécurité",
  "comment.show_bomb": "Dessine la bombe (Noto Animated Emoji de Google, CC BY 4.0). Les images sont des fichiers sur la carte, installés avec le firmware de l'atelier. Nerveuse affiche l'image suivante à chaque fois ; explose et en sécurité jouent toute leur animation.",
  "comment.jolt": "La force avec laquelle la carte bouge en ce moment : 0 quand elle est immobile, plus quand on la secoue. C'est l'écart entre l'accélération et 100 (= 1 g).",
  "comment.danger_bar": "Une barre en bas de l'écran : verte sous 50, orange à partir de 50, rouge à 100."
```

`nl.json`:
```json
  "blk.show_bomb": "toon bom _",
  "blk.jolt": "schok",
  "blk.danger_bar": "toon gevarenbalk _",
  "menu.bomb_calm": "kalm",
  "menu.bomb_nervous": "nerveus",
  "menu.bomb_explode": "ontploft",
  "menu.bomb_safe": "veilig",
  "comment.show_bomb": "Tekent de bom (Noto Animated Emoji van Google, CC BY 4.0). De beelden zijn bestanden op het bord, geïnstalleerd met de workshopfirmware. Nerveus toont elke keer het volgende beeld; ontploft en veilig spelen hun hele animatie af.",
  "comment.jolt": "Hoe hard het bord nu beweegt: 0 als het stil ligt, meer als je schudt. Het is het verschil tussen de versnelling en 100 (= 1 g).",
  "comment.danger_bar": "Een balk onderaan het scherm: groen onder 50, oranje vanaf 50, rood bij 100."
```

- [ ] **Step 5: Add the blocks to the library template**

In `W/src/library/Core2Buttons.ubl.tmpl`:

Replace the line `variables _c2b_wasDown ` with:
```
variables _c2b_wasDown _c2b_nervousFrame _c2b_palette 
choices c2b_bombMenu '{{menu.bomb_calm}}' '{{menu.bomb_nervous}}' '{{menu.bomb_explode}}' '{{menu.bomb_safe}}'
```

After the spec line of `c2b_bigText`, add:
```
  space
  spec ' ' 'c2b_showBomb' '{{blk.show_bomb}}' 'menu.c2b_bombMenu' '{{menu.bomb_calm}}'
  spec 'r' 'c2b_jolt' '{{blk.jolt}}'
  spec ' ' 'c2b_dangerBar' '{{blk.danger_bar}}' 'num' 50
```
After the spec line of `_c2b_flashOff`, add:
```
  spec ' ' '_c2b_drawFrame' '_c2b_drawFrame _ _' 'str num' 'bomb_calm_1.data' 140
  spec ' ' '_c2b_playSet' '_c2b_playSet _' 'str' 'explode'
  spec 'r' '_c2b_bombPalette' '_c2b_bombPalette'
  spec 'r' '_c2b_bombSet' '_c2b_bombSet _' 'str' 'calm'
```
At the end of the file, add:
```

to c2b_showBomb state {
  comment '{{comment.show_bomb}}'
  if (state == '{{menu.bomb_calm}}') {
    '_c2b_drawFrame' 'bomb_calm_1.data' (at 2 ('_c2b_bombSet' 'calm'))
  } (state == '{{menu.bomb_nervous}}') {
    local 'set' ('_c2b_bombSet' 'nervous')
    _c2b_nervousFrame = ((_c2b_nervousFrame % (at 1 set)) + 1)
    '_c2b_drawFrame' ('[data:join]' 'bomb_nervous_' _c2b_nervousFrame '.data') (at 2 set)
  } (state == '{{menu.bomb_explode}}') {
    '[tft:clear]'
    '_c2b_playSet' 'explode'
  } (state == '{{menu.bomb_safe}}') {
    '[tft:clear]'
    '_c2b_playSet' 'safe'
  }
}

to '_c2b_playSet' name {
  local 'set' ('_c2b_bombSet' name)
  for i (at 1 set) {
    '_c2b_drawFrame' ('[data:join]' 'bomb_' name '_' i '.data') (at 2 set)
  }
}

to '_c2b_drawFrame' file size {
  if (_c2b_palette == 0) {
    _c2b_palette = ('_c2b_bombPalette')
  }
  local 'x' ((320 - size) / 2)
  local 'y' ((200 - size) / 2)
  '[file:open]' file
  repeat size {
    '[tft:pixelRow]' ('[file:readBytes]' size file) x y 1 _c2b_palette
    y += 1
  }
  '[file:close]' file
}

to c2b_jolt {
  comment '{{comment.jolt}}'
  return (absoluteValue (('[sensors:acceleration]') - 100))
}

to c2b_dangerBar value {
  comment '{{comment.danger_bar}}'
  local 'v' value
  if (v < 0) {
    v = 0
  }
  if (v > 100) {
    v = 100
  }
  local 'w' ((v * 320) / 100)
  local 'color' (colorSwatch 0 200 0 255)
  if (v >= 50) {
    color = (colorSwatch 255 160 0 255)
  }
  if (v >= 100) {
    color = (colorSwatch 255 0 0 255)
  }
  '[tft:rect]' 0 224 w 16 color (booleanConstant true)
  '[tft:rect]' w 224 (320 - w) 16 (colorSwatch 40 40 40 255) (booleanConstant true)
}

{{> BombAssets}}
```

- [ ] **Step 6: Generate and run all tests**

Run: `python3 tools/build.py && python3 -m pytest tools/tests -q && python3 tools/build.py --check`
Expected: library and project files rewritten; all tests pass; `--check` prints nothing.

- [ ] **Step 7: Update the changelog and commit**

Add under `### Added`: `- Bomb blocks in Core2Buttons: show bomb, jolt, show danger bar (EN, FR, NL).`

```bash
git add workshops/InternetOfThings/ESP32
git commit -m "ESP32 workshop: add bomb, jolt and danger bar blocks to Core2Buttons"
```

---

### Task 3: Mission 2 Bomb projects replace Hot Potato

**Files:**
- Create: `W/src/projects/bomb-start.ubp.tmpl`, `W/src/projects/bomb-done.ubp.tmpl`
- Delete: `W/src/projects/hot-potato-start.ubp.tmpl`, `hot-potato-done.ubp.tmpl`, and the folder `W/missions/02-hot-potato/`
- Modify: `W/tools/build.py` (`PROJECTS`), `W/i18n/*.json`, `W/tools/tests/test_generated.py`, `W/CHANGELOG.md`
- Generated: `W/missions/02-bomb/starter/bomb-start-{en,fr,nl}.ubp`, `W/missions/02-bomb/solution/bomb-done-{en,fr,nl}.ubp`

**Interfaces:**
- Consumes: `c2b_showBomb`, `c2b_jolt`, `c2b_dangerBar` (Task 2); `c2b_middleTouched`, `c2b_bigText`, `c2b_beep`, `c2b_vibrate`.
- Produces: solution globals `danger`, `playing`, `mood`; the tuning constants Task 5 adjusts are on these lines of `bomb-done.ubp.tmpl`: `if (j > 15) {` (jolt ignored below 15), `danger = (danger + (j / 5))` (increase per jolt), `(danger >= 100)` and `(danger >= 50)`.

- [ ] **Step 1: Write the failing tests**

In `W/tools/tests/test_generated.py`, delete the whole function `test_hot_potato_solution_has_both_games` and append:
```python
def test_bomb_solution_plays_the_danger_meter_game(files):
    en = strings("en")
    done = main_module(files["missions/02-bomb/solution/bomb-done-en.ubp"])
    assert "whenCondition playing" in done
    assert "local 'j' (c2b_jolt)" in done
    assert "(danger >= 100)" in done and "(danger >= 50)" in done
    for key in ("menu.bomb_calm", "menu.bomb_nervous", "menu.bomb_explode", "menu.bomb_safe"):
        assert "c2b_showBomb '" + build.escape(en[key]) + "'" in done, key
    assert "c2b_dangerBar danger" in done


def test_bomb_restart_resets_the_round(files):
    done = main_module(files["missions/02-bomb/solution/bomb-done-en.ubp"])
    restart = done[done.index("} else {", done.index("whenCondition (c2b_middleTouched)")):]
    for line in ("danger = 0", "resetTimer", "playing = (booleanConstant true)"):
        assert line in restart, line


def test_hot_potato_is_gone():
    assert not (build.ROOT / "missions/02-hot-potato").exists()
    assert all("hot-potato" not in template for template, _ in build.PROJECTS)
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m pytest tools/tests/test_generated.py -q -k "bomb or hot_potato"`
Expected: FAIL (`KeyError: 'missions/02-bomb/solution/bomb-done-en.ubp'`, and `test_hot_potato_is_gone` fails because the folder exists).

- [ ] **Step 3: Replace the Mission 2 strings**

In each JSON file, **delete** these keys: `project.m2_start`, `project.m2_done`, `comment.m2_start`, `screen.m2_ready`, `screen.m2_pass`, `screen.m2_lives`, `screen.m2_game_over`, `screen.m2_get_ready`, `screen.m2_go`, `screen.m2_early_left`, `screen.m2_early_right`, `screen.m2_left_wins`, `screen.m2_right_wins`. Keep `screen.m2_boom`. Then add:

`en.json`:
```json
  "project.m2_start": "Bomb - start here",
  "project.m2_done": "Bomb - finished version for coaches",
  "comment.m2_start": "Start here! Carry the bomb to the safe zone without jolting it. Follow mission.md step by step.",
  "screen.m2_touch": "Touch middle to start",
  "screen.m2_safe": "SAFE!"
```
`fr.json`:
```json
  "project.m2_start": "La bombe - commence ici",
  "project.m2_done": "La bombe - version finie pour les coachs",
  "comment.m2_start": "Commence ici ! Porte la bombe jusqu'à la zone de sécurité sans la secouer. Suis mission.md étape par étape.",
  "screen.m2_touch": "Touche le milieu",
  "screen.m2_safe": "BRAVO !"
```
`nl.json`:
```json
  "project.m2_start": "De bom - begin hier",
  "project.m2_done": "De bom - klaar, voor coaches",
  "comment.m2_start": "Begin hier! Breng de bom naar de veilige zone zonder te schokken. Volg mission.md stap voor stap.",
  "screen.m2_touch": "Tik midden om te starten",
  "screen.m2_safe": "VEILIG!"
```

- [ ] **Step 4: Write the templates**

`W/src/projects/bomb-start.ubp.tmpl`:
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

`W/src/projects/bomb-done.ubp.tmpl`:
```
module main
author Devoxx4Kids
version 1 0 
description '{{project.m2_done}}'
variables danger playing mood 

script 50 50 {
whenStarted
playing = (booleanConstant false)
'[tft:clear]'
c2b_showBomb '{{menu.bomb_calm}}'
'[tft:text]' '{{screen.m2_touch}}' 10 210 (colorSwatch 255 255 255 255) 2 (booleanConstant false)
}

script 50 300 {
whenCondition (c2b_middleTouched)
if playing {
  playing = (booleanConstant false)
  c2b_showBomb '{{menu.bomb_safe}}'
  c2b_bigText ('[data:join]' '{{screen.m2_safe}}' ' ' ((timer) / 1000) ' s') (colorSwatch 0 255 0 255)
  c2b_beep 1320 300
} else {
  danger = 0
  mood = 0
  resetTimer
  '[tft:clear]'
  c2b_showBomb '{{menu.bomb_calm}}'
  c2b_dangerBar 0
  playing = (booleanConstant true)
}
}

script 450 50 {
whenCondition playing
local 'j' (c2b_jolt)
if (j > 15) {
  danger = (danger + (j / 5))
} (danger > 0) {
  danger = (danger - 1)
}
if (danger >= 100) {
  playing = (booleanConstant false)
  c2b_showBomb '{{menu.bomb_explode}}'
  c2b_vibrate 800
  c2b_bigText '{{screen.m2_boom}}' (colorSwatch 255 0 0 255)
} (danger >= 50) {
  c2b_showBomb '{{menu.bomb_nervous}}'
  c2b_beep 880 40
  mood = 1
  c2b_dangerBar danger
} else {
  if (mood == 1) {
    c2b_showBomb '{{menu.bomb_calm}}'
    mood = 0
  }
  c2b_dangerBar danger
}
waitMillis 30
}


{{> Core2Buttons}}


{{> Tone}}
```

- [ ] **Step 5: Register the projects and remove Hot Potato**

In `W/tools/build.py`, replace the two `hot-potato` entries of `PROJECTS` with:
```python
    ("src/projects/bomb-start.ubp.tmpl", "missions/02-bomb/starter/bomb-start-{lang}.ubp"),
    ("src/projects/bomb-done.ubp.tmpl", "missions/02-bomb/solution/bomb-done-{lang}.ubp"),
```
Then, from the repository root:
```bash
git rm -r -q workshops/InternetOfThings/ESP32/missions/02-hot-potato workshops/InternetOfThings/ESP32/src/projects/hot-potato-start.ubp.tmpl workshops/InternetOfThings/ESP32/src/projects/hot-potato-done.ubp.tmpl
```

- [ ] **Step 6: Generate and run all tests**

Run (from `W/`): `python3 tools/build.py && python3 -m pytest tools/tests -q && python3 tools/build.py --check && python3 tools/check_docs.py`
Expected: six `wrote: missions/02-bomb/...` lines; all tests pass; no checker output.

- [ ] **Step 7: Update the changelog and commit**

Add under today's entry, `### Changed`: `- Mission 2 is now the Bomb (carry it to the safe zone without jolting it); Hot Potato removed, its duel becomes a bonus card.`

```bash
git add -A workshops/InternetOfThings/ESP32
git commit -m "ESP32 workshop: replace Hot Potato with the Bomb mission"
```

---

### Task 4: Firmware and image file system, reproducible

**Files:**
- Create: `W/firmware/build.sh`
- Generated (commit): `W/firmware/bomb-images.bin`; regenerated: `W/firmware/microblocks-core2-v1.3.bin`
- Modify: `W/firmware/README.md`, `W/CHANGELOG.md`

**Interfaces:**
- Consumes: `W/firmware/images/*.data` (Task 1), `W/firmware/microblocks-core2-v1.3.patch`.
- Produces: one install command for coaches, used by Task 7's setup text:
  `esptool --chip esp32 --port <PORT> --baud 460800 write-flash 0x0 microblocks-core2-v1.3.bin 0x210000 bomb-images.bin`
  (`0x210000` is the `spiffs` partition of MicroBlocks' `microblocks_partitions.csv`, size `0x1E0000`, file system LittleFS.)

- [ ] **Step 1: Write the build script**

`W/firmware/build.sh`:
```bash
#!/bin/bash
# Rebuild the Devoxx4Kids MicroBlocks firmware and the bomb image file system for the
# M5Stack Core2 v1.3. Needs git, Python 3 with platformio and esptool, and internet access.
# Usage: firmware/build.sh            (from the workshop folder)
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
BASE=b40b74d
WORK="${WORK:-$(mktemp -d)}"

git clone --quiet --branch dev https://codeberg.org/MicroBlocks/smallvm.git "$WORK/smallvm"
cd "$WORK/smallvm"
git checkout --quiet "$BASE"
git apply "$HERE/microblocks-core2-v1.3.patch"

rm -rf data
mkdir data
cp "$HERE"/images/*.data data/

pio run -e m5core2
pio run -e m5core2 -t buildfs

B=.pio/build/m5core2
BOOT_APP0="$(find "${PLATFORMIO_CORE_DIR:-$HOME/.platformio}/packages" -name boot_app0.bin | head -1)"
esptool --chip esp32 merge-bin --flash-size 16MB -o "$HERE/microblocks-core2-v1.3.bin" \
  0x1000 "$B/bootloader.bin" 0x8000 "$B/partitions.bin" 0xe000 "$BOOT_APP0" 0x10000 "$B/firmware.bin"
cp "$B/littlefs.bin" "$HERE/bomb-images.bin"

cd "$HERE"
shasum -a 256 microblocks-core2-v1.3.bin bomb-images.bin
```

- [ ] **Step 2: Run it**

```bash
chmod +x firmware/build.sh
python3 -m pip install platformio esptool
firmware/build.sh
```
Expected: both PlatformIO runs end with `[SUCCESS]`; the script prints two SHA-256 lines; `ls -la firmware/bomb-images.bin` shows about 1.9 MB (the full partition size).

- [ ] **Step 3: Check the frame count**

The script copies the frames into the file system folder; `build.sh` prints nothing about
them, so check the source folder: `ls firmware/images/*.data | wc -l` must print `21`.
Whether the board can read them is checked on hardware in Task 5 (check B1).

- [ ] **Step 4: Update the firmware README**

In `W/firmware/README.md`:
- Add a row to the files table:
  `| bomb-images.bin | LittleFS file system with the 21 bomb frames (Mission 2), to be written at address 0x210000 |`
- Replace the install command block with:
  ```bash
  esptool --chip esp32 --port <PORT> --baud 460800 write-flash 0x0 microblocks-core2-v1.3.bin 0x210000 bomb-images.bin
  ```
- Replace the "Rebuild from source" section body with: "Run `firmware/build.sh` from the workshop folder. It clones MicroBlocks `dev` at `b40b74d`, applies the patch, copies `firmware/images/*.data` into the file system, builds both images and prints their SHA-256."
- Replace the image SHA-256 line with the two values printed in Step 2.
- Add at the end: "Bomb and explosion animations: Noto Animated Emoji by Google, CC BY 4.0 (https://googlefonts.github.io/noto-emoji-animation/)."

- [ ] **Step 5: Commit**

Add under `### Added`: `- firmware/build.sh rebuilds the patched firmware and the bomb image file system (bomb-images.bin).`

```bash
git add workshops/InternetOfThings/ESP32/firmware workshops/InternetOfThings/ESP32/CHANGELOG.md
git commit -m "ESP32 workshop: reproducible firmware build with the bomb image file system"
```

---

### Task 5: Bomb spike on the Core2 v1.3 (HUMAN with agent)

Needs board #1 and a person carrying it. An agent can flash and edit, a person must carry and report.

**Files:**
- Modify (only to tune): `W/src/projects/bomb-done.ubp.tmpl` lines named in Task 3's Interfaces, then regenerate
- Modify: `W/library/README.md` (Bomb spike section; create the file with the template of Task 6 Step 1 first if it does not exist yet)

**Interfaces:**
- Consumes: Task 4 images, Task 3 projects.
- Produces: tuned constants and the values B1–B5 for Task 6's README.

- [ ] **Step 1: Flash board #1** (close MicroBlocks first)

```bash
esptool --chip esp32 --port /dev/cu.usbserial-<board1> --baud 460800 write-flash 0x0 firmware/microblocks-core2-v1.3.bin 0x210000 firmware/bomb-images.bin
```
Then unplug, 6 s off, 2 s on, plug in, connect in MicroBlocks (board name `M5StackCore2`).

- [ ] **Step 2: Checks**

| Check | How | Pass |
|---|---|---|
| B1 pictures | Open `missions/02-bomb/solution/bomb-done-en.ubp`, click `show bomb calm`, then `nervous` several times, then `explode`, then `safe` | Each picture is recognisable, colours correct, centred |
| B2 speed | Script: `reset timer`, `show bomb explode`, `say (timer)` | Note the ms; pass if under 2000 ms for the 8 frames |
| B3 careful walk | ▶, touch middle, carry the board 3 m carefully with two hands | The danger bar stays below 50 most of the way |
| B4 clumsy walk | Same, walking quickly and bumping the board lightly | Reaches 100 and explodes |
| B5 no images | Flash only `0x0 microblocks-core2-v1.3.bin` with `erase-flash` first on board #2, open the solution, play | No pictures, but no error popup; bar, beep, texts, buzz work |

- [ ] **Step 3: Tune**

- If B3 fails (too sensitive): raise `if (j > 15)` in steps of 5, or change `(j / 5)` to `(j / 8)`.
- If B4 fails (never explodes): lower `(j / 5)` to `(j / 3)`.
- If B2 is over 2000 ms: in `tools/convert_images.py` reduce the `explode` frames to `[0, 6, 12, 18, 26, 32]` and `safe` to `[25, 30, 35, 40]`, run `python3 tools/convert_images.py`, `firmware/build.sh`, and re-flash.
After any change: `python3 tools/build.py && python3 -m pytest tools/tests -q` (all pass), re-run the failing check.

- [ ] **Step 4: Record and commit**

Add to `W/library/README.md`, under `## Tested on hardware`:
```markdown
### Bomb spike

| Check | Result | Notes |
|---|---|---|
| B1 pictures | | |
| B2 explode animation time | | ms: |
| B3 careful walk | | max danger: |
| B4 clumsy walk | | |
| B5 without bomb-images.bin | | |

Final constants in `src/projects/bomb-done.ubp.tmpl`: jolt ignored below __, increase `j / __`, nervous at 50, explode at 100.
```
Fill every cell (replace the `__` too).

```bash
git add workshops/InternetOfThings/ESP32
git commit -m "ESP32 workshop: tune the Bomb on hardware and record the spike results"
```

---

### Task 6: Close the hardware test (HUMAN with agent)

**Files:**
- Create or modify: `W/library/README.md`
- Modify: `W/CHANGELOG.md`

**Interfaces:**
- Consumes: the ledger entries of 2026-11-13 in `.superpowers/sdd/2026-11-11-esp32-magic-ball-workshop/progress.md` (results H1–H7 and the firmware patch).
- Produces: the hardware record that the first plan's Tasks 8–11 rely on.

- [ ] **Step 1: Write `W/library/README.md`** (if Task 5 already created it, keep its Bomb spike section)

```markdown
# Core2Buttons library

Helper blocks for the M5Stack Core2, used by every mission.

## Tested on hardware

Board: Core2 v1.3 (K010-V13), two boards. Firmware: MicroBlocks `dev` b40b74d with the
Devoxx4Kids patch (`../firmware/`). IDE: MicroBlocks pilot (2.5.15) and the 3.0 preview.
Date: 2026-11-13.

| Check | What was tested | Result | Notes |
|---|---|---|---|
| H1 | Install, connection, screen | pass | Stable VM 411 fails on the v1.3 (no reply); pilot VM 424 and the patched build work. The firmware menu has no Core2 entry: advanced mode → install ESP firmware from microblocks.fun → m5core2_1.0, or esptool with `../firmware/`. On macOS, power-cycle without USB after flashing. Green LED is off by design (MicroBlocks turns it off) |
| H2 | Circles react, other circles ignored | pass | screen tap: |
| H3 | One event per touch (hold 3 s) | | |
| H4 | Beep | pass | Tone library works on the pilot firmware |
| H5 | Shake and vibration | pass (patched) | Stock firmware: acceleration 0 (BMI270 not read), no motor. Patched: acceleration 99 at rest; motor on/off via `[tft:setVibration]` |
| H6 | ESP Now between two boards | pass | both directions, emoji, name, beep; party with buzz (250 ms; 100 ms was not felt) |
| H7 | Hot Potato | pass | replaced by the Bomb (see below) |
| H8 | Long text and accents | | accents render: |
| H9 | FR and NL labels | | |

**Decision (plan Task 7, Step 8):** MicroBlocks + firmware patch.
```

- [ ] **Step 2: Run the open checks with the person**

- **H3:** hold the middle circle 3 s in the Magic Ball → exactly one answer.
- **H2 screen tap:** tap the screen itself → no answer.
- **H8:** change one answer to `Peut-être !` and one to a 40-character sentence → note whether `ê` renders and whether the sentence fits.
- **H9:** globe → Français, open `missions/01-magic-shake-ball/solution/magic-ball-done-fr.ubp` → Core2Buttons labels in French; same for Nederlands with `-nl.ubp`.

Fill the remaining cells. If H8 shows that accents do not render, add to `W/i18n/*.json` nothing (the `screen.*` texts are ASCII already) and write in the notes: "children's own answers: avoid accents on the Core2".

- [ ] **Step 3: Commit**

Add under today's entry, `### Changed`: `- Hardware test on two Core2 v1.3 boards recorded in library/README.md.`

```bash
git add workshops/InternetOfThings/ESP32
git commit -m "ESP32 workshop: record the Core2 v1.3 hardware test results"
```

---

### Task 7: Amend the first plan's remaining tasks

**Files:**
- Modify: `docs/superpowers/plans/2026-11-11-esp32-magic-ball-workshop.md`

**Interfaces:**
- Consumes: the install command of Task 4, the Bomb projects of Task 3, the results of Tasks 5–6.
- Produces: Tasks 8–14 of the first plan, ready to execute.

- [ ] **Step 1: Mark the finished tasks**

At the top of the first plan, under the header, add:
```markdown
> **Status 2026-11-13:** Tasks 1–6 done. Task 7 (hardware test) is closed by Tasks 5–6 of `2026-11-13-esp32-workshop-bomb-and-firmware.md`. Mission 2 is now the Bomb: Task 5 below (Hot Potato) is superseded, and Task 10 is replaced by the version in this file's Task 10 note. The firmware for coaches is `firmware/microblocks-core2-v1.3.bin` + `firmware/bomb-images.bin`.
```

- [ ] **Step 2: Replace the firmware section of Task 8's `coach/en/setup.md`**

In Task 8 Step 3, replace the whole section `## 2. Install MicroBlocks on each Core2 (once)` (from its heading to the line before `## 3. Language`) with:
```markdown
## 2. Install the workshop firmware on each Core2 (once)

The standard MicroBlocks firmware does not support the Core2 v1.3 fully. Use the workshop
firmware from `firmware/` (MicroBlocks with a small patch for the v1.3 motion sensor and
vibration motor, plus the bomb pictures for Mission 2).

1. Install Python 3 and esptool once: `pip install esptool`.
2. Close MicroBlocks, connect the Core2 with a data cable, and run from the workshop folder
   (replace `<PORT>`; on macOS it looks like `/dev/cu.usbserial-…`):

       esptool --chip esp32 --port <PORT> --baud 460800 write-flash 0x0 firmware/microblocks-core2-v1.3.bin 0x210000 firmware/bomb-images.bin

3. Unplug the cable, switch the board off (hold the left button 6 seconds) and on again
   (2 seconds), and plug the cable back in.
4. Open MicroBlocks (https://microblocks.fun → **Run**), connect, and check that the board
   name is **M5StackCore2**.
5. Open `missions/01-magic-shake-ball/solution/magic-ball-done-en.ubp`, click ▶ and shake
   the board: an answer appears, with a beep and a buzz. The board is ready.

The screen stays black and the green LED stays off until a program draws something: that
is normal.
```

- [ ] **Step 3: Add to Task 8's `coach/en/hardware.md` and `README.md` text**

In Task 8 Step 3, at the end of the `coach/en/hardware.md` block, add:
```markdown

## Credits

Bomb and explosion animations: Noto Animated Emoji by Google, CC BY 4.0
(https://googlefonts.github.io/noto-emoji-animation/).
```
In Task 8 Step 1 (`W/README.md`), change the Mission 2 table row to:
`| 2. The Bomb | Carry the bomb to the safe zone without jolting it, or BOOM | [EN](missions/02-bomb/en/mission.md) | [FR](missions/02-bomb/fr/mission.md) | [NL](missions/02-bomb/nl/mission.md) |`
and add the Credits section above as the last section of `W/README.md`.

In Task 8 Step 3 (`coach/en/running-a-session.md`), add under "Before the children arrive":
`- For Mission 2, mark a start point and a safe zone (a sheet of paper) about 3 metres apart on each table. Children carry the board with two hands, walking.`

- [ ] **Step 4: Replace Task 10 with the Bomb pages**

Replace the whole of Task 10 (heading to the line before `### Task 11`) with:

````markdown
### Task 10: English kids' pages for Mission 2 (The Bomb)

**Files:**
- Create: `W/missions/02-bomb/en/mission.md`, `W/missions/02-bomb/en/bonus-cards.md`
- Modify: `W/CHANGELOG.md`

**Interfaces:**
- Consumes: block labels from `library/README.md`; starter `../starter/bomb-start-en.ubp`; `menu.bomb_*`, `blk.show_bomb`, `blk.jolt`, `blk.danger_bar`, `screen.m2_*` from `en.json`; tuned constants from `library/README.md` (Bomb spike).

- [ ] **Step 1: Write `mission.md`**

```markdown
# Mission 2: The Bomb 💣

You are the bomb squad! Carry the bomb to the safe zone without jolting it... or BOOM!

**You need:** a Core2 board, a laptop with MicroBlocks, the project
[bomb-start-en.ubp](../starter/bomb-start-en.ubp), and a safe zone on the table (your
coach marks it).

**Roles:** the **driver** uses the mouse, the **navigator** reads this page aloud. Swap at
every 🔄. **Always carry the board with two hands, and walk.**

## ⭐1 The bomb appears

1. Under **when started**, add **show bomb calm** (from **Core2Buttons**).
2. Make a **when** script with **middle button touched?** and add **reset timer** and
   **show big text** `Go!`.

**🧪 Try it!** Click ▶. Do you see the bomb? Touch the middle circle.

**🔄 Swap**

## ⭐2 How hard are you moving?

1. Make a **when** script with **middle button touched?** → **forever** →
   **show big text (jolt)** in white.
2. Click ▶, touch the middle circle, and move the board slowly, then faster.

**🧪 Try it!** What number do you get when you hold it still? When you walk? When you bump
it?

**🔄 Swap**

## ⭐3 The danger meter

1. Add a variable `danger`. Set it to 0 when the middle circle is touched.
2. In the **forever** loop (remove the jolt text): if **jolt > 15**, change danger by
   **jolt / 5**; otherwise, if danger > 0, change danger by -1.
3. **If danger ≥ 100:** **show bomb explode**, **vibrate for 800 ms**, **show big text**
   `BOOM!` in red, and stop. **Else if danger ≥ 50:** **show bomb nervous** and
   **beep 880 Hz for 40 ms**. **Else:** **show bomb calm**.
4. At the end of the loop: **show danger bar (danger)**.

**🧪 Try it!** Walk to the safe zone. Does the bomb get nervous when you bump it?

**🔄 Swap**

## ⭐4 Safe!

1. When the middle circle is touched **during** the game, the bomb is in the safe zone:
   **show bomb safe**, then **show big text (join `SAFE!` (timer / 1000) ` s`)** in green.
2. Use a variable `playing` (true during the game) so the middle circle knows whether to
   start or to finish.

**🧪 Try it!** How fast can you bring the bomb to safety without exploding it?

**🔄 Swap**

## You did it! 🎉

You built a game with a **sensor** (movement), a **variable that changes over time** (the
danger meter), **limits** (50 and 100), images and a **timer**. Try a
[bonus card](bonus-cards.md)!

*Bomb and explosion animations: Noto Animated Emoji by Google, CC BY 4.0.*
```

- [ ] **Step 2: Write `bonus-cards.md`**

```markdown
# Mission 2: bonus cards 🃏

---

## 🃏 Card A: Bomb squad training (reaction duel)

**Goal:** who reacts fastest? The board stays on the table.

**How:** a **when** script with **right button touched?**: show `Get ready...`, wait a
**random** 2000 to 5000 ms, show `GO!` and beep. Then **repeat until** someone touches:
left circle → `Left wins!`, right circle → `Right wins!`. Touching before GO! → `Too early!`.

---

## 🃏 Card B: Expert mode

**Goal:** a more sensitive bomb.

**How:** change the limits: nervous at **30**, explode at **60**.

---

## 🃏 Card C: Record

**Goal:** remember the fastest safe time.

**How:** a variable `best`, set to 99999 in **when started**. When the bomb is safe, if
the time is smaller than `best`, set `best` to it and show `NEW RECORD!`.

---

## 🃏 Card D: The long route

**Goal:** a route around the room; pairs take turns.

**How:** no new blocks: agree with your coach on a longer route. Who keeps the danger bar
the lowest?

**Coach hint:** keep the route clear of chairs and bags; always walk.
```

- [ ] **Step 3: Check and commit**

Run: `python3 tools/check_docs.py | grep -v -e "folder missing" -e "/fr/" -e "/nl/" -e "03-emoji-messenger"`
Expected: no output.

Add under `### Added`: `- Mission 2 (The Bomb) kids' page and bonus cards (English).`

```bash
git add workshops/InternetOfThings/ESP32
git commit -m "ESP32 workshop: add Mission 2 Bomb English pages"
```
````

- [ ] **Step 5: Fix references to Hot Potato in Tasks 8, 12, 13 and 14**

In the first plan, replace every remaining `02-hot-potato` with `02-bomb`, and in Task 9 and Task 11 check commands replace `-e "02-hot-potato"` with `-e "02-bomb"`. In Task 14 Step 2, change "BOOM!" in the photo list to "the bomb (calm or exploding)". Then run:
```bash
grep -n -i "hot.potato" docs/superpowers/plans/2026-11-11-esp32-magic-ball-workshop.md
```
Expected: only lines inside the new status note and Task 5's original text (kept as history).

- [ ] **Step 6: Commit**

```bash
git add docs/superpowers/plans/2026-11-11-esp32-magic-ball-workshop.md
git commit -m "Plan: amend remaining tasks for the Bomb mission and the workshop firmware"
```
