from copy import deepcopy
from pathlib import Path
from typing import Literal

import pyexcel
import yaml
from pydantic import BaseModel

data_path = Path(r"data/")

Sheets = dict[str:list]


def yaml_string_to_xls(yaml_string: str) -> Sheets:
    decks = yaml.safe_load(yaml_string)
    return game_to_xls(decks)


class Card(BaseModel):
    name: str

    def make_card_row(self, hero_name: str):
        raise NotImplementedError


class Unit(Card):
    speed: int
    health: int
    size: int = 1
    dodge: int = 0

    def make_card_row(self, hero_name: str):
        return [
            self.name,
            HERO_CARD_LABEL,
            self.name,
            SPEED_LABEL,
            str(self.speed),
            HEALTH_LABEL,
            str(self.health),
            hero_name,
        ]


class Hero(Unit):
    def make_card_row(self, hero_name: str):
        return [
            self.name,
            HERO_CARD_LABEL,
            self.name,
            SPEED_LABEL,
            str(self.speed),
            HEALTH_LABEL,
            str(self.health),
            SPEED_LABEL,
            str(self.speed),
            hero_name,
        ]


BASIC = "Basic"
QUICK = "Quick"

UNIT_CARD_LABEL = "Unit"
HERO_CARD_LABEL = "HeroCard"
ABILITY_CARD_LABEL = "Ability"
SPEED_LABEL = "Speed"
HEALTH_LABEL = "Health"
SIZE_LABEL = "Size"


class Ability(Card):
    type: Literal["Basic"] | Literal["Quick"] = BASIC
    cost: str = ""
    text: str

    def make_card_row(self, hero_name: str):
        return [
            self.name,
            ABILITY_CARD_LABEL,
            self.name,
            self.type,
            self.cost,
            self.text,
            hero_name,
        ]


class Deck(BaseModel):
    hero: Unit
    abilities: list[Ability] = []
    units: list[Unit] = []

    @property
    def cards(self) -> list[Card]:
        return [self.hero] + self.abilities + self.units


class Game(BaseModel):
    decks: list[Deck]


def parse_game(game):
    return Game.parse_obj(game)


class SheetNames:
    COMPLEX_TYPES = "ComplexTypes"
    SHAPES = "Shapes"
    COMPLEX_OBJECTS = "ComplexObjects"
    CONTAINERS = "Containers"
    DICE = "Dice"
    DECKS = "Decks"
    TOKENS = "Tokens"
    PLACEMENT = "Placement"


DEFAULT_XLS = {
    SheetNames.COMPLEX_TYPES: [
        [
            "NAME",
            "SIZE",
            "SHAPE - TOPLEFT",
            "SHAPE - BOTTOMRIGHT",
            "BG - COLOR",
            "BACKSIDE",
            "TYPE",
        ],
        ["Board", "3000x2500", "A1", "G5", "Brown", "White", "board"],
        ["HeroCard", "500x500", "A6", "D11", "White", "Black", "card"],
        ["Ability", "500x500", "A12", "D17", "White", "Black", "card"],
        ["Field", "500x500", "A12", "D17", "White", "Black", "card"],
        ["Status", "500x500", "A12", "D17", "White", "Black", "card"],
    ],
    SheetNames.SHAPES: [
        ["c", "d", "e", "f", "g", "h", "I"],
        ["j", "k", "l", "m", "n", "o", "p"],
        ["q", "r", "s", "t", "u", "v", "w"],
        ["x", "y", "z", "aa", "ab", "ac", "ad"],
        ["ae", "af", "ag", "ah", "aj", "ak", "al"],
        ["c", "c", "c", "c"],  # Hero cards
        ["d", "e", 0, 0],
        ["f", "g", 0, 0],
        ["h", "I", 0, 0],
        [0, 0, 0, 0],
        [0, "j", "j", 0],
        ["c", "c", "c", "d"],  # Ability cards
        ["e", "e", "e", "e"],
        ["f", "f", "f", "f"],
        ["f", "f", "f", "f"],
        ["f", "f", "f", "f"],
        [0, "g", "g", 0],
    ],
    SheetNames.COMPLEX_OBJECTS: [
        ["NAME", "TYPE", "CONTENT?"],
        ["GameBoard", "Board"] + ["."] * 100,
    ],
    SheetNames.DECKS: [],
    SheetNames.CONTAINERS: [
        ["NAME", "TYPE", "COLOR", "SIZE", "CONTENTS"],
        ["Characters", "bag", "black", "1"],
    ],
    SheetNames.TOKENS: [
        [
            "NAME",
            "ENTITY",
            "COLOR",
            "SIZE",
            "TEXT-COLOR-FRONT",
            "CONTENT-FRONT",
        ],
        ["Team1Pawn", "Pawn", "Red", "1"],
        ["Team2Pawn", "Pawn", "Blue", "1"],
    ],
    SheetNames.DICE: [
        ["NAME", "COLOR", "SIZE", "SIDES", "CONTENT?"],
        ["HealthDie", "white", "1", "6"],
    ],
    SheetNames.PLACEMENT: [["", "", "", "", "Characters"]],
}


def make_deck_name(character_name: str):
    return f"{character_name} deck"


def game_to_xls(game: Game) -> Sheets:
    sheets = deepcopy(DEFAULT_XLS)

    for deck in game.decks:
        deck_name = make_deck_name(deck.hero.name)

        sheets[SheetNames.DECKS].append(["Deck", deck_name])

        # Add cards
        for card in deck.cards:
            sheets[SheetNames.COMPLEX_OBJECTS].append(
                card.make_card_row(deck.hero.name)
            )

            sheets[SheetNames.DECKS].append([card.name, "1"])

        # Setup containers
        sheets[SheetNames.CONTAINERS][1].append(deck_name)

    return sheets


def file_to_xls(src, dest=None) -> Sheets:
    with open(src) as yaml_file:
        game_structure = yaml.safe_load(yaml_file)
    game = parse_game(game_structure)
    sheets = game_to_xls(game)
    if dest is not None:
        pyexcel.save_book_as(bookdict=sheets, dest_file_name=str(dest))
    return sheets


if __name__ == "__main__":
    schema = Game.schema_json()

    src = "data/input.yaml"
    dest = "dest/output.xls"

    sheets = file_to_xls(src=src, dest=dest)
    print("debug")
