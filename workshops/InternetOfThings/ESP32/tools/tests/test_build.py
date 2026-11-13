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
    write(root / "src/library/BombAssets.ubl.part", "")
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


def test_library_parts_are_included_into_the_library(tmp_path):
    projects = make_workshop(tmp_path)
    write(tmp_path / "src/library/Core2Buttons.ubl.tmpl", "module Core2Buttons Input\n{{> BombAssets}}\n")
    write(tmp_path / "src/library/BombAssets.ubl.part", "to '_c2b_bombSet' name {\n}\n")
    build.build(tmp_path, projects)
    assert "to '_c2b_bombSet' name {" in (tmp_path / "library/Core2Buttons-en.ubl").read_text(encoding="utf-8")
