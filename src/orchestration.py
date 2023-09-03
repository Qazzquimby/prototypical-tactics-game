import asyncio
import json
import random
from pathlib import Path

import yaml.scanner

from schema import yaml_parsing
from schema.yaml_parsing import Game
from src.global_settings import global_config

from src.image_builders import ImageBuilder
from src.library import game_to_library
from src.paths import data_dir, site_public_dir
from src.tts_dir import try_and_find_save_games_folder
from src.tts_objects import library_to_tts_dict


def build(image_builder):
    save_schema()
    copy_yaml_to_site()

    save_dir = Path(try_and_find_save_games_folder())
    yaml_file_to_tts_save(
        yaml_path=str(data_dir / "input.yaml"),
        save_dir=save_dir,
        image_builder=image_builder,
    )


def save_schema():
    schema = yaml_parsing.Game.schema_json()
    with open(data_dir / "game_schema.json", "w") as f:
        f.write(schema)


def copy_yaml_to_site():
    with open(data_dir / "input.yaml", "r") as f:
        input_yaml = f.read()
    with open(site_public_dir / "input.yaml", "w+") as f:
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
            if hero.polish:
                heroes_needing_playtest.append(hero)
            else:
                other_heroes.append(hero)

    min_heroes = 12
    # want 50% heroes needing playtest, 50% other heroes.
    num_other_heroes = min(min_heroes, len(other_heroes))
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

    if global_config["prune_for_playtest"]:
        prune_for_playtest(game)
    library = game_to_library(game)

    # all_text_fields = get_all_text_fields(game)

    tts_dict = asyncio.run(
        library_to_tts_dict(
            library=library,
            image_builder=image_builder,
            file_name="Crossover Tactics",
        ),
    )

    save_tts(tts_dict, save_dir=save_dir, file_name=Path(yaml_path).stem)
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
    path = save_dir / f"Crossover_Tactics.json"
    with open(path, "w") as outfile:
        json.dump(tts_json, outfile)
