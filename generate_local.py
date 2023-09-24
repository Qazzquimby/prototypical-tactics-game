from pathlib import Path

import pygame

from src.global_settings import global_config
from src.image_builders import DirectoryImagesBuilder
from src.orchestration import build
from src.paths import SITE_PUBLIC_DIR

global_config["prune_for_playtest"] = True


def build_local():
    image_builder = DirectoryImagesBuilder(
        pygame=pygame, base_path=Path(SITE_PUBLIC_DIR)
    )
    build(image_builder)


if __name__ == "__main__":

    build_local()
