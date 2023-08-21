import pygame

from src.image_builders import OnlineImagesBuilder
from src.orchestration import build


def build_online():
    image_builder = OnlineImagesBuilder(
        pygame=pygame, base_path="tactics-site/public/images"
    )
    build(image_builder)


if __name__ == "__main__":
    build_online()
