import pygame

from generate_local import build_local
from src.image_builders import DirectoryImagesBuilder
from src.orchestration import build


def build_online():
    image_builder = DirectoryImagesBuilder(
        pygame=pygame, base_path="tactics-site/public/images"
    )
    build(image_builder)


if __name__ == "__main__":
    build_local()
