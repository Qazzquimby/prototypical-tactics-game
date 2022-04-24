from copy import deepcopy
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel

data_path = Path(r"data/")

Sheets = dict[str: list]


def yaml_string_to_xls(yaml_string: str) -> Sheets:
    decks = yaml.safe_load(yaml_string)
    return decks_to_xls(decks)


class Card(BaseModel):
    name: str

    def make_card_row(self, hero_name: str):
        raise NotImplementedError


class Unit(Card):
    speed: int
    health: int
    size: int = 1

    def make_card_row(self, hero_name: str):
        return [
            self.name, HERO_CARD_LABEL, self.name,
            SPEED_LABEL, str(self.speed),
            HEALTH_LABEL, str(self.health),
            hero_name
        ]


class Hero(Unit):
    def make_card_row(self, hero_name: str):
        return [
            self.name, HERO_CARD_LABEL, self.name,
            SPEED_LABEL, str(self.speed),
            HEALTH_LABEL, str(self.health),
            hero_name
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
    cost: str = ''
    text: str

    def make_card_row(self, hero_name: str):
        return [
            self.name, ABILITY_CARD_LABEL, self.name,
            self.type,
            self.cost,
            self.text,
            hero_name
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


def parse_decks(decks: list[dict]):
    return [Deck.parse_obj(deck) for deck in decks]


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
        ["NAME", "SIZE", "SHAPE - TOPLEFT", "SHAPE - BOTTOMRIGHT", "BG - COLOR", "BACKSIDE", "TYPE", ],
        ["Board", "3000x2500", "A1", "G5", "Brown", "White", "board", ],
        ["HeroCard", "500x500", "A12", "D17", "White", "Black", "card", ],
        ["Ability", "500x500", "A19", "D24", "White", "Black", "card", ],
        ["Field", "500x500", "A19", "D24", "White", "Black", "card", ],
        ["Status", "500x500", "A19", "D24", "White", "Black", "card", ],

    ],
    SheetNames.SHAPES: [
        ["c", "d", "e", "f", "g", "h", "I", ],
        ["j", "k", "l", "m", "n", "o", "p", ],
        ["q", "r", "s", "t", "u", "v", "w", ],
        ["x", "y", "z", "aa", "ab", "ac", "ad", ],
        ["ae", "af", "ag", "ah", "aj", "ak", "al", ],

        ["c", "c", "c", "c", ],
        ["d", "e", "0", "0", ],
        ["f", "g", "0", "0", ],  # Hero cards
        ["h", "I", "0", "0", ],
        ["0", "0", "0", "0", ],
        ["0", "0", "0", "0", ],
        ["c", "c", "c", "d", ],  # Ability cards
        ["e", "e", "e", "e", ],
        ["f", "f", "f", "f", ],
        ["f", "f", "f", "f", ],
        ["f", "f", "f", "f", ],
        ["0", "g", "g", "0", ],

    ],
    SheetNames.COMPLEX_OBJECTS: [
        ["NAME", "TYPE", "CONTENT?"],
        ["GameBoard", "Board"],
    ],
    SheetNames.DECKS: [],
    SheetNames.CONTAINERS: [
        ["NAME", "TYPE", "COLOR", "SIZE", "CONTENTS"],
        ["Characters", "bag", "black", "1"]
    ],
    SheetNames.TOKENS: [
        ["NAME", "ENTITY", "COLOR", "SIZE", "TEXT-COLOR-FRONT", "CONTENT-FRONT", ],
        ["Team1Pawn", "Pawn", "Red", "1"],
        ["Team2Pawn", "Pawn", "Blue", "1"]
    ],
    SheetNames.DICE: [
        ["NAME", "COLOR", "SIZE", "SIDES", "CONTENT?"],
        ["HealthDie", "white", "1", "6"]
    ],
    SheetNames.PLACEMENT: [
        ["", "", "", "", "Characters"]
    ],
}


def make_deck_name(character_name: str):
    return f"{character_name} deck"


def decks_to_xls(decks: list[Deck]) -> Sheets:
    sheets = deepcopy(DEFAULT_XLS)

    for deck in decks:
        deck_name = make_deck_name(deck.hero.name)

        sheets[SheetNames.DECKS].append(["Deck", deck_name])

        # Add cards
        for card in deck.cards:
            sheets[SheetNames.COMPLEX_OBJECTS].append(
                card.make_card_row(deck.hero.name)
            )

            sheets[SheetNames.DECKS].append(
                [card.name, "1"]
            )

        # Setup containers
        sheets[SheetNames.CONTAINERS][1].append(deck_name)

    return sheets


if __name__ == '__main__':
    yaml = """
- hero:
    """

    yaml_string_to_xls()
