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
from sheetParser.tokenParser import TokenParser


def build_file(
    excel_file, image_builder, save_dir, file_name, progress_callback=None, config=None
):
    if progress_callback is None:
        progress_callback = lambda x, y=None: None

    # setup pygame as drawing library
    import pygame

    pygame.init()

    # open save template
    with open("data/template.json", "r") as infile:
        data = json.load(infile)
        data["SaveName"] = file_name

    # parse here
    library = parse_file(excel_file, progress_callback)

    progress_callback("Drawing all custom content.")

    # draw all the card decks
    progress_callback("Drawing decks... ", False)
    drawer = DeckDrawer(config)
    for deck in library.decks:
        path = image_builder.build(drawer.draw(deck), deck.name, "jpg")
        deck.setImagePath(path)

    # draw all the deck backs
    drawer = CardBackDrawer(config)
    for deck in library.decks:
        path = image_builder.build(drawer.draw(deck), deck.name + "_back", "jpg")
        deck.setBackImagePath(path)
    progress_callback(str(len(library.decks)) + " decks successfully drawn.")

    # draw all the boards
    progress_callback("Drawing boards... ", False)
    done = 0
    for obj in library.complexObjects:
        if obj.type.type == "board":
            drawer = ComplexObjectDrawer(obj, config)
            path = image_builder.build(drawer.draw(), obj.name, "jpg")
            obj.setImagePath(path)
            done += 1
    progress_callback(str(done) + " boards successfully drawn.")

    # draw all the (custom) tokens
    progress_callback("Drawing tokens... ", False)
    done = 0
    for token in library.tokens:
        if isinstance(token, ContentToken):
            drawer = TokenDrawer(token)
            path = image_builder.build(drawer.draw(), "token_" + token.name, "jpg")
            token.setImagePath(path)
            done += 1
    progress_callback(str(done) + " custom tokens successfully drawn.")

    # draw all dice
    progress_callback("Drawing dice... ", False)
    done = 0
    for die in library.dice:
        if die.customContent:
            drawer = DiceDrawer(die)
            path = image_builder.build(drawer.draw(), "die" + die.name, "png")
            die.setImagePath(path)
            done += 1
    progress_callback(str(done) + " dice successfully drawn.")

    # UGLY - we already did this step during parsing, but we need to create entities AFTER drawing or their image paths aren't set
    creator = EntityCreator(library.all())
    workbook = xlrd.open_workbook(excel_file)
    entities = creator.createEntities(workbook.sheet_by_name("Placement"))

    dicts = []
    for entity in entities:
        dicts.append(entity.as_dict())

    progress_callback("Placing all entities on the tabletop.")
    # add entities to save file
    data["ObjectStates"] = dicts
    progress_callback("All entities have been placed.")

    # save file
    path = save_dir / f"TS_{file_name.replace(' ', '_')}.json"
    progress_callback(f"Saving file to {path}")
    with open(path, "w") as outfile:
        json.dump(data, outfile)


def parse_file(excel_file, progress_callback):
    # open Excel file
    progress_callback(f"Reading spreadsheet: {excel_file}")
    workbook = xlrd.open_workbook(excel_file)

    # collect entity libraries
    progress_callback("Reading tokens... ", False)
    tokens = TokenParser.parse(workbook.sheet_by_name("Tokens"))
    progress_callback(str(len(tokens)) + " tokens successfully extracted.")

    progress_callback("Reading dice... ", False)
    dice = DiceParser.parse(workbook.sheet_by_name("Dice"))
    progress_callback(str(len(dice)) + " dice successfully extracted.")

    progress_callback("Reading complex types... ", False)
    complex_types = ComplexTypeParser.parse(
        workbook.sheet_by_name("ComplexTypes"), workbook.sheet_by_name("Shapes")
    )
    progress_callback(str(len(complex_types)) + " types successfully extracted.")

    progress_callback("Reading complex objects... ", False)
    complex_parser = ComplexObjectParser(complex_types)
    complex_objects = complex_parser.parse(workbook.sheet_by_name("ComplexObjects"))
    progress_callback(
        str(len(complex_objects)) + " complex objects successfully extracted."
    )

    progress_callback("Reading decks... ", False)
    decks = DeckParser.parse(workbook.sheet_by_name("Decks"), complex_objects)
    progress_callback(str(len(decks)) + " decks successfully extracted.")

    progress_callback("Reading bags... ", False)
    bag_parser = BagParser(types=tokens + dice + complex_objects + decks)
    bags = bag_parser.parse(workbook.sheet_by_name("Containers"))
    progress_callback(str(len(bags)) + " bags successfully extracted.")

    # UGLY - we have to redo this step later because we set the image paths after drawing and these entities won't work
    progress_callback("Reading table content... ", False)
    creator = EntityCreator(tokens + dice + complex_objects + decks + bags)
    entities = creator.createEntities(workbook.sheet_by_name("Placement"))
    progress_callback("Read " + str(len(entities)) + " items to be placed.", True)

    return Library(tokens, dice, complex_objects, decks, bags)
