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
