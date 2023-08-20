import asyncio
from typing import Union, Coroutine

from playwright.async_api import Playwright
from pygame import Surface

from domain.library import Library
from domain.token import ContentToken
from drawer.base import BaseDrawer
from src.drawing.card_drawer import CardDrawer
from drawer.cardBackDrawer import CardBackDrawer
from drawer.lone_card_drawer import LoneCardDrawer
from src.browser import create_browser, close_browser
from src.image_builders import ImageBuilder


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
            card_drawer = CardDrawer(card.object, config)
            names = [deck.set_name, deck.name, card.object.content.name]
            image_name = make_image_name(names)
            coroutines.append(
                save_image_and_set_attribute(
                    image_builder=image_builder,
                    drawer=card_drawer,
                    object_=card,
                    file_name=image_name,
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
    file_extension: str = "jpg",
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
