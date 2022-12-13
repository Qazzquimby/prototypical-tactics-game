import asyncio
import json
from pathlib import Path

import xlrd
from pygame import Surface

from creator.entityCreator import EntityCreator
from domain.bag import Bag
from domain.card import Card
from domain.complexObject import ComplexObject
from domain.complexType import ComplexType
from domain.deck import Deck as DomainDeck
from domain.figurine import Figurine
from domain.library import Library
from domain.token import ContentToken
from drawer.base import BaseDrawer
from drawer.cardBackDrawer import CardBackDrawer
from drawer.complexObjectDrawer import ComplexObjectDrawer
from drawer.deckDrawer import DeckDrawer
from drawer.diceDrawer import DiceDrawer
from drawer.tokenDrawer import TokenDrawer
from image_builders import ImageBuilder
from sheetParser.bagParser import BagParser
from sheetParser.complexObjectParser import ComplexObjectParser
from sheetParser.complexTypeParser import ComplexTypeParser
from sheetParser.deckParser import DeckParser
from sheetParser.diceParser import DiceParser
from sheetParser.figurineParser import FigurineParser
from sheetParser.tokenParser import TokenParser
from yaml_to_xls import (
    GameSet,
    make_box_name,
    HeroBox,
    make_figurine_name,
    Deck,
    make_deck_name,
    Hero,
    Ability,
)


async def xls_file_to_tts_save(
    xls_file_path, image_builder, save_dir, file_name, config=None
):
    print("Depreciate this, go straight from yaml using sheets_to_tts_json")
    sheets = xlrd.open_workbook(xls_file_path)

    tts_json = await sheets_to_tts_json(sheets, image_builder, file_name, config)

    save_tts(tts_json=tts_json, save_dir=save_dir, file_name=file_name)


async def sheets_to_tts_json(sheets: dict, image_builder, file_name, config=None):
    library = sheets_to_library(sheets)
    return await library_to_tts_dict(
        library, image_builder, file_name, sheets["Placement"], config
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


def card_row_to_content_dict(row: list):
    no_label = row[2:]
    return {i + 2: value for i, value in enumerate(no_label)}


def make_hero_box_bag(hero_box: HeroBox):
    hero_box_bag = Bag(
        name=make_box_name(hero_box.hero.name), size=1, color=(1.0, 0.0, 0.0)
    )

    figurine_name = make_figurine_name(hero_box.hero.name)
    hero_box_bag.content.append(
        Figurine(
            name=figurine_name,
            size=hero_box.hero.size,
            image_path=hero_box.image,
        )
    )

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
                content=card_row_to_content_dict(
                    hero_box.hero.make_card_row(hero_box.hero.name)
                ),
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
                        type_=Ability.to_complex_type(),  # todo make work for other card types
                        content=card_row_to_content_dict(card.make_card_row(card.name)),
                    ),
                )
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
    placement=None,
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
            drawer = ComplexObjectDrawer(obj, config)
            path = await image_builder.build(drawer.draw(), obj.name, "jpg")
            obj.image_path = path

    for token in library.tokens:
        if isinstance(token, ContentToken):
            drawer = TokenDrawer(token)
            path = await image_builder.build(
                drawer.draw(), "token_" + token.name, "jpg"
            )
            token.image_path = path

    for die in library.dice:
        if die.custom_content:
            drawer = DiceDrawer(die)
            path = await image_builder.build(drawer.draw(), "die" + die.name, "png")
            die.image_path = path

    await asyncio.gather(*coroutines)

    # UGLY - we already did this step during parsing, but we need to create entities AFTER drawing or their image paths aren't set
    creator = EntityCreator(library.all())
    entities = creator.create_entities(placement)

    dicts = []
    for entity in entities:
        dicts.append(entity.as_dict())
    tts_dict["ObjectStates"] = dicts

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


def xls_file_to_library(excel_file) -> Library:
    # open Excel file
    sheets = xlrd.open_workbook(excel_file)
    return sheets_to_library(sheets)


def sheets_to_library(sheets: dict):
    tokens = TokenParser.parse(sheets["Tokens"])

    figurines = FigurineParser.parse(sheets["Figurines"])

    dice = DiceParser.parse(sheets["Dice"])

    complex_types = ComplexTypeParser.parse(sheets["ComplexTypes"], sheets["Shapes"])

    complex_parser = ComplexObjectParser(complex_types)
    complex_objects = complex_parser.parse(sheets["ComplexObjects"])

    decks = DeckParser.parse(sheets["Decks"], complex_objects)

    bag_parser = BagParser(types=tokens + figurines + dice + complex_objects + decks)
    bags = bag_parser.parse(sheets["Containers"])

    # creator = EntityCreator(tokens + dice + complex_objects + decks + bags)
    # entities = creator.createEntities(sheets["Placement"])  # todo, unused? May be important

    return Library(tokens, dice, complex_objects, decks, bags)
