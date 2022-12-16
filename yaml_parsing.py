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


class Figurine(BaseModel):
    name: str
    image_url: str
    size: int = 1


class Card(BaseModel):
    name: str
    tokens: list[Token] = None

    def make_content_dict(self, hero_name: str) -> dict:
        raise NotImplementedError

    def get_lua(self) -> str:
        return ""


class UnitCard(Card, Figurine):
    speed: int
    health: int
    dodge: int = 0

    def make_content_dict(self, hero_name: str):
        content_list = [
            self.name,
            SPEED_LABEL,
            str(self.speed),
            HEALTH_LABEL,
            str(self.health),
            hero_name,
        ]
        return {i + 2: value for i, value in enumerate(content_list)}

    def get_lua(self):
        return f"""\
        function onLoad()
              local front='https://live-production.wcms.abc-cdn.net.au/a3e43d3ebfc6102ef6d18feabcb3dcec?impolicy=wcms_crop_resize&cropH=726&cropW=1097&xPos=756&yPos=400&width=862&height=575'
              local back='https://domf5oio6qrcr.cloudfront.net/medialibrary/8862/back-pain-lower-black-man.jpg'
              local name='testtoken'
              local tile_type=2 -- or 2 or 3
              local s=1.0
              local tint={{ r=107/255, g=71/255,  b=28/255  }}
            
              local obj = spawnObject({{
              type = "Custom_Tile",
              position = {{x=-48, y=15, z=10}},
              rotation = {{x=0, y=0, z=0}},
              scale = {{x=s, y=s, z=s}},
              callback_function = function(newObj)
                newObj.setName(name)
                newObj.setColorTint(tint)
              end
            }})
            obj.setCustomObject({{
              type ="Custom_Tile",
              type = tile_type, -- circlef
              image = front,
              image_bottom = back,
              thickness = 0.15,
            }})
        end
        """


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
