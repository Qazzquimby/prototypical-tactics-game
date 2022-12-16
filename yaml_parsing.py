from functools import lru_cache
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel

from domain.complexType import ComplexType
from domain.shape import Shape

data_path = Path(r"data/")


class Token(BaseModel):
    name: str
    image_url: str
    back_image_url: str = None
    size: float = 1


class Card(BaseModel):
    name: str
    tokens: Token = []

    def make_card_row(self, hero_name: str):
        raise NotImplementedError


class UnitCard(Card):
    name: str
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


def read_yaml_file(yaml_path: str) -> dict:
    with open(yaml_path) as yaml_file:
        yaml_content = yaml.safe_load(yaml_file)
    return yaml_content


def make_deck_name(character_name: str):
    return f"{character_name} deck"


def make_box_name(character_name: str):
    return f"{character_name} box"


def make_figurine_name(character_name: str):
    return f"{character_name} figurine"
