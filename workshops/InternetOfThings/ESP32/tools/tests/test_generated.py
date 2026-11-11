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
