from pathlib import Path

import pygame

from tests.integration_test import site_images_dir

from image_builders import DirectoryImagesBuilder
from core import build


def build_local():
    image_builder = DirectoryImagesBuilder(
        pygame=pygame, base_path=Path(site_images_dir)
    )
    build(image_builder)


if __name__ == "__main__":
    build_local()
