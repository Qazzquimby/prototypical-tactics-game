from copy import deepcopy
from functools import lru_cache
from pathlib import Path
from typing import Literal

import pyexcel
import yaml
from pydantic import BaseModel

from domain.complexType import ComplexType
from domain.shape import Shape

data_path = Path(r"data/")

Sheets = dict[str:list]


class Card(BaseModel):
    name: str

    def make_card_row(self, hero_name: str):
        raise NotImplementedError


class Token(BaseModel):
    name: str

    def make_token_row(self):
        raise NotImplementedError


class UnitCard(Card, Token):
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

    def make_token_row(self):
        return [
            self.name,
            "token",
            "\\",
            self.size,
            "black",
            "the content!",
        ]


class Hero(UnitCard):
    pass

    @staticmethod
    @lru_cache
    def to_complex_type():
        return ComplexType(
            name=HERO_CARD_LABEL,
            backside=(0.0, 0.0, 0.0),
            background_color=(1.0, 1.0, 1.0),
            size=(500, 500),
            type_="card",
            shape=Shape(
                areas={
                    2: (0, 0, 0, 3),
                    3: (1, 0, 1, 0),
                    4: (1, 1, 1, 1),
                    5: (2, 0, 2, 0),
                    6: (2, 1, 2, 1),
                    7: (3, 0, 3, 0),
                    8: (3, 1, 3, 1),
                    9: (5, 1, 5, 2),
                },
                size=(4, 6),
            ),
        )


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

    @staticmethod
    @lru_cache
    def to_complex_type():
        return ComplexType(
            name=ABILITY_CARD_LABEL,
            backside=(0.0, 0.0, 0.0),
            background_color=(1.0, 1.0, 1.0),
            size=(500, 500),
            type_="card",
            shape=Shape(
                areas={
                    2: (0, 0, 0, 2),
                    3: (0, 3, 0, 3),
                    4: (1, 0, 1, 3),
                    5: (2, 0, 4, 3),
                    6: (5, 1, 5, 2),
                },
                size=(4, 6),
            ),
        )


class Deck(BaseModel):
    """One hero can have multiple decks, like a loadout. Maybe call 'loadout' instead"""

    abilities: list[Ability] = []
    units: list[UnitCard] = []

    @property
    def cards(self) -> list[Card]:
        return self.abilities + self.units


class HeroBox(BaseModel):
    hero: Hero
    decks: list[Deck]
    tokens: list[Token] = []
    image: str
    # maybe a description here


class GameSet(BaseModel):
    name: str
    hero_boxes: list[HeroBox] = []
    # set rules
    # maps


class Game(BaseModel):
    sets: list[GameSet]


class SheetNames:
    COMPLEX_TYPES = "ComplexTypes"
    SHAPES = "Shapes"
    COMPLEX_OBJECTS = "ComplexObjects"
    CONTAINERS = "Containers"
    DICE = "Dice"
    DECKS = "Decks"
    TOKENS = "Tokens"
    PLACEMENT = "Placement"
    FIGURINES = "Figurines"


DEFAULT_SHEETS = {
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
        ["Sets", "bag", "white", "3"]
        # default is game sets
        # in game sets are hero boxes
        # in hero boxes are decks (not bags)  ["Characters", "bag", "black", "1"],
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
    SheetNames.PLACEMENT: [["", "", "", "", "Sets"]],
    SheetNames.FIGURINES: [["NAME", "SIZE", "IMAGE-PATH"]],
}


def yaml_file_to_xls_file(yaml_path: str, dest=None) -> Sheets:
    yaml_content = read_yaml_file(yaml_path)

    sheets = yaml_content_to_sheets(yaml_content)

    if dest is not None:
        pyexcel.save_book_as(bookdict=sheets, dest_file_name=str(dest))
    return sheets


def read_yaml_file(yaml_path: str) -> dict:
    with open(yaml_path) as yaml_file:
        yaml_content = yaml.safe_load(yaml_file)
    return yaml_content


def yaml_content_to_sheets(yaml_content: dict) -> Sheets:
    game = Game.parse_obj(yaml_content)
    sheets = game_to_sheets(game)
    return sheets


def game_to_sheets(game: Game) -> Sheets:
    sheets = deepcopy(DEFAULT_SHEETS)

    for game_set in game.sets:
        game_set_to_sheets(game_set, sheets)

    return sheets


def make_deck_name(character_name: str):
    return f"{character_name} deck"


def make_box_name(character_name: str):
    return f"{character_name} box"


def make_figurine_name(character_name: str):
    return f"{character_name} figurine"


def game_set_to_sheets(game_set: GameSet, sheets: Sheets) -> Sheets:
    container_row = [game_set.name, "bag", "black", "2"]
    sheets[SheetNames.CONTAINERS][1].append(game_set.name)

    # Make a bag for each set
    for hero_box in game_set.hero_boxes:
        hero_box_to_sheets(hero_box, sheets)
        container_row.append(make_box_name(hero_box.hero.name))

    sheets[SheetNames.CONTAINERS].append(container_row)


def hero_box_to_sheets(hero_box: HeroBox, sheets: Sheets) -> Sheets:
    container_row = [make_box_name(hero_box.hero.name), "bag", "red", "1"]

    sheets[SheetNames.COMPLEX_OBJECTS].append(
        hero_box.hero.make_card_row(hero_box.hero.name)
    )

    figurine_name = make_figurine_name(hero_box.hero.name)
    sheets[SheetNames.FIGURINES].append(
        [figurine_name, hero_box.hero.size, hero_box.image]
    )
    container_row.append(figurine_name)

    if not hero_box.decks:
        hero_box.decks.append(Deck())

    for deck in hero_box.decks:
        deck_name = make_deck_name(
            hero_box.hero.name
        )  # this will need to change when a hero has multiple loadouts

        sheets[SheetNames.DECKS] += [["Deck", deck_name], [hero_box.hero.name, "1"]]
        container_row.append(deck_name)

        # Add cards
        for card in deck.cards:
            sheets[SheetNames.COMPLEX_OBJECTS].append(
                card.make_card_row(hero_box.hero.name)
            )
            sheets[SheetNames.DECKS].append([card.name, "1"])

    sheets[SheetNames.CONTAINERS].append(container_row)


if __name__ == "__main__":
    schema = Game.schema_json()
    with open("data/game_schema.json", "w") as f:
        f.write(schema)

    src = "data/input.yaml"
    dest = "dest/output.xls"

    sheets = yaml_file_to_xls_file(yaml_path=src, dest=dest)
    print("debug")
