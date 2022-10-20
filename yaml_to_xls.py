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
    # maybe a description here


class GameSet(BaseModel):
    name: str
    hero_boxes: list[HeroBox] = []
    # set rules
    # maps


class Game(BaseModel):
    sets: list[GameSet]


def parse_game(game_structure):
    return Game.parse_obj(game_structure)


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
    SheetNames.PLACEMENT: [["", "", "", "", "Characters"]],
}


def make_deck_name(character_name: str):
    return f"{character_name} deck"


def make_box_name(character_name: str):
    return f"{character_name} box"


def game_to_xls(game: Game) -> Sheets:
    sheets = deepcopy(DEFAULT_XLS)

    for game_set in game.sets:
        game_set_to_xlsx(game_set, sheets)

    return sheets


def game_set_to_xlsx(game_set: GameSet, sheets: Sheets) -> Sheets:
    container_row = [game_set.name, "bag", "black", "2"]
    sheets[SheetNames.CONTAINERS][1].append(game_set.name)

    # Make a bag for each set
    for hero_box in game_set.hero_boxes:
        hero_box_to_xlsx(hero_box, sheets)
        container_row.append(make_box_name(hero_box.hero.name))

    sheets[SheetNames.CONTAINERS].append(container_row)


def hero_box_to_xlsx(hero_box: HeroBox, sheets: Sheets) -> Sheets:
    container_row = [make_box_name(hero_box.hero.name), "bag", "red", "1"]

    sheets[SheetNames.COMPLEX_OBJECTS].append(
        hero_box.hero.make_card_row(hero_box.hero.name)
    )

    # refactor this into separate methods make_deck and add_cards
    if not hero_box.decks:
        deck_name = make_deck_name(hero_box.hero.name)
        sheets[SheetNames.DECKS].append(["Deck", make_deck_name(hero_box.hero.name)])
        sheets[SheetNames.DECKS].append([hero_box.hero.name, "1"])
        container_row.append(deck_name)

    for deck in hero_box.decks:
        deck_name = make_deck_name(
            hero_box.hero.name
        )  # this will need to change when a hero has multiple loadouts
        container_row.append(deck_name)

        # Add cards
        for card in deck.cards:
            sheets[SheetNames.COMPLEX_OBJECTS].append(
                card.make_card_row(hero_box.hero.name)
            )

            sheets[SheetNames.DECKS].append([card.name, "1"])
    sheets[SheetNames.CONTAINERS].append(container_row)


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
    with open("data/game_schema.json", "w") as f:
        f.write(schema)

    src = "data/input.yaml"
    dest = "dest/output.xls"

    sheets = file_to_xls(src=src, dest=dest)
    print("debug")
