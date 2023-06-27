import abc
from functools import lru_cache
from pathlib import Path
from typing import Literal, ClassVar, Optional

import jinja2
import yaml
from pydantic import BaseModel

from domain.bag import CustomBag
from domain.complexObject import ComplexObject
from domain.complexType import ComplexType
from domain.shape import Shape
from drawer.complexObjectDrawer import (
    TemplatesPath,
    EDGE_MARGIN,
    IMAGE_WIDTH,
    IMAGE_HEIGHT,
)
from spawning_lua import get_full_lua, scale_size, clean_string_for_lua
from domain.deck import Deck as DomainDeck
from domain.card import Card as DomainCard

data_path = Path(r"data/")

CARD_HEIGHT = 450
CARD_WIDTH = 350
CARD_SIZE = (CARD_WIDTH, CARD_HEIGHT)


class Spawnable(abc.ABC):
    def get_lua(self) -> str:
        return get_full_lua(self.get_spawning_lua())

    def get_spawning_lua(self):
        raise NotImplementedError


class Token(BaseModel, Spawnable):
    name: str
    image_url: str
    back_image_url: str = ""
    size: float = 0.25

    def get_spawning_lua(self):
        back_image_url = self.back_image_url or self.image_url
        return f"""\
      local front='{self.image_url}'
      local back='{back_image_url}'
      local name='{clean_string_for_lua(self.name)}'
      local s={scale_size(self.size)}
      local tile_type=2
      if s > 0.25 then
        tile_type=3
    end
      
      local my_position = self.getPosition()
      local tint={{ r=0/255, g=0/255,  b=0/255  }}

      local obj = spawnObject({{
      type = "Custom_Tile",
      position = {{x=my_position.x, y=my_position.y+1, z=my_position.z}},
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
      thickness = 0.05,
    }})
        """


class Figurine(BaseModel, Spawnable):
    name: str
    image_url: str
    size: int = 1

    def get_spawning_lua(self):
        return f"""\
    local front='{self.image_url}'
    local name='{clean_string_for_lua(self.name)}'
    local s={scale_size(self.size)}
    local my_position = self.getPosition()

    local obj = spawnObject({{
        type = "Figurine_Custom",
        position = {{x=my_position.x, y=my_position.y+1, z=my_position.z}},
        rotation = {{x=0, y=0, z=0}},
        scale = {{x=s, y=s, z=s}},
        callback_function = function(newObj)
            newObj.setName(name)
        end
    }})
    obj.setCustomObject({{
        type ="Figurine_Custom",
        image = front,
    }})"""


class Ability(BaseModel):
    name: str
    text: str

    def __str__(self):

        # convert markdown to html
        # text_html = markdown.markdown(self.text)
        text_html = "\n".join([f"<p>{line}</p>" for line in self.text.split("\n")])
        return f"<span class='ability-name'>{self.name}:</span> {text_html}"


class Passive(Ability):
    pass


class Active(Ability):
    pass


class Card(BaseModel, Spawnable):
    name: str
    tokens: list[Token] = []

    template: ClassVar[jinja2.Template] = NotImplemented

    def make_content_dict(self, hero_name: str) -> dict:
        raise NotImplementedError

    def get_spawning_lua(self):
        spawning_luas = [token.get_spawning_lua() for token in self.tokens]
        full_spawning_lua = "\n\n\n".join(spawning_luas)
        return full_spawning_lua

    def get_html(self):
        content = self._inner_html()
        html = f"""\
<div class="card">
    {content}
</div>"""

        return html

    def _inner_html(self):
        raise NotImplementedError


class UnitCard(Card, Figurine):
    speed: int
    health: int
    # dodge: int = 0
    passives: list[Passive] = []
    default_ability: Optional[Active] = None

    def _inner_html(self):
        passives = "\n".join([f"<p>{str(passive)}</p" for passive in self.passives])

        content = f"""\
<h1>{self.name}</h1>
<p>Speed: {self.speed}; Health: {self.health}</p>

{passives}

<p>{self.default_ability}</p>
<p>{'owner todo'}</p>
"""

        return content

    @property
    def text(self):
        _text = f"""\
        Speed: {self.speed}
        Health: {self.health}
        """

        # if self.dodge:
        #     _text += f"\nDodge: {self.dodge}"
        if self.size != 1:
            _text += f"\nSize: {self.size}"
        return _text

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

    def get_spawning_lua(self):
        return Card.get_spawning_lua(self) + "\n\n\n" + Figurine.get_spawning_lua(self)


class Hero(UnitCard):
    @staticmethod
    @lru_cache
    def to_complex_type():
        return ComplexType(
            name=HERO_CARD_LABEL,
            backside=(0.0, 0.0, 0.0),
            background_color=(1.0, 1.0, 1.0),
            size=CARD_SIZE,
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


class AbilityCard(Card):
    type: Literal["Basic"] | Literal["Quick"] = BASIC
    text: str

    def _inner_html(self):
        return f"""\
<h1>{self.name}</h1>
<p>{self.type}</p>
<p>{self.text}</p>
<p>{"owner todo"}</p>
"""

    def make_content_dict(self, hero_name: str) -> dict:
        return NotImplemented  # this should replace card row?

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
            size=CARD_SIZE,
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

    abilities: list[AbilityCard] = []
    units: list[UnitCard] = []

    @property
    def cards(self) -> list[Card]:
        return self.abilities + self.units


class HeroBox(BaseModel):
    hero: Hero
    decks: list[Deck]

    # maybe a description here

    def get_tts_obj(self):
        hero_box_bag = CustomBag(
            name=make_box_name(self.hero.name),
            size=1,
            color=(1.0, 0.0, 0.0),
            diffuse_url="http://cloud-3.steamusercontent.com/ugc/1469815174066637129/930D22149972BB2B9C6164FB8D1819249640546B/",
            # todo, generate the image and url like how cards are generated
        )

        if not self.decks:
            self.decks.append(Deck())

        for deck in self.decks:
            deck_name = make_deck_name(
                self.hero.name
            )  # this will need to change when a hero has multiple loadouts

            domain_deck = DomainDeck(name=deck_name)

            hero_card = DomainCard(
                id_=1,
                count=1,
                obj=ComplexObject(
                    name=deck_name,
                    type_=Hero.to_complex_type(),
                    content=self.hero,
                ),
            )

            domain_deck.cards.append(hero_card)

            for card in deck.cards:
                domain_deck.cards.append(
                    DomainCard(
                        id_=len(domain_deck.cards) + 1,
                        count=1,
                        obj=ComplexObject(
                            name=deck_name,
                            type_=AbilityCard.to_complex_type(),
                            # todo make work for other card types
                            content=card,  # no longer used because of jinja rendering
                        ),
                    ),
                )

            hero_box_bag.content.append(domain_deck)

        return hero_box_bag


class GameSet(BaseModel):
    name: str
    hero_boxes: list[HeroBox] = []
    # set rules
    # maps


class Game(BaseModel):
    sets: list[GameSet]


def read_yaml_file(yaml_path: str) -> dict:
    with open(yaml_path, "r", encoding="utf8") as yaml_file:
        yaml_content = yaml.safe_load(yaml_file)
    return yaml_content


def make_deck_name(character_name: str):
    return f"{character_name} deck"


def make_box_name(character_name: str):
    return f"{character_name} box"


def make_figurine_name(character_name: str):
    return f"{character_name} figurine"
