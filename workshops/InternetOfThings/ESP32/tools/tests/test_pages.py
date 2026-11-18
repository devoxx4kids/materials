"""Content checks on the kids' and coach pages that a session depends on."""
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def page(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


@pytest.mark.parametrize("lang, palette", [("en", "**Operators**"), ("fr", "**Opérateurs**"), ("nl", "**Functies**")])
def test_bomb_page_says_where_the_true_false_switch_is(lang, palette):
    """Typing true into the set block stores the text "true", and when (playing) never fires."""
    first_step = page(f"missions/02-bomb/{lang}/mission.md").split("## ⭐2")[0]
    assert palette in first_step


@pytest.mark.parametrize("lang, cancel", [("en", "**Cancel**"), ("fr", "**Annuler**"), ("nl", "**Annuleren**")])
def test_setup_warns_against_the_firmware_update_prompt(lang, cancel):
    """Accepting MicroBlocks' update offer replaces the workshop firmware with the stock one."""
    setup = page(f"coach/{lang}/setup.md")
    assert cancel in setup and "3.0" in setup


@pytest.mark.parametrize("lang", ["en", "fr", "nl"])
def test_troubleshooting_covers_overwritten_firmware_and_text_true(lang):
    table = page(f"coach/{lang}/running-a-session.md")
    assert table.count("setup.md") >= 3  # bomb pictures, overwritten firmware, plus the known limit
    assert "`true`" in table or "`vrai`" in table or "`waar`" in table


def test_firmware_shows_the_logo_after_the_start_up_clear():
    patch = page("firmware/microblocks-core2-v1.3.patch")
    assert "+void tftShowLogo();" in patch  # declared in interp.h
    io = patch[patch.index("diff --git a/vm/ioPrims.cpp"):]
    io = io[:io.index("diff --git", 1)] if "diff --git" in io[1:] else io
    assert " \t\ttftClear();\n+\t#if defined(ARDUINO_M5STACK_Core2)\n+\t\ttftShowLogo();" in io
    assert '#include "d4kLogo.h"' in patch


def test_build_script_copies_the_logo_header():
    assert 'cp "$HERE/d4kLogo.h" vm/' in page("firmware/build.sh")


@pytest.mark.parametrize("path", ["README.md", "firmware/README.md", "coach/en/setup.md", "coach/fr/setup.md", "coach/nl/setup.md"])
def test_docs_say_the_logo_shows_the_workshop_firmware(path):
    """A black screen at power-on now means the workshop firmware is missing, not that all is well."""
    text = page(path)
    assert "Devoxx4Kids" in text and ("logo" in text.lower())
    assert "until a program draws something: that is normal" not in text
    assert "tant qu'aucun programme ne dessine quelque chose : c'est normal" not in text
    assert "zolang geen programma iets tekent: dat is normaal" not in text



def test_core2_does_not_spell_the_bluetooth_name_over_the_logo():
    """MicroBlocks spells the Bluetooth name on the screen and then clears it; the workshop uses USB."""
    patch = page("firmware/microblocks-core2-v1.3.patch")
    ide = patch[patch.index("diff --git a/vm/ideComm.cpp"):]
    assert "+\t#if !defined(NEZHA_ESP32) && !defined(ARDUINO_M5STACK_Core2)\n \t\tshow_BLE_ID();" in ide


def test_logo_stays_three_seconds_before_the_program_starts():
    patch = page("firmware/microblocks-core2-v1.3.patch")
    boot = patch[patch.index("diff --git a/vm/vm.ino"):]
    assert "+\t#if defined(ARDUINO_M5STACK_Core2)\n+\t\tdelay(3000);" in boot
    assert boot.index("delay(3000)") < boot.index("startAll();")
    assert "tftShowLogo" not in boot
