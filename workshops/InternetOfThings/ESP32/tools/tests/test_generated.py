"""Checks on the real generated files of the workshop (not on fixtures)."""
import json
import re

import pytest

import build

FUNCTION = re.compile(r"^to '?(_?c2b_\w+)'?", re.MULTILINE)
CALL = re.compile(r"\b(_?c2b_\w+)\b")
# Library variables and menus: names that look like helpers but are not functions.
LIBRARY_NAMES = {"_c2b_wasDown", "_c2b_nervousFrame", "_c2b_palette", "c2b_bombMenu"}
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
            assert set(CALL.findall(text)) <= defined | LIBRARY_NAMES, name


def test_magic_ball_solution_answers_touch_and_shake(files):
    en = json.loads((build.ROOT / "i18n/en.json").read_text(encoding="utf-8"))
    done = files["missions/01-magic-shake-ball/solution/magic-ball-done-en.ubp"]
    assert "whenCondition (or (c2b_middleTouched) (c2b_shaken))" in done
    for key in ("screen.m1_yes", "screen.m1_no", "screen.m1_maybe", "screen.m1_again", "screen.m1_ask"):
        assert "'" + build.escape(en[key]) + "'" in done, key
    start = files["missions/01-magic-shake-ball/starter/magic-ball-start-en.ubp"]
    assert "whenStarted" in start
    assert "c2b_middleTouched" not in main_module(start)


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


def test_every_buzz_is_long_enough_to_feel(files):
    """On the Core2 the motor needs about 200 ms to be felt (100 ms buzzes went unnoticed
    in the hardware test of 2026-11-13)."""
    for name, text in files.items():
        if name.endswith(".ubp"):
            for ms in re.findall(r"c2b_vibrate (\d+)", main_module(text)):
                assert int(ms) >= 200, f"{name}: vibrate {ms} ms"


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
