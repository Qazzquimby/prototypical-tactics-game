import asyncio
import json
from pathlib import Path

import yaml.scanner

import yaml_parsing

from image_builders import ImageBuilder
from src.library import game_to_library
from tts_dir import try_and_find_save_games_folder
from src.tts_objects import library_to_tts_dict


def build(image_builder):
    save_schema()
    copy_yaml_to_site()

    save_dir = Path(try_and_find_save_games_folder())
    yaml_file_to_tts_save(
        yaml_path="data/input.yaml", save_dir=save_dir, image_builder=image_builder
    )


def save_schema():
    schema = yaml_parsing.Game.schema_json()
    with open("data/game_schema.json", "w") as f:
        f.write(schema)


def copy_yaml_to_site():
    with open("data/input.yaml", "r") as f:
        input_yaml = f.read()
    with open("tactics-site/public/input.yaml", "w+") as f:
        f.write(input_yaml)


def yaml_file_to_tts_save(yaml_path: str, save_dir: Path, image_builder: ImageBuilder):
    game = load_game_from_yaml_path(yaml_path)
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


def load_game_from_yaml_path(yaml_path: str):
    try:
        yaml_content = yaml_parsing.read_yaml_file(yaml_path)
    except yaml.scanner.ScannerError as e:
        print(f"Error parsing {yaml_path}\n{e}")
        return

    game = yaml_parsing.Game.parse_obj(yaml_content)
    return game


def save_tts(tts_json: dict, save_dir: Path, file_name: str):
    path = save_dir / f"TS_{file_name.replace(' ', '_')}.json"
    with open(path, "w") as outfile:
        json.dump(tts_json, outfile)
