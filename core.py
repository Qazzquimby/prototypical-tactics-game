import json

import xlrd

from creator.entityCreator import EntityCreator
from domain.library import Library
from domain.token import ContentToken
from drawer.cardBackDrawer import CardBackDrawer
from drawer.complexObjectDrawer import ComplexObjectDrawer
from drawer.deckDrawer import DeckDrawer
from drawer.diceDrawer import DiceDrawer
from drawer.tokenDrawer import TokenDrawer
from sheetParser.bagParser import BagParser
from sheetParser.complexObjectParser import ComplexObjectParser
from sheetParser.complexTypeParser import ComplexTypeParser
from sheetParser.deckParser import DeckParser
from sheetParser.diceParser import DiceParser
from sheetParser.figurineParser import FigurineParser
from sheetParser.tokenParser import TokenParser


def xls_file_to_tts_save(
    xls_file_path, image_builder, save_dir, file_name, config=None
):
    sheets = xlrd.open_workbook(xls_file_path)

    tts_json = sheets_to_tts_json(sheets, image_builder, file_name, config)

    save_tts(tts_json=tts_json, save_dir=save_dir, file_name=file_name)


def sheets_to_tts_json(sheets: dict, image_builder, file_name, config=None):
    library = sheets_to_library(sheets)
    return library_to_tts_json(
        library, image_builder, file_name, sheets["Placement"], config
    )


def library_to_tts_json(
    library: Library, image_builder, file_name, placement, config=None
):
    setup_pygame()

    tts_dict = read_template_dict(file_name)

    drawer = DeckDrawer(config)
    for deck in library.decks:
        path = image_builder.build(drawer.draw(deck), deck.name, "jpg")
        deck.setImagePath(path)

    drawer = CardBackDrawer(config)
    for deck in library.decks:
        path = image_builder.build(drawer.draw(deck), deck.name + "_back", "jpg")
        deck.setBackImagePath(path)

    done = 0
    for obj in library.complexObjects:
        if obj.type.type == "board":
            drawer = ComplexObjectDrawer(obj, config)
            path = image_builder.build(drawer.draw(), obj.name, "jpg")
            obj.setImagePath(path)
            done += 1

    done = 0
    for token in library.tokens:
        if isinstance(token, ContentToken):
            drawer = TokenDrawer(token)
            path = image_builder.build(drawer.draw(), "token_" + token.name, "jpg")
            token.setImagePath(path)
            done += 1

    # draw all dice
    done = 0
    for die in library.dice:
        if die.customContent:
            drawer = DiceDrawer(die)
            path = image_builder.build(drawer.draw(), "die" + die.name, "png")
            die.setImagePath(path)
            done += 1

    # UGLY - we already did this step during parsing, but we need to create entities AFTER drawing or their image paths aren't set
    creator = EntityCreator(library.all())
    entities = creator.createEntities(placement)

    dicts = []
    for entity in entities:
        dicts.append(entity.as_dict())
    tts_dict["ObjectStates"] = dicts

    return tts_dict


def save_tts(tts_json, save_dir, file_name):
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

    creator = EntityCreator(tokens + dice + complex_objects + decks + bags)
    entities = creator.createEntities(sheets["Placement"])  # todo, unused?

    return Library(tokens, dice, complex_objects, decks, bags)
