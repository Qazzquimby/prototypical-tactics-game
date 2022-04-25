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
    excelFile, imageBuilder, saveDir, fileName, progressCallback, config=None
):
    # setup pygame as drawing library
    import pygame

    pygame.init()

    # open save template
    with open("data/template.json", "r") as infile:
        data = json.load(infile)
        data["SaveName"] = fileName

    # parse here
    library = parse_file(excelFile, progressCallback)

    progressCallback("Drawing all custom content.")

    # draw all the card decks
    progressCallback("Drawing decks... ", False)
    drawer = DeckDrawer(config)
    for deck in library.decks:
        path = imageBuilder.build(drawer.draw(deck), deck.name, "jpg")
        deck.setImagePath(path)

    # draw all the deck backs
    drawer = CardBackDrawer(config)
    for deck in library.decks:
        path = imageBuilder.build(drawer.draw(deck), deck.name + "_back", "jpg")
        deck.setBackImagePath(path)
    progressCallback(str(len(library.decks)) + " decks succesfully drawn.")

    # draw all the boards
    progressCallback("Drawing boards... ", False)
    done = 0
    for obj in library.complexObjects:
        if obj.type.type == "board":
            drawer = ComplexObjectDrawer(obj, config)
            path = imageBuilder.build(drawer.draw(), obj.name, "jpg")
            obj.setImagePath(path)
            done += 1
    progressCallback(str(done) + " boards succesfully drawn.")

    # draw all the (custom) tokens
    progressCallback("Drawing tokens... ", False)
    done = 0
    for token in library.tokens:
        if isinstance(token, ContentToken):
            drawer = TokenDrawer(token)
            path = imageBuilder.build(drawer.draw(), "token_" + token.name, "jpg")
            token.setImagePath(path)
            done += 1
    progressCallback(str(done) + " custom tokens succesfully drawn.")

    # draw all dice
    progressCallback("Drawing dice... ", False)
    done = 0
    for die in library.dice:
        if die.customContent:
            drawer = DiceDrawer(die)
            path = imageBuilder.build(drawer.draw(), "die" + die.name, "png")
            die.setImagePath(path)
            done += 1
    progressCallback(str(done) + " dice succesfully drawn.")

    # UGLY - we already did this step during parsing but we need to create entities AFTER drawing or their image paths aren't set
    creator = EntityCreator(library.all())
    workbook = xlrd.open_workbook(excelFile)
    entities = creator.createEntities(workbook.sheet_by_name("Placement"))

    dicts = []
    for entity in entities:
        dicts.append(entity.as_dict())

    progressCallback("Placing all entities on the tabletop.")
    # add entities to save file
    data["ObjectStates"] = dicts
    progressCallback("All entities have been placed.")

    # save file
    path = saveDir + "\TS_" + fileName.replace(" ", "_") + ".json"
    progressCallback("Saving file to " + path)
    with open(path, "w") as outfile:
        json.dump(data, outfile)


def parse_file(excelFile, progressCallback):
    # open excel file
    progressCallback("Reading spreadsheet: " + excelFile)
    workbook = xlrd.open_workbook(excelFile)

    # collect entity libraries
    progressCallback("Reading tokens... ", False)
    tokens = TokenParser.parse(workbook.sheet_by_name("Tokens"))
    progressCallback(str(len(tokens)) + " tokens succesfully extracted.")

    progressCallback("Reading dice... ", False)
    dice = DiceParser.parse(workbook.sheet_by_name("Dice"))
    progressCallback(str(len(dice)) + " dice succesfully extracted.")

    progressCallback("Reading complex types... ", False)
    complexTypes = ComplexTypeParser.parse(
        workbook.sheet_by_name("ComplexTypes"), workbook.sheet_by_name("Shapes")
    )
    progressCallback(str(len(complexTypes)) + " types succesfully extracted.")

    progressCallback("Reading complex objects... ", False)
    complexParser = ComplexObjectParser(complexTypes)
    complexObjects = complexParser.parse(workbook.sheet_by_name("ComplexObjects"))
    progressCallback(
        str(len(complexObjects)) + " complex objects succesfully extracted."
    )

    progressCallback("Reading decks... ", False)
    decks = DeckParser.parse(workbook.sheet_by_name("Decks"), complexObjects)
    progressCallback(str(len(decks)) + " decks succesfully extracted.")

    progressCallback("Reading bags... ", False)
    bagParser = BagParser(tokens + dice + complexObjects + decks)
    bags = bagParser.parse(workbook.sheet_by_name("Containers"))
    progressCallback(str(len(bags)) + " bags succesfully extracted.")

    # UGLY - we have to redo this step later because we set the image paths after drawing and these entities won't work
    progressCallback("Reading table content... ", False)
    creator = EntityCreator(tokens + dice + complexObjects + decks + bags)
    entities = creator.createEntities(workbook.sheet_by_name("Placement"))
    progressCallback("Read " + str(len(entities)) + " items to be placed.", True)

    return Library(tokens, dice, complexObjects, decks, bags)
