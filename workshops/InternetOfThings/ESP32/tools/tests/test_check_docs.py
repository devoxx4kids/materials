from pathlib import Path

import check_docs


def write(path: Path, text: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_parity_reports_missing_and_extra_files(tmp_path):
    for name in ("setup.md", "hardware.md"):
        write(tmp_path / "coach/en" / name)
        write(tmp_path / "coach/nl" / name)
    write(tmp_path / "coach/fr/setup.md")
    write(tmp_path / "coach/fr/extra.md")
    assert check_docs.check_language_parity(tmp_path) == [
        "coach/fr: missing hardware.md",
        "coach/fr: extra extra.md",
    ]


def test_parity_reports_missing_language_folder(tmp_path):
    write(tmp_path / "missions/01-x/en/mission.md")
    write(tmp_path / "missions/01-x/fr/mission.md")
    assert check_docs.check_language_parity(tmp_path) == ["missions/01-x/nl: folder missing"]


def test_links_only_reports_broken_local_targets(tmp_path):
    write(
        tmp_path / "README.md",
        "[ok](coach/en/setup.md) [bad](coach/en/nope.md) [web](https://example.org) "
        "[top](#top) ![img](images/a%20b.png) [anchor](coach/en/setup.md#step-1) [mail](mailto:x@y.z)",
    )
    write(tmp_path / "coach/en/setup.md")
    write(tmp_path / "images/a b.png")
    assert check_docs.check_links(tmp_path) == ["README.md: broken link coach/en/nope.md"]


def test_links_are_relative_to_the_file(tmp_path):
    write(tmp_path / "missions/01-x/en/mission.md", "[start](../starter/a-en.ubp)")
    assert check_docs.check_links(tmp_path) == ["missions/01-x/en/mission.md: broken link ../starter/a-en.ubp"]
    write(tmp_path / "missions/01-x/starter/a-en.ubp")
    assert check_docs.check_links(tmp_path) == []


def test_asciidoc_is_rejected(tmp_path):
    write(tmp_path / "README.adoc")
    write(tmp_path / "coach/en/old.asciidoc")
    assert check_docs.check_no_asciidoc(tmp_path) == [
        "README.adoc: AsciiDoc is not allowed, use Markdown",
        "coach/en/old.asciidoc: AsciiDoc is not allowed, use Markdown",
    ]


def test_mission_pages_must_exist(tmp_path):
    write(tmp_path / "missions/01-x/en/mission.md")
    assert check_docs.check_mission_pages(tmp_path) == ["missions/01-x/en: missing bonus-cards.md"]


def test_main_returns_zero_for_a_clean_tree(tmp_path):
    write(tmp_path / "README.md", "# Hi")
    assert check_docs.main([str(tmp_path)]) == 0


def test_main_returns_one_and_prints_problems(tmp_path, capsys):
    write(tmp_path / "README.adoc")
    assert check_docs.main([str(tmp_path)]) == 1
    assert "README.adoc: AsciiDoc is not allowed" in capsys.readouterr().out
