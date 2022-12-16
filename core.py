import asyncio
import json
from pathlib import Path

from pygame import Surface

from creator.entityCreator import EntityCreator
from domain.bag import Bag
from domain.card import Card
from domain.complexObject import ComplexObject
from domain.complexType import ComplexType
from domain.deck import Deck as DomainDeck
from domain.library import Library
from domain.token import ContentToken
from drawer.base import BaseDrawer
from drawer.cardBackDrawer import CardBackDrawer
from drawer.deckDrawer import DeckDrawer
from image_builders import ImageBuilder
from yaml_parsing import (
    GameSet,
    make_box_name,
    HeroBox,
    Deck,
    make_deck_name,
    Hero,
    Ability,
)

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

    return library


def make_game_set_bag(game_set: GameSet):
    bag = Bag(name=game_set.name, size=2, color=(0.0, 0.0, 0.0))

    # Make a bag for each set
    for hero_box in game_set.hero_boxes:
        hero_box_bag = make_hero_box_bag(hero_box)
        bag.content.append(hero_box_bag)

    return bag


def make_hero_box_bag(hero_box: HeroBox):
    hero_box_bag = Bag(
        name=make_box_name(hero_box.hero.name), size=1, color=(1.0, 0.0, 0.0)
    )

    # figurine_name = make_figurine_name(hero_box.hero.name)
    # hero_box_bag.content.append(
    #     Figurine(
    #         name=figurine_name,
    #         size=hero_box.hero.size,
    #         image_path=hero_box.hero.image_url,
    #     )
    # ) #todo remove
    # instead of putting the figurine in the bag, spawn it on demand when the card is drawn

    if not hero_box.decks:
        hero_box.decks.append(Deck())

    for deck in hero_box.decks:
        deck_name = make_deck_name(
            hero_box.hero.name
        )  # this will need to change when a hero has multiple loadouts

        domain_deck = DomainDeck(name=deck_name)

        hero_card = Card(
            id_=1,
            count=1,
            obj=ComplexObject(
                name=hero_box.hero.name,
                type_=Hero.to_complex_type(),
                content=hero_box.hero,
            ),
        )

        domain_deck.cards.append(hero_card)

        for card in deck.cards:
            domain_deck.cards.append(
                Card(
                    id_=len(domain_deck.cards) + 1,
                    count=1,
                    obj=ComplexObject(
                        name=deck_name,
                        type_=Ability.to_complex_type(),
                        # todo make work for other card types
                        content=card,  # no longer used because of jinja rendering
                    ),
                ),
            )

        hero_box_bag.content.append(domain_deck)

    return hero_box_bag


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
    setup_pygame()

    tts_dict = read_template_dict(file_name)
    drawer = DeckDrawer(config)

    coroutines = []
    for deck in library.decks:
        coroutines.append(
            _save_image_and_set_attribute(
                image_builder=image_builder,
                drawer=drawer,
                object_=deck,
                file_name=deck.name,
                file_extension="jpg",
                attribute_to_set="image_path",
            )
        )

    drawer = CardBackDrawer(config)
    for deck in library.decks:
        coroutines.append(
            _save_image_and_set_attribute(
                image_builder=image_builder,
                drawer=drawer,
                object_=deck,
                file_name=f"{deck.name}_back",
                file_extension="jpg",
                attribute_to_set="back_image_path",
            )
        )

    for obj in library.complex_objects:
        if obj.type.type == "board":
            coroutines.append(
                _save_image_and_set_attribute(
                    image_builder=image_builder,
                    drawer=drawer,
                    object_=obj,
                    file_name=obj.name,
                    file_extension="jpg",
                    attribute_to_set="image_path",
                )
            )

    for token in library.tokens:
        if isinstance(token, ContentToken):
            coroutines.append(
                _save_image_and_set_attribute(
                    image_builder=image_builder,
                    drawer=drawer,
                    object_=token,
                    file_name="token_" + token.name,
                    file_extension="jpg",
                    attribute_to_set="image_path",
                )
            )

    for die in library.dice:
        if die.custom_content:
            coroutines.append(
                _save_image_and_set_attribute(
                    image_builder=image_builder,
                    drawer=drawer,
                    object_=die,
                    file_name="die" + die.name,
                    file_extension="png",
                    attribute_to_set="image_path",
                )
            )
    await asyncio.gather(*coroutines)

    entities = library.all()
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
    image: Surface = drawer.draw(object_)
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
