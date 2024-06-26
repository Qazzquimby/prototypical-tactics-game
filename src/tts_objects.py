import json

from playwright.async_api import async_playwright

from domain.library import Library
from src.drawing.drawing import draw_library_assets
from src.image_builders import ImageBuilder
from tts.guid import guid


def reposition_set_bag(tts_dict):
    # this is the old single bag
    sets_bag = [
        item for item in tts_dict["ObjectStates"] if item["Nickname"] == "Sets"
    ][0]
    sets_bag["Transform"] = {  # copied from save file to fit the table
        "posX": 74.78447,
        "posY": 1.154937,
        "posZ": 15.9169846,
        "rotX": 1.4840989e-05,
        "rotY": -1.382713e-05,
        "rotZ": 1.612498e-05,
        "scaleX": 3.0,
        "scaleY": 3.0,
        "scaleZ": 3.0,
    }


def reposition_set_bags(tts_dict):
    game_set_bags = [
        obj
        for obj in tts_dict["ObjectStates"]
        if obj["Name"] == "Bag" and obj["Nickname"] != "Randomizer"
    ]
    for i, bag in enumerate(game_set_bags):
        z_pos = 27 - i * 6

        bag["Transform"] = {
            "posX": 120,
            "posY": 2,
            "posZ": z_pos,
            "rotX": 0,
            "rotY": 0,
            "rotZ": 0,
            "scaleX": 1.0,
            "scaleY": 1.0,
            "scaleZ": 1.0,
        }

        # setup_button = {
        #     "GUID": guid(),
        #     "Name": "Button",
        #     "Transform": {
        #         "posX": 120,
        #         "posY": 10,
        #         "posZ": z_pos,
        #         "rotX": 0.0,
        #         "rotY": 0.0,
        #         "rotZ": 0.0,
        #         "scaleX": 1.0,
        #         "scaleY": 1.0,
        #         "scaleZ": 1.0,
        #     },
        #     "Nickname": f"Into Setup {bag['Nickname']}",
        #     #  print hello name
        #     "LuaScript": f"function onLoad()\n    print('Hello {bag['Nickname']}')\nend",
        # }
        # tts_dict["ObjectStates"].append(setup_button)


async def library_to_tts_dict(
    library: Library,
    image_builder: ImageBuilder,
    file_name: str,
    config=None,
):
    await image_builder.initialize()
    setup_pygame()

    tts_dict = read_template_dict(file_name)

    async with async_playwright() as playwright:
        await draw_library_assets(
            playwright=playwright,
            library=library,
            config=config,
            image_builder=image_builder,
        )

    entities = library.bags
    tts_dict["ObjectStates"] += [entity.as_dict() for entity in entities]
    # reposition_set_bag(tts_dict)
    reposition_set_bags(tts_dict)

    return tts_dict


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
