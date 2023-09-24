import abc
import base64
from functools import lru_cache
from pathlib import Path
from typing import ClassVar, Literal, List

import jinja2
import yaml
from pydantic import BaseModel

from domain.bag import Bag
from domain.card import DomainMap
from domain.complexObject import ComplexObject
from domain.complexType import ComplexType
from src.drawing.duplicate_units import duplicate_number_to_letter, make_duplicate_image
from src.drawing.self_host_tokens import TokenImage, get_hosted_address
from src.drawing.size_constants import CARD_SIZE, DIE_SPACING

from src.spawning_lua import get_full_lua, scale_size, clean_string_for_lua
from domain.deck import Deck as DomainDeck
from domain.card import Card as DomainCard

data_path = Path(r"data/")


class Spawnable(abc.ABC):
    def get_lua(self) -> str:
        return get_full_lua(self.get_spawning_lua())

    def get_spawning_lua(self):
        raise NotImplementedError


class Token(BaseModel, Spawnable):
    name: str
    image_url: str
    back_image_url: str = ""
    text: str = ""
    size: float = 0.25

    def get_spawning_lua(self):
        back_image_url = self.back_image_url or self.image_url
        return f"""\
        local front="{get_hosted_address(url=self.image_url, name=self.name)}"
        local back="{get_hosted_address(url=self.back_image_url, name=self.name+'_back')}"
        local name=[[{clean_string_for_lua(self.name)}]]
        local description=[[{clean_string_for_lua(self.text)}]]
        local s={scale_size(self.size)}
        local tile_type=2
        if s > 0.25 then
            tile_type=3
        end
        
        local my_position = self.getPosition()
        local my_rotation = self.getRotation()
        local tint={{ r=0/255, g=0/255,  b=0/255  }}
        
        local obj = spawnObject({{
            type = "Custom_Tile",
            position = {{x=my_position.x+2, y=my_position.y+1, z=my_position.z}},
            rotation = {{x=my_rotation.x, y=my_rotation.y, z=my_rotation.z}},
            scale = {{x=s, y=s, z=s}},
            callback_function = function(newObj)
                newObj.setName(name)
                newObj.setDescription(description)
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
    local front="{get_hosted_address(self.image_url, name=self.name)}"
    local name="{clean_string_for_lua(self.name)}"
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
        lines = self.text.split("\n")
        first_line, *other_lines = lines

        use_colon = bool(
            self.text
        )  # If there's no body text, dont put a hanging colon.
        colon = ":" if use_colon else ""

        ability_line = (
            f"<p><span class='ability-name'>{self.name}{colon}</span> {first_line}</p>"
        )
        other_lines = "\n".join([f"<p>{line}</p>" for line in other_lines])
        text_html = f"{ability_line}\n{other_lines}"
        return text_html


class Passive(Ability):
    pass


class Active(Ability):
    pass


Color = Literal[
    "white",
    "black",
    "brown",
    "red",
    "orange",
    "yellow",
    "green",
    "blue",
    "purple",
    "pink",
    "gray",
]
color_dict = {
    "white": {"r": 1, "g": 1, "b": 1},
    "black": {"r": 0, "g": 0, "b": 0},
    "brown": {"r": 0.588, "g": 0.294, "b": 0},
    "red": {"r": 1, "g": 0, "b": 0},
    "orange": {"r": 1, "g": 0.5, "b": 0},
    "yellow": {"r": 1, "g": 1, "b": 0},
    "green": {"r": 0, "g": 1, "b": 0},
    "blue": {"r": 0, "g": 0, "b": 1},
    "purple": {"r": 0.5, "g": 0, "b": 0.5},
    "pink": {"r": 1, "g": 0, "b": 1},
    "gray": {"r": 0.5, "g": 0.5, "b": 0.5},
}


class Dice(BaseModel):
    name: str
    color: Color
    values: list[int]


class Card(BaseModel, Spawnable):
    name: str
    tokens: list[Token] = []
    dice: list[Dice] = []

    template: ClassVar[jinja2.Template] = NotImplemented

    def make_content_dict(self, hero_name: str) -> dict:
        raise NotImplementedError

    def get_spawning_lua(self):
        spawning_luas = [token.get_spawning_lua() for token in self.tokens]

        for dice_type in self.dice:
            for i, die_value in enumerate(dice_type.values):
                spawning_luas.append(
                    make_spawn_die_lua(
                        name=dice_type.name,
                        die_value=die_value,
                        offset={"x": i * DIE_SPACING, "y": 1, "z": -2},
                        color=color_dict[dice_type.color],
                        scale=0.5,
                    )
                )

        full_spawning_lua = "\n\n\n".join(spawning_luas)
        return full_spawning_lua


unit_image_url_cache = {}


def get_unit_image_url(unit_card, duplicate_number=None):
    if duplicate_number is None:
        return unit_card.image_url

    if unit_card.image_url not in unit_image_url_cache:
        unit_image_url_cache[unit_card.image_url] = {}

    if duplicate_number in unit_image_url_cache[unit_card.image_url]:
        return unit_image_url_cache[unit_card.image_url][duplicate_number]

    duplicate_image = make_duplicate_image(unit_card.image_url, duplicate_number)
    duplicate_image_url = duplicate_image.url
    unit_image_url_cache[unit_card.image_url][duplicate_number] = duplicate_image_url
    return duplicate_image_url


class UnitCard(Card, Figurine):
    speed: int
    health: int
    passives: list[Passive] = []
    default_abilities: list[Active] = []
    count: int = 1

    def get_html(self, duplicate_number=None):
        passives = "\n".join([f"<p>{str(passive)}</p>" for passive in self.passives])
        default_abilities = "\n".join(
            [f"{str(ability)}" for ability in self.default_abilities]
        )

        separator = "<p> - - -</p>" if passives and default_abilities else ""

        image_url = get_unit_image_url(self, duplicate_number)
        safe_url = image_url.replace(" ", "%20").replace("'", "%27")

        duplicate_name = self.name
        if duplicate_number is not None:
            duplicate_name = (
                f"{self.name} {duplicate_number_to_letter(duplicate_number)}"
            )

        content = f"""\
<div class="card" style="background-image: url({safe_url})">
    <p class="card-title-bar">
    <span class="card-name">{duplicate_name}</span>
    <span class="stats">🦶🏼{self.speed} | ❤️{self.health}</span>
    </p>
    
    <span class="card-text">
        {passives}
        {separator}
        {default_abilities}
    </span>
    <p class="owner">owner todo</p>
</div>
"""

        return content

    def get_spawning_lua(self):
        health_dice_values = []
        remaining_health = self.health
        while remaining_health > 0:
            health_die_value = min(remaining_health, 6)
            health_dice_values.append(health_die_value)
            remaining_health -= health_die_value

        health_dice_lua = ""
        for i, health_die_value in enumerate(health_dice_values):

            # position must be relative to the card's rotation.
            health_dice_lua += make_spawn_die_lua(
                die_value=health_die_value,
                offset={"x": i * DIE_SPACING, "y": 1, "z": -2},
                color={"r": 1, "g": 0, "b": 0},
                name="Health",
            )

        full_spawning_lua = (
            health_dice_lua
            + "\n\n\n"
            + Card.get_spawning_lua(self)
            + "\n\n\n"
            + Figurine.get_spawning_lua(self)
        )
        return full_spawning_lua


def make_spawn_die_lua(
    die_value: int, offset: dict, name="", color: dict = None, scale: float = 1
):
    if color is None:
        color = {"r": 1, "g": 1, "b": 1}

    spawn_die_lua = f"""
    local my_position = self.getPosition()
    local my_rotation = self.getRotation()
    local relative_position = {{x={offset['x']}, y={offset['y']}, z={offset['z']}}}
    local world_position = self.positionToWorld(relative_position)

    local health_die = spawnObject({{
        type = "Die_6",
        position = world_position,
        rotation = my_rotation,
        scale = {{x={scale}, y={scale}, z={scale}}},
        callback_function = function(newObj)
            newObj.setName('{name}')
            newObj.setRotationValue({die_value})
            newObj.setColorTint({{r={color['r']}, g={color['g']}, b={color['b']}}})
        end
    }})
    """
    return spawn_die_lua


class Hero(UnitCard):
    description: str
    polish: List[
        Literal["unplayable", "needs_assets", "needs_balance", "needs_testing"]
    ] = []

    @staticmethod
    @lru_cache
    def to_complex_type():
        return ComplexType(
            name=HERO_CARD_LABEL,
            size=CARD_SIZE,
            type_="card",
        )


BASIC = "Basic"
QUICK = "Quick"

UNIT_CARD_LABEL = "Unit"
HERO_CARD_LABEL = "HeroCard"
ABILITY_CARD_LABEL = "Ability"
RULES_CARD_LABEL = "Rules"
SPEED_LABEL = "Speed"
HEALTH_LABEL = "Health"
SIZE_LABEL = "Size"


class RulesCard(Card):
    text: str

    def get_html(self):
        text = "\n".join([f"<p>{line}</p>" for line in self.text.split("\n")])
        html = f"""\
        <div class="card">
            <h1>{self.name}</h1>
            {text}
        </div>"""
        return html

    @staticmethod
    @lru_cache
    def to_complex_type():
        return ComplexType(
            name=RULES_CARD_LABEL,
            size=CARD_SIZE,
            type_="card",
        )


class AbilityCard(Card):
    text: str

    def get_html(self):

        header = f'<p class ="card-title-bar"> <span class ="card-name">{self.name}</span></p>'
        ability_text = "\n".join(
            [
                f"<p style='white-space: pre-wrap;'>{line}</p>"
                for line in self.text.split("\n")
            ]
        )

        content = f"""\
<div class="card">
    {header}
    <span class="card-text">
        {ability_text}
    </span>
    <p class="owner">owner todo</p>
</div>"""
        return content

    def make_content_dict(self, hero_name: str) -> dict:
        return NotImplemented  # this should replace card row?

    @staticmethod
    @lru_cache
    def to_complex_type():
        return ComplexType(
            name=ABILITY_CARD_LABEL,
            size=CARD_SIZE,
            type_="card",
        )


class Deck(BaseModel):
    """One hero can have multiple decks, like a loadout. Maybe call 'loadout' instead"""

    abilities: list[AbilityCard] = []
    units: list[UnitCard] = []

    @property
    def cards(self) -> list[Card]:
        return self.abilities + self.units  # todo split out duplicate units


class RulesDeck(BaseModel):
    cards: list[RulesCard] = []

    def get_tts_obj(self, set_name):
        if not self.cards:
            return None

        deck_name = make_deck_name(f"{set_name}_rules")

        domain_cards = []
        for card in reversed(self.cards):
            domain_cards.append(
                DomainCard(
                    id_=len(domain_cards) + 1,
                    count=1,
                    obj=ComplexObject(
                        name=deck_name,
                        type_=RulesCard.to_complex_type(),
                        content=card,
                    ),
                ),
            )

        domain_deck = DomainDeck.from_cards(
            set_name=set_name, name=deck_name, cards=domain_cards
        )
        return domain_deck


class HeroDeck(Hero, Deck):
    def get_tts_obj(self, set_name: str):
        deck_name = make_deck_name(self.name)

        domain_cards = []
        for card in reversed(self.cards):
            domain_cards.append(
                DomainCard(
                    id_=len(domain_cards) + 1,
                    count=1,
                    obj=ComplexObject(
                        name=deck_name,
                        type_=AbilityCard.to_complex_type(),  # this is used regardless of type
                        content=card,
                    ),
                ),
            )

        hero_card = DomainCard(
            id_=len(domain_cards) + 1,
            count=1,
            obj=ComplexObject(
                name=deck_name,
                type_=Hero.to_complex_type(),
                content=self,
            ),
        )
        domain_cards.append(hero_card)

        domain_deck = DomainDeck.from_cards(
            set_name=set_name, name=deck_name, cards=domain_cards
        )
        return domain_deck


class Map(Spawnable, BaseModel):
    name: str
    image_path: str

    tokens: list[Token] = []

    size_: tuple[int, int] = None

    @property
    def width_height(self):
        if self.size_ is None:
            import cv2

            image = cv2.imread((data_path / "maps" / self.image_path).as_posix())
            height = image.shape[0]
            width = image.shape[1]
            size = (width, height)
            self.size_ = size
        return self.size_

    def get_spawning_lua(self):
        spawning_luas = [token.get_spawning_lua() for token in self.tokens]
        full_spawning_lua = "\n\n\n".join(spawning_luas)
        return full_spawning_lua

    def get_html(self):
        local_image_path = data_path / "maps" / self.image_path
        image_bytes = local_image_path.read_bytes()
        image_data = base64.b64encode(image_bytes).decode()

        html = f"""\
<div class="map">    
    <img src="data:image/jpeg;base64,{image_data}" style="height: 100%; width: 100%; object-fit: contain;"/>
</div>"""
        return html

    def get_tts_obj(self):
        bag = Bag(
            name=make_box_name(self.name),
            description="",
            size=1,
            color=(1.0, 1.0, 1.0),
        )

        width, height = self.width_height

        map_ = DomainMap(
            obj=ComplexObject(
                name=make_deck_name(self.name),
                type_=ComplexType(
                    name="Map",
                    size=(width, height),
                    type_="card",
                ),
                content=self,
            ),
            local_path=self.image_path,
        )
        bag.contained_objects.append(map_)

        return bag


class GameSet(BaseModel):
    name: str
    description: str
    rules: list[RulesCard] = []
    heroes: list[HeroDeck] = []
    maps: list[Map] = []


class Game(BaseModel):
    rules: list[RulesCard] = []
    sets: list[GameSet]

    def get_token_images(self):
        token_images: list[TokenImage] = []
        for game_set in self.sets:
            for hero in game_set.heroes:
                for card in hero.cards:
                    if isinstance(card, UnitCard):
                        token_image = TokenImage(url=card.image_url, name=card.name)
                        token_images.append(token_image)
                    for token in card.tokens:
                        token_image = TokenImage(url=token.image_url, name=token.name)
                        token_images.append(token_image)
                        if token.back_image_url:
                            token_image = TokenImage(
                                url=token.back_image_url, name=token.name + "_back"
                            )
                            token_images.append(token_image)
        return token_images


def read_yaml_file(yaml_path: str) -> dict:
    with open(yaml_path, "r", encoding="utf8") as yaml_file:
        yaml_content = yaml.safe_load(yaml_file)
    return yaml_content


def write_yaml_file(path: str, content_dict: dict):
    with open(path, "w", encoding="utf8") as yaml_file:
        yaml.safe_dump(content_dict, yaml_file, sort_keys=False, allow_unicode=True)


def make_deck_name(character_name: str):
    return character_name
    # return f"{character_name} deck"


def make_box_name(character_name: str):
    return f"{character_name} box"


def make_figurine_name(character_name: str):
    return f"{character_name} figurine"


# {'1': {'FaceURL': 'file:///D:\\Users\\User\\PycharmProjects\\prototypical-tactics-game\\data\\images\\game rules deck.jpg', 'BackURL': 'file:///D:\\Users\\User\\PycharmProjects\\prototypical-tactics-game\\data\\images\\game rules deck_back.jpg', 'NumWidth': 10, 'NumHeight': 7, 'BackIsHidden': False, 'UniqueBack': False}}
# {'Name': 'Card', 'Transform': {'posX': 1, 'posY': 1, 'posZ': 1, 'rotX': 0, 'rotY': 0, 'rotZ': 0, 'scaleX': 1, 'scaleY': 1, 'scaleZ': 1}, 'Nickname': 'game rules deck', 'Description': '', 'ColorDiffuse': {'r': 0.713235259, 'g': 0.713235259, 'b': 0.713235259}, 'Locked': False, 'Grid': True, 'Snap': True, 'Autoraise': True, 'Sticky': True, 'Tooltip': True, 'GridProjection': False, 'Hands': True, 'CardID': 100, 'SidewaysCard': False, 'LuaScript': 'function onLoad()\n    local has_spawned = false\nend\n\nfunction onDrop(player_color)\n    if has_spawned then\n        return\n    end\n    has_spawned = true  \n    spawnSelf()\nend\n\nfunction spawnSelf()\n    \nend\n', 'LuaScriptState': '', 'ContainedObjects': [], 'GUID': 'f981cff1dd904b48b68320404b3a2e50'}

# {'FaceURL': 'file:///D:\\Users\\User\\PycharmProjects\\prototypical-tactics-game\\data\\images\\Ana deck.jpg',              'BackURL': 'file:///D:\\Users\\User\\PycharmProjects\\prototypical-tactics-game\\data\\images\\Ana deck_back.jpg',        'NumWidth': 10, 'NumHeight': 7, 'BackIsHidden': False, 'UniqueBack': False}
# {'Name': 'Card', 'Transform': {'posX': 1, 'posY': 1, 'posZ': 1, 'rotX': 0, 'rotY': 0, 'rotZ': 0, 'scaleX': 1, 'scaleY': 1, 'scaleZ': 1}, 'Nickname': 'Ana deck',        'Description': '', 'ColorDiffuse': {'r': 0.713235259, 'g': 0.713235259, 'b': 0.713235259}, 'Locked': False, 'Grid': True, 'Snap': True, 'Autoraise': True, 'Sticky': True, 'Tooltip': True, 'GridProjection': False, 'Hands': True, 'CardID': 100, 'SidewaysCard': False, 'LuaScript': 'function onLoad()\n    local has_spawned = false\nend\n\nfunction onDrop(player_color)\n    if has_spawned then\n        return\n    end\n    has_spawned = true  \n    spawnSelf()\nend\n\nfunction spawnSelf()\n                         tate': '', 'ContainedObjects': [], 'GUID': '8a65d1fae16841ba844d1ee5357239b0'}
