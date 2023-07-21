import asyncio
import json
from pathlib import Path
from typing import Union, Coroutine

from pygame import Surface

from domain.bag import Bag

from domain.complexObject import ComplexObject
from domain.complexType import ComplexType

from domain.library import Library, get_hero_boxes
from domain.token import ContentToken
from drawer.base import BaseDrawer
from drawer.cardBackDrawer import CardBackDrawer
from drawer.complexObjectDrawer import close_browser
from drawer.deckDrawer import DeckDrawer
from drawer.heroBoxDrawer import HeroBoxDrawer
from image_builders import ImageBuilder
from yaml_parsing import GameSet, RulesDeck

DEFAULT_LIBRARY = Library(
    tokens=[],
    dice=[],
    complex_objects=[],
    decks=[],
    bags=[],
)


def game_to_library(game):
    library = Library(
        tokens=[],
        dice=[],
        complex_objects=[],
        decks=[],
        bags=[],
    )

    sets_bag = Bag(name="Sets", size=3, color=(1.0, 1.0, 1.0))
    for game_set in game.sets:
        game_set_bag = make_game_set_bag(game_set)
        sets_bag.content.append(game_set_bag)
    library.bags.append(sets_bag)

    rules_deck = RulesDeck(cards=game.rules)
    domain_rules_deck = rules_deck.get_tts_obj()
    library.bags[0].content.append(domain_rules_deck)

    return library


def make_game_set_bag(game_set: GameSet):
    bag = Bag(
        name=game_set.name,
        description=game_set.description,
        size=2,
        color=(0.0, 0.0, 0.0),
    )

    rules_deck = RulesDeck(cards=game_set.rules)
    domain_rules_deck = rules_deck.get_tts_obj()
    if domain_rules_deck:
        bag.content.append(domain_rules_deck)

    # Make a bag for each set
    for hero_box in game_set.hero_boxes:
        hero_box_bag = hero_box.get_tts_obj()
        bag.content.append(hero_box_bag)

    return bag


def complex_object_row_to_complex_object(
    row: list, type_: ComplexType
) -> ComplexObject:
    return ComplexObject(name=row[0], type_=type_, content=dict(row[2:]))


async def library_to_tts_dict(
    library: Library,
    image_builder: ImageBuilder,
    file_name,
    config=None,
):
    await image_builder.initialize()
    setup_pygame()

    tts_dict = read_template_dict(file_name)

    coroutines = []

    deck_drawer = DeckDrawer(config)
    back_drawer = CardBackDrawer(config)

    # todo render images for LoneCards

    for deck in library.decks:
        coroutines.append(
            _save_image_and_set_attribute(
                image_builder=image_builder,
                drawer=deck_drawer,
                object_=deck,
                file_name=deck.name,
                file_extension="jpg",
                attribute_to_set="image_path",
            )
        )

        coroutines.append(
            _save_image_and_set_attribute(
                image_builder=image_builder,
                drawer=back_drawer,
                object_=deck,
                file_name=f"{deck.name}_back",
                file_extension="jpg",
                attribute_to_set="back_image_path",
            )
        )

    hero_box_drawer = HeroBoxDrawer(config)
    hero_boxes = get_hero_boxes(library)
    for hero_box in hero_boxes:
        coroutines.append(
            _save_image_and_set_attribute(
                image_builder=image_builder,
                drawer=hero_box_drawer,
                object_=hero_box,
                file_name=hero_box.name,
                file_extension="jpg",
                attribute_to_set="diffuse_url",
            )
        )

    for token in library.tokens:
        if isinstance(token, ContentToken):
            coroutines.append(
                _save_image_and_set_attribute(
                    image_builder=image_builder,
                    drawer=back_drawer,  # todo why? Seems to work though.
                    object_=token,
                    file_name="token_" + token.name,
                    file_extension="jpg",
                    attribute_to_set="image_path",
                )
            )

    await asyncio.gather(*coroutines)
    await close_browser()

    entities = library.bags  # will need to change for games that are more than one bag
    tts_dict["ObjectStates"] = [entity.as_dict() for entity in entities]

    return tts_dict


async def _save_image_and_set_attribute(
    image_builder: ImageBuilder,
    drawer: BaseDrawer,
    object_,
    file_name: str,
    file_extension: str,
    attribute_to_set: str,
):
    image: Union[Surface, Coroutine[Surface]] = drawer.draw(object_)
    # if image is promise, resolve
    if isinstance(image, Coroutine):
        image = await image
    path = await image_builder.build(
        image=image, file_name=file_name, file_extension=file_extension
    )
    object_.__setattr__(attribute_to_set, path)


def save_tts(tts_json: dict, save_dir: Path, file_name: str):
    path = save_dir / f"TS_{file_name.replace(' ', '_')}.json"
    with open(path, "w") as outfile:
        json.dump(tts_json, outfile)


def setup_pygame():
    # setup pygame as drawing library
    import pygame

    pygame.init()


def read_template_dict(file_name: str):
    # open save template
    with open("data/template.json", "r") as infile:
        data = json.load(infile)
        data["SaveName"] = file_name
    return data
