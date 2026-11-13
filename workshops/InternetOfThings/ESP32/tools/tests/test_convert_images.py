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
