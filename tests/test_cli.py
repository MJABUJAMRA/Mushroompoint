from pathlib import Path

import mushroompoint
from mushroompoint.cli import (
    DATA_PATH,
    Mushroom,
    filter_mushrooms,
    format_mushroom,
    format_summary,
    load_mushrooms,
    main,
    summarize_mushrooms,
)


def test_data_file_exists():
    assert DATA_PATH.exists()
    assert DATA_PATH.is_file()


def test_load_mushrooms_parses_data(tmp_path: Path):
    fake_data = tmp_path / "mushrooms.json"
    fake_data.write_text(
        """
        [
          {"name": "Test", "edible": true, "habitat": ["forest"], "season": ["autumn"], "notes": "Sample"}
        ]
        """,
        encoding="utf-8",
    )

    mushrooms = load_mushrooms(fake_data)
    assert len(mushrooms) == 1
    assert mushrooms[0] == Mushroom(
        name="Test",
        edible=True,
        habitat=["forest"],
        season=["autumn"],
        notes="Sample",
    )


def test_filtering_by_habitat_and_edibility():
    mushrooms = load_mushrooms()
    forest_edible = filter_mushrooms(mushrooms, habitat="forest", edible=True)

    assert all("forest" in [h.lower() for h in mushroom.habitat] for mushroom in forest_edible)
    assert all(mushroom.edible for mushroom in forest_edible)


def test_matches_is_case_insensitive():
    morels = filter_mushrooms(load_mushrooms(), habitat="FOREST", season="SPRING")
    assert any(mushroom.name == "Morel" for mushroom in morels)


def test_summarize_mushrooms_counts_and_sorts():
    mushrooms = load_mushrooms()
    summary = summarize_mushrooms(mushrooms)

    assert "forest" in [h.lower() for h in summary["habitat"]]
    assert summary["season"] == sorted(summary["season"])
    assert summary["edible"]["edible"] + summary["edible"].get("toxic", 0) == len(mushrooms)


def test_cli_listar_prints_summary(capsys):
    exit_code = main(["--listar"])
    captured = capsys.readouterr().out

    assert exit_code == 0
    assert "Opções disponíveis" in captured
    assert "Habitat" in captured
    assert "Estações" in captured


def test_cli_no_results_message_is_in_portuguese(capsys):
    exit_code = main(["--habitat", "desert"])
    captured = capsys.readouterr().out

    assert exit_code == 1
    assert "Nenhum cogumelo" in captured


def test_format_mushroom_outputs_portuguese_labels():
    mushroom = Mushroom(
        name="Teste",
        edible=False,
        habitat=["floresta"],
        season=["inverno"],
        notes="Exemplo",
    )

    rendered = format_mushroom(mushroom)

    assert "tóxico" in rendered
    assert "estações" in rendered
    assert "notas" in rendered
