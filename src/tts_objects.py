import json

from playwright.async_api import async_playwright

from domain.library import Library
from src.drawing.drawing import draw_library_assets
from src.image_builders import ImageBuilder


def reposition_set_bag(tts_dict):
    # todo could combine with _make_game_set_bag
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


async def library_to_tts_dict(
    library: Library,
    image_builder: ImageBuilder,
    file_name,
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
    reposition_set_bag(tts_dict)

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
