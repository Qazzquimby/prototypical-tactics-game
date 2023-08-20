from pathlib import Path

import pygame

from src.image_builders import DirectoryImagesBuilder
from src.orchestration import build
from src.paths import site_images_dir


def build_local():
    image_builder = DirectoryImagesBuilder(
        pygame=pygame, base_path=Path(site_images_dir)
    )
    build(image_builder)


if __name__ == "__main__":
    build_local()
