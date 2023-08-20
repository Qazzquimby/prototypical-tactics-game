import asyncio
import json
from pathlib import Path
from typing import Union, Coroutine

import yaml.scanner
from playwright.async_api import Playwright, async_playwright

from pygame import Surface

import yaml_parsing
from browser import create_browser, close_browser
from domain.bag import Bag

from domain.library import Library
from domain.token import ContentToken
from drawer.base import BaseDrawer
from drawer.cardBackDrawer import CardBackDrawer
from drawer.complexObjectDrawer import ComplexObjectDrawer
from drawer.loneCardDrawer import LoneCardDrawer
from image_builders import ImageBuilder
from tts_dir import try_and_find_save_games_folder
from yaml_parsing import GameSet, RulesDeck


def build(image_builder):
    _save_schema()
    _copy_yaml_to_site()

    save_dir = Path(try_and_find_save_games_folder())
    yaml_file_to_tts_save(
        yaml_path="data/input.yaml", save_dir=save_dir, image_builder=image_builder
    )


def yaml_file_to_tts_save(yaml_path: str, save_dir: Path, image_builder: ImageBuilder):
    game = _load_game_from_yaml_path(yaml_path)
    library = game_to_library(game)

    tts_dict = asyncio.run(
        library_to_tts_dict(
            library=library,
            image_builder=image_builder,
            file_name="TestGame",
        ),
    )

    save_tts(tts_dict, save_dir=save_dir, file_name=Path(yaml_path).stem)
    print("Built images")


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
        game_set_bag = _make_game_set_bag(game_set)
        sets_bag.contained_objects.append(game_set_bag)
    library.bags.append(sets_bag)

    rules_deck = RulesDeck(cards=game.rules)
    domain_rules_deck = rules_deck.get_tts_obj(set_name="core")
    library.bags[0].contained_objects.append(domain_rules_deck)

    return library


async def library_to_tts_dict(
    library: Library,
    image_builder: ImageBuilder,
    file_name,
    config=None,
):
    await image_builder.initialize()
    _setup_pygame()

    tts_dict = _read_template_dict(file_name)

    async with async_playwright() as playwright:
        await draw_library_assets(
            playwright=playwright,
            library=library,
            config=config,
            image_builder=image_builder,
        )

    entities = library.bags
    tts_dict["ObjectStates"] += [entity.as_dict() for entity in entities]
    _reposition_set_bag(tts_dict)

    return tts_dict


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
            card_drawer = ComplexObjectDrawer(card.object, config)
            names = [deck.set_name, deck.name, card.object.content.name]
            image_name = _make_image_name(names)
            coroutines.append(
                _save_image_and_set_attribute(
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
            _save_image_and_set_attribute(
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
                _save_image_and_set_attribute(
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


def save_tts(tts_json: dict, save_dir: Path, file_name: str):
    path = save_dir / f"TS_{file_name.replace(' ', '_')}.json"
    with open(path, "w") as outfile:
        json.dump(tts_json, outfile)


def _save_schema():
    schema = yaml_parsing.Game.schema_json()
    with open("data/game_schema.json", "w") as f:
        f.write(schema)


def _copy_yaml_to_site():
    with open("data/input.yaml", "r") as f:
        input_yaml = f.read()
    with open("tactics-site/public/input.yaml", "w+") as f:
        f.write(input_yaml)


def _load_game_from_yaml_path(yaml_path: str):
    try:
        yaml_content = yaml_parsing.read_yaml_file(yaml_path)
    except yaml.scanner.ScannerError as e:
        print(f"Error parsing {yaml_path}\n{e}")
        return

    game = yaml_parsing.Game.parse_obj(yaml_content)
    return game


def _read_template_dict(file_name: str):
    # open save template
    with open("data/template.json", "r") as infile:
        data = json.load(infile)
        data["SaveName"] = file_name
    return data


def _make_image_name(names):
    return "__".join(names)


async def _save_image_and_set_attribute(
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


def _setup_pygame():
    # setup pygame as drawing library
    import pygame

    pygame.init()


def _make_game_set_bag(game_set: GameSet):
    set_bag = Bag(
        name=game_set.name,
        description=game_set.description,
        size=2,
        color=(0.0, 0.0, 0.0),
    )

    rules_deck = RulesDeck(cards=game_set.rules)
    domain_rules_deck = rules_deck.get_tts_obj(set_name=game_set.name)
    if domain_rules_deck:
        set_bag.contained_objects.append(domain_rules_deck)

    # heroes
    hero_bag = Bag(
        name=f"{game_set.name} heroes",
        size=2,
        color=(0.0, 0.0, 1.0),
    )
    for hero_box in game_set.heroes:
        hero_box_bag = hero_box.get_tts_obj(set_name=game_set.name)
        hero_bag.contained_objects.append(hero_box_bag)
    set_bag.contained_objects.append(hero_bag)

    # maps
    map_bag = Bag(
        name=f"{game_set.name} maps",
        size=2,
        color=(0.0, 1.0, 0.0),
    )
    for map_ in game_set.maps:
        map_bag.contained_objects.append(map_.get_tts_obj())
    set_bag.contained_objects.append(map_bag)

    return set_bag


def _reposition_set_bag(tts_dict):
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
