import asyncio
import json
import math
import random
from pathlib import Path

import yaml.scanner

from src import yaml_parsing
from src.drawing.self_host_tokens import (
    filter_unsaved_image_urls,
    host_external_images,
    bump_version,
    update_git,
)
from src.global_settings import global_config

from src.image_builders import ImageBuilder
from src.library import game_to_library
from src.paths import DATA_DIR, SITE_PUBLIC_DIR
from src.tts_dir import try_and_find_save_games_folder
from src.tts_objects import library_to_tts_dict
from src.yaml_parsing import Game


def build(image_builder):
    save_schema()
    copy_yaml_to_site()

    save_dir = Path(try_and_find_save_games_folder())
    yaml_file_to_tts_save(
        yaml_path=str(DATA_DIR / "input.yaml"),
        save_dir=save_dir,
        image_builder=image_builder,
    )


def build_production(image_builder):
    save_schema()
    copy_yaml_to_site()

    save_dir = Path(try_and_find_save_games_folder())
    yaml_file_to_tts_save(
        yaml_path=str(DATA_DIR / "input.yaml"),
        save_dir=save_dir,
        image_builder=image_builder,
    )


def save_schema():
    schema = Game.schema_json()
    with open(DATA_DIR / "game_schema.json", "w") as f:
        f.write(schema)


def copy_yaml_to_site():
    with open(DATA_DIR / "input.yaml", "r") as f:
        input_yaml = f.read()
    with open(SITE_PUBLIC_DIR / "input.yaml", "w+") as f:
        f.write(input_yaml)


def get_all_text_fields(game):
    # used to stylecheck
    heroes = []
    for set_ in game.sets:
        heroes += set_.heroes

    abilities = []
    for hero in heroes:
        abilities += hero.passives
        abilities += hero.default_abilities
        abilities += hero.abilities

    texts = [ability.text for ability in abilities]

    return texts


def prune_for_playtest(game: Game):
    heroes_needing_playtest = []
    other_heroes = []
    for game_set in game.sets:
        for hero in game_set.heroes:
            if "needs_testing" in hero.polish:
                heroes_needing_playtest.append(hero)
            else:
                other_heroes.append(hero)

    desired_healthy_per_needing = 0.7

    min_heroes = 12
    # want 50% heroes needing playtest, 50% other heroes.
    min_other_heroes = min_heroes - len(heroes_needing_playtest)
    max_other_heroes = len(other_heroes)
    desired_other_heroes = math.ceil(
        len(heroes_needing_playtest) * desired_healthy_per_needing
    )
    num_other_heroes = min(
        max_other_heroes, max(min_other_heroes, desired_other_heroes)
    )
    random_other_heroes = random.sample(other_heroes, num_other_heroes)

    hero_pool = heroes_needing_playtest + random_other_heroes

    print("Pruning to heroes:")
    for hero in heroes_needing_playtest:
        print("! " + hero.name)
    for hero in random_other_heroes:
        print(hero.name)

    for game_set in game.sets:
        game_set.heroes = [hero for hero in game_set.heroes if hero in hero_pool]


def yaml_file_to_tts_save(yaml_path: str, save_dir: Path, image_builder: ImageBuilder):
    game = load_game_from_yaml_path(yaml_path)

    if global_config["production"]:
        host_external_images(game, wait=True)

    if global_config["prune_for_playtest"]:
        prune_for_playtest(game)
    library = game_to_library(game)

    tts_dict = asyncio.run(
        library_to_tts_dict(
            library=library,
            image_builder=image_builder,
            file_name="Tabletop Teamfight",
        ),
    )

    save_tts(tts_dict, save_dir=save_dir, file_name=Path(yaml_path).stem)

    # bump_version(mode="cards")
    # update_git()

    print("Built images")


def load_game_from_yaml_path(yaml_path: str):
    try:
        yaml_content = yaml_parsing.read_yaml_file(yaml_path)
    except yaml.scanner.ScannerError as e:
        print(f"Error parsing {yaml_path}\n{e}")
        return

    game = yaml_parsing.Game.parse_obj(yaml_content)
    return game


def save_tts(tts_json: dict, save_dir: Path, file_name: str):
    path = save_dir / f"TabletopTeamfight.json"
    with open(path, "w") as outfile:
        json.dump(tts_json, outfile)
