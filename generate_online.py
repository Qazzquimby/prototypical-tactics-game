from pathlib import Path

import pygame

from src.global_settings import global_config
from src.image_builders import OnlineImagesBuilder
from src.orchestration import build

global_config["production"] = True


def build_online():
    image_builder = OnlineImagesBuilder(
        pygame=pygame, base_path=Path("tactics-site/public/")
    )
    build(image_builder)


if __name__ == "__main__":
    build_online()
