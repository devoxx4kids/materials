"""Checks on the real generated files of the workshop (not on fixtures)."""
import json
import re

import pytest

import build

FUNCTION = re.compile(r"^to '?(_?c2b_\w+)'?", re.MULTILINE)
CALL = re.compile(r"\b(_?c2b_\w+)\b")
# Library variables and menus: names that look like helpers but are not functions.
LIBRARY_NAMES = {"_c2b_wasDown", "_c2b_nervousFrame", "_c2b_palette", "_c2b_openFile", "c2b_bombMenu"}
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


def test_big_text_wraps_long_text_instead_of_shrinking_it(files):
    """A 39-character answer at size 1 (6 x 8 pixel letters) was too small to read on the
    Core2 (hardware test H8, 2026-11-16): long texts are split over lines, as big as fits."""
    text = library(files)
    big = body(text, "c2b_bigText")
    assert "for scale ('[data:makeList]' 4 3 2 1) {" in big
    assert "('_c2b_wrap' text (320 / (6 * scale)))" in big
    wrap = body(text, "_c2b_wrap")
    assert "for word ('[data:split]' text ' ') {" in wrap
    assert "'[data:addLast]' line lines" in wrap

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
    assert "to '_c2b_bombSet' name {" in text
    assert "to '_c2b_loadPalette' {" in text


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


def test_no_text_literal_is_too_big_to_send(files):
    """MicroBlocks refuses to send a compiled function over 1000 bytes to the board and
    replaces it with a 'Script too large' error, so keep every text literal well below."""
    for name, text in files.items():
        for literal in re.findall(r"'((?:[^']|'')*)'", main_module(text) if name.endswith(".ubp") else text):
            if literal.startswith(("Generated by", "Support for ESP Now", "This library supports")):
                continue  # comments and descriptions are not compiled into the board's code
            assert len(literal) <= 700, f"{name}: literal of {len(literal)} characters"


def test_committed_frames_match_the_frame_table():
    part = (build.ROOT / "src/library/BombAssets.ubl.part").read_text(encoding="utf-8")
    table = dict((m[0], (int(m[1]), int(m[2]))) for m in re.findall(
        r"if \(name == '(\w+)'\) \{\n    return \('\[data:makeList\]' (\d+) (\d+)\)", part))
    expected = {f"bomb_{s}_{n}.data": size for s, (count, size) in table.items() for n in range(1, count + 1)}
    images = build.ROOT / "firmware/images"
    frames = {p.name: p.stat().st_size for p in images.glob("bomb_*_*.data")}
    assert set(frames) == set(expected)
    for name, size in expected.items():
        assert frames[name] == size * size, name
    assert (images / "bomb_palette.data").stat().st_size == 256 * 3


def test_palette_comes_from_a_file_and_survives_a_missing_file(files):
    load = body(library(files), "_c2b_loadPalette")
    assert "('[file:readBytes]' 768 'bomb_palette.data')" in load
    assert "if ((size rgb) < 768) {" in load  # no images on the board: no error, just black


def test_a_frame_file_left_open_by_a_stopped_program_is_closed_first(files):
    """The VM has only 4 file slots and does not close files when a program is stopped."""
    draw = body(library(files), "_c2b_drawFrame")
    close_old = "if (_c2b_openFile != 0) {\n    '[file:close]' _c2b_openFile\n  }"
    assert close_old in draw
    assert draw.index(close_old) < draw.index("'[file:open]' file")
    assert "_c2b_openFile = file" in draw and "_c2b_openFile = 0" in draw



def test_touching_during_boom_or_safe_is_ignored(files):
    """Children tap while the explosion plays; that tap must not start a broken round."""
    en = strings("en")
    done = main_module(files["missions/02-bomb/solution/bomb-done-en.ubp"])
    middle = done[done.index("whenCondition (c2b_middleTouched)"):]
    middle = middle[:middle.index("\n}\n")]
    assert middle.splitlines()[1] == "if (not busy) {"
    for state in ("menu.bomb_explode", "menu.bomb_safe"):
        show = "c2b_showBomb '" + build.escape(en[state]) + "'"
        before = done[:done.index(show)]
        assert before.rstrip().endswith("busy = (booleanConstant true)") or "busy = (booleanConstant true)\n" in before[-200:], state
    assert done.count("busy = (booleanConstant false)") >= 3  # start, after BOOM, after SAFE


def test_the_explosion_can_be_heard(files):
    """Each explosion frame comes with a short low rumble, after a deep opening boom."""
    show = body(library(files), "c2b_showBomb")
    play = body(library(files), "_c2b_playSet")
    explode = show[show.index("menu") if False else show.index("'_c2b_playSet' 'explode'") - 200:show.index("'_c2b_playSet' 'explode'")]
    assert "'play frequency' 50 200" in explode
    assert "if (name == 'explode') {\n      'play frequency' (random 30 90) 50\n    }" in play
