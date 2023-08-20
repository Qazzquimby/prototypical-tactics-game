import asyncio
import json
from typing import Union, Coroutine

from playwright.async_api import async_playwright, Playwright
from pygame import Surface

from src.browser import create_browser, close_browser
from domain.library import Library
from domain.token import ContentToken
from drawer.base import BaseDrawer
from drawer.cardBackDrawer import CardBackDrawer
from drawer.browser_drawer import BrowserDrawer
from drawer.lone_card_drawer import LoneCardDrawer
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


async def draw_library_assets(
    playwright: Playwright, library: Library, config, image_builder: ImageBuilder
):
    await create_browser(playwright)

    coroutines = []

    back_drawer = CardBackDrawer(config)

    deck_names = [deck.name for deck in library.decks]
    assert len(deck_names) == len(set(deck_names)), "Deck names must be unique"

    for deck in library.decks:
        for i, card in enumerate(deck.cards):
            card_drawer = BrowserDrawer(card.object, config)
            names = [deck.set_name, deck.name, card.object.content.name]
            image_name = make_image_name(names)
            coroutines.append(
                save_image_and_set_attribute(
                    image_builder=image_builder,
                    drawer=card_drawer,
                    object_=card,
                    file_name=image_name,
                    file_extension="jpg",
                    attribute_to_set=["image_path"],
                )
            )

    for lone_card in library.lone_cards:
        coroutines.append(
            save_image_and_set_attribute(
                image_builder=image_builder,
                drawer=LoneCardDrawer(config),
                object_=lone_card,
                file_name=lone_card.object.name,
                file_extension="jpg",
            )
        )

    for token in library.tokens:
        if isinstance(token, ContentToken):
            coroutines.append(
                save_image_and_set_attribute(
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


def make_image_name(names):
    return "__".join(names)


async def save_image_and_set_attribute(
    image_builder: ImageBuilder,
    drawer: BaseDrawer,
    object_,
    file_name: str,
    file_extension: str,
    attribute_to_set: str | list[str] = None,
):
    if attribute_to_set is None:
        attribute_to_set = ["image_path", "back_image_path"]

    image: Union[Surface, Coroutine[Surface]] = drawer.draw(object_)
    # if image is promise, resolve
    if isinstance(image, Coroutine):
        image = await image
    path = await image_builder.build(
        image=image, file_name=file_name, file_extension=file_extension
    )
    if isinstance(attribute_to_set, str):
        attribute_to_set = [attribute_to_set]

    for attribute in attribute_to_set:
        object_.__setattr__(attribute, path)
