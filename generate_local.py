import asyncio
import time
from pathlib import Path

import pygame
import yaml.scanner

from tests.integration_test import data_dir, site_images_dir
from tts_dir import try_and_find_save_games_folder


import yaml_parsing
from image_builders import DirectoryImagesBuilder
from core import save_tts, game_to_library, library_to_tts_dict


def yaml_file_to_tts_save(yaml_path: str, save_dir: Path, image_builder=None):
    if image_builder is None:
        image_builder = DirectoryImagesBuilder(
            pygame=pygame, base_path=data_dir / "images"
        )

    file_stem = Path(yaml_path).stem

    try:
        yaml_content = yaml_parsing.read_yaml_file(yaml_path)
    except yaml.scanner.ScannerError as e:
        print(f"Error parsing {yaml_path}\n{e}")
        return

    game = yaml_parsing.Game.parse_obj(yaml_content)
    library = game_to_library(game)
    tts_dict = asyncio.run(
        library_to_tts_dict(
            library=library,
            image_builder=image_builder,
            file_name="TestGame",
        ),
    )
    save_tts(tts_dict, save_dir=save_dir, file_name=file_stem)
    print("Built images")


def build_local():
    image_builder = DirectoryImagesBuilder(
        pygame=pygame, base_path=Path(site_images_dir)
    )
    build(image_builder)


def build(image_builder):
    schema = yaml_parsing.Game.schema_json()
    with open("data/game_schema.json", "w") as f:
        f.write(schema)

    # copy 'data/input.yaml' to 'tactics-site/public/input.yaml'
    with open("data/input.yaml", "r") as f:
        input_yaml = f.read()
    with open("tactics-site/public/input.yaml", "w+") as f:
        f.write(input_yaml)

    save_dir = Path(try_and_find_save_games_folder())
    yaml_file_to_tts_save(
        "data/input.yaml", save_dir=save_dir, image_builder=image_builder
    )


if __name__ == "__main__":
    build_local()
