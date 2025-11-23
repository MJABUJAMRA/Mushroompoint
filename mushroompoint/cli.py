from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from collections import Counter
from typing import Dict, Iterable, List, Optional, Sequence


DATA_PATH = Path(__file__).resolve().parent / "data" / "mushrooms.json"


@dataclass
class Mushroom:
    name: str
    edible: bool
    habitat: List[str]
    season: List[str]
    notes: str

    @classmethod
    def from_dict(cls, data: dict) -> "Mushroom":
        return cls(
            name=data["name"],
            edible=bool(data["edible"]),
            habitat=list(data["habitat"]),
            season=list(data["season"]),
            notes=data["notes"],
        )

    def matches(
        self,
        habitat: Optional[str] = None,
        season: Optional[str] = None,
        edible: Optional[bool] = None,
    ) -> bool:
        if habitat and habitat.lower() not in (h.lower() for h in self.habitat):
            return False
        if season and season.lower() not in (s.lower() for s in self.season):
            return False
        if edible is not None and self.edible != edible:
            return False
        return True


def load_mushrooms(data_path: Path = DATA_PATH) -> List[Mushroom]:
    with data_path.open("r", encoding="utf-8") as handle:
        raw_mushrooms = json.load(handle)
    return [Mushroom.from_dict(entry) for entry in raw_mushrooms]


def filter_mushrooms(
    mushrooms: Iterable[Mushroom],
    *,
    habitat: Optional[str] = None,
    season: Optional[str] = None,
    edible: Optional[bool] = None,
) -> List[Mushroom]:
    return [m for m in mushrooms if m.matches(habitat=habitat, season=season, edible=edible)]


def summarize_mushrooms(mushrooms: Sequence[Mushroom]) -> Dict[str, object]:
    habitats = set()
    seasons = set()
    edibility = Counter()

    for mushroom in mushrooms:
        habitats.update(mushroom.habitat)
        seasons.update(mushroom.season)
        edibility["edible" if mushroom.edible else "toxic"] += 1

    return {
        "habitat": sorted(habitats),
        "season": sorted(seasons),
        "edible": dict(edibility),
    }


def format_summary(summary: Dict[str, object]) -> str:
    habitats = ", ".join(summary["habitat"]) if summary.get("habitat") else "-"
    seasons = ", ".join(summary["season"]) if summary.get("season") else "-"
    edibility = summary.get("edible", {})
    edible_count = edibility.get("edible", 0)
    toxic_count = edibility.get("toxic", 0)

    return (
        "Opções disponíveis:\n"
        f"  Habitat: {habitats}\n"
        f"  Estações: {seasons}\n"
        f"  Registros comestíveis: {edible_count} | tóxicos: {toxic_count}"
    )


def format_mushroom(mushroom: Mushroom) -> str:
    edibility = "comestível" if mushroom.edible else "tóxico"
    habitats = ", ".join(mushroom.habitat)
    seasons = ", ".join(mushroom.season)
    return (
        f"{mushroom.name} — {edibility}\n"
        f"  habitat: {habitats}\n"
        f"  estações: {seasons}\n"
        f"  notas: {mushroom.notes}"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Filtre anotações de cogumelos por habitat, estação ou comestibilidade "
            "para reduzir o escopo de identificação em campo."
        )
    )
    parser.add_argument(
        "--habitat",
        help="Filtrar por habitat (ex.: forest, logs, pine)",
        metavar="HABITAT",
    )
    parser.add_argument(
        "--season",
        help="Filtrar por estação (ex.: spring, autumn)",
        metavar="SEASON",
    )
    parser.add_argument(
        "--edible",
        choices=["yes", "no"],
        help="Limitar resultados a cogumelos comestíveis ('yes') ou tóxicos ('no')",
    )
    parser.add_argument(
        "--listar",
        "--list",
        action="store_true",
        help="Listar habitats, estações e quantidade de registros antes de filtrar",
    )
    return parser


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    parser = build_parser()
    return parser.parse_args(args=args)


def main(args: Optional[List[str]] = None) -> int:
    parsed_args = parse_args(args)

    edible_flag = None
    if parsed_args.edible == "yes":
        edible_flag = True
    elif parsed_args.edible == "no":
        edible_flag = False

    mushrooms = load_mushrooms()

    if getattr(parsed_args, "listar", False):
        print(format_summary(summarize_mushrooms(mushrooms)))
        return 0

    results = filter_mushrooms(
        mushrooms,
        habitat=parsed_args.habitat,
        season=parsed_args.season,
        edible=edible_flag,
    )

    if not results:
        print("Nenhum cogumelo correspondeu aos filtros. Tente ampliar a busca.")
        return 1

    for mushroom in results:
        print(format_mushroom(mushroom))
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
