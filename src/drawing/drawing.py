import asyncio
from functools import cache
from pathlib import Path
from typing import Union, Coroutine

from playwright.async_api import Playwright
from pygame import Surface

from domain.card import Card
from domain.library import Library
from src.drawing.base import BaseDrawer
from src.drawing.card_drawer import CardDrawer
from src.browser import create_browser, close_browser
from src.image_builders import ImageBuilder


async def draw_library_assets(
    playwright: Playwright, library: Library, config, image_builder: ImageBuilder
):
    await create_browser(playwright)

    coroutines = []

    card_drawer = CardDrawer(config)

    deck_names = [deck.name for deck in library.decks]
    assert len(deck_names) == len(set(deck_names)), "Deck names must be unique"

    for deck in library.decks:
        for i, card in enumerate(deck.cards):
            names = [deck.set_name, deck.name, card.object.content.name]
            image_name = make_image_name(names)
            coroutines.append(
                save_image_and_set_attribute(
                    image_builder=image_builder,
                    drawer=card_drawer,
                    card=card,
                    file_name=image_name,
                    attribute_to_set=["image_path"],
                )
            )

    for lone_card in library.lone_cards:
        coroutines.append(
            save_image_and_set_attribute(
                image_builder=image_builder,
                drawer=card_drawer,
                card=lone_card,
                file_name=lone_card.object.name,
            )
        )

    batch_size = 10
    batches = [
        coroutines[i : i + batch_size] for i in range(0, len(coroutines), batch_size)
    ]
    for i, batch in enumerate(batches):
        await asyncio.gather(*batch)

    # await asyncio.gather(*coroutines)
    await close_browser()


def make_image_name(names):
    return "__".join(names)


async def save_image_and_set_attribute(
    image_builder: ImageBuilder,
    drawer: BaseDrawer,
    card: Card,
    file_name: str,
    file_extension: str = "jpg",
    attribute_to_set: str | list[str] = None,
):
    cache_file = Path(f"cache/{file_name}.json")
    if cache_file.exists():
        cache_content = cache_file.read_text()
        if cache_content == card.object.content.json():
            return

    if attribute_to_set is None:
        attribute_to_set = ["image_path", "back_image_path"]

    image: Union[Surface, Coroutine[Surface]] = drawer.draw(card)
    # if image is promise, resolve
    if isinstance(image, Coroutine):
        image = await image
    path = await image_builder.build(
        image=image, file_name=file_name, file_extension=file_extension
    )
    if isinstance(attribute_to_set, str):
        attribute_to_set = [attribute_to_set]

    for attribute in attribute_to_set:
        card.__setattr__(attribute, path)

    # create cache_file
    cache_file.parent.mkdir(exist_ok=True, parents=True)
    cache_file.touch()
    cache_file.write_text(card.object.content.json())
