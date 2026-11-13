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


def test_magic_ball_solution_answers_touch_and_shake(files):
    en = json.loads((build.ROOT / "i18n/en.json").read_text(encoding="utf-8"))
    done = files["missions/01-magic-shake-ball/solution/magic-ball-done-en.ubp"]
    assert "whenCondition (or (c2b_middleTouched) (c2b_shaken))" in done
    for key in ("screen.m1_yes", "screen.m1_no", "screen.m1_maybe", "screen.m1_again", "screen.m1_ask"):
        assert "'" + build.escape(en[key]) + "'" in done, key
    start = files["missions/01-magic-shake-ball/starter/magic-ball-start-en.ubp"]
    assert "whenStarted" in start
    assert "c2b_middleTouched" not in main_module(start)


def test_hot_potato_solution_has_both_games(files):
    done = files["missions/02-hot-potato/solution/hot-potato-done-en.ubp"]
    assert "whenCondition (c2b_middleTouched)" in done
    assert "whenCondition (c2b_rightTouched)" in done
    assert "(random 5000 15000)" in done
    assert "lives = (lives - 1)" in done
    start = files["missions/02-hot-potato/starter/hot-potato-start-en.ubp"]
    assert "whenStarted" in start


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


def test_beep_and_vibrate_also_flash_the_screen(files):
    """The Core2 speaker and motor may stay silent in MicroBlocks, so every beep and
    buzz is also shown as a frame around the screen."""
    text = library(files)
    for helper in ("_c2b_flashOn", "_c2b_flashOff"):
        assert "'[tft:rect]'" in body(text, helper), helper
    for name in ("c2b_beep", "c2b_vibrate"):
        assert "'_c2b_flashOn'" in body(text, name), name
        assert "'_c2b_flashOff'" in body(text, name), name


def test_vibrate_uses_the_firmware_vibration_primitive(files):
    """The Core2 motor is switched by the setVibration primitive of our patched MicroBlocks
    firmware (AXP192 LDO3 on the internal bus). The old I2C route reached the Grove port
    instead and stopped the child's script with an error."""
    vibrate = body(library(files), "c2b_vibrate")
    on = "'[tft:setVibration]' (booleanConstant true)"
    off = "'[tft:setVibration]' (booleanConstant false)"
    assert on in vibrate and off in vibrate
    assert vibrate.index(on) < vibrate.index("waitMillis ms") < vibrate.index(off)
    assert "i2cSet" not in vibrate and "i2cGet" not in vibrate
