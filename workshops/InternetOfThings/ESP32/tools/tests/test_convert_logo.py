from pathlib import Path

import pytest

PIL = pytest.importorskip("PIL")
from PIL import Image  # noqa: E402

import convert_logo  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]


def rgb565(r, g, b):
    return ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)


def decode(runs, width):
    rows, row = [], []
    for count, color in runs:
        row += [color] * count
        assert len(row) <= width, "a run crosses the end of a row"
        if len(row) == width:
            rows.append(row)
            row = []
    assert row == []
    return rows


def test_runs_rebuild_the_image_on_white():
    image = Image.new("RGBA", (4, 2), (0, 0, 0, 0))
    image.putpixel((1, 0), (255, 0, 0, 255))
    image.putpixel((2, 0), (255, 0, 0, 255))
    image.putpixel((3, 1), (0, 0, 255, 255))
    white, red, blue = rgb565(255, 255, 255), rgb565(255, 0, 0), rgb565(0, 0, 255)
    runs = convert_logo.runs(image)
    assert runs == [(1, white), (2, red), (1, white), (3, white), (1, blue)]
    assert decode(runs, 4) == [[white, red, red, white], [white, white, white, blue]]


def test_header_centres_the_logo_on_the_screen():
    text = convert_logo.header_text(Image.new("RGBA", (231, 231), (0, 0, 0, 0)))
    for line in ("#define D4K_LOGO_W 231", "#define D4K_LOGO_H 231", "#define D4K_LOGO_X 44", "#define D4K_LOGO_Y 4"):
        assert line in text
    assert "static const uint16_t d4kLogoRuns[] = {" in text


def test_logo_must_fit_the_screen():
    with pytest.raises(ValueError, match="320 x 240"):
        convert_logo.header_text(Image.new("RGBA", (241, 241)))


def test_committed_header_matches_the_logo():
    expected = convert_logo.header_text(Image.open(ROOT / "src/images/devoxx4kids-logo.png"))
    assert (ROOT / "firmware/d4kLogo.h").read_text(encoding="utf-8") == expected
