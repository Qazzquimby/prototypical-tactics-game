from pathlib import Path

import pygame

from src.global_settings import global_config
from src.image_builders import OnlineImagesBuilder
from src.orchestration import build

global_config["production"] = True


def build_online():
    # read yaml
    # get image urls that aren't yet on netlify
    # download, process, rename, save new images to tactics-site/public
    # Bump version number, type "images"
    # git add, commit, push
    # exponential dropoff wait for new version number to be live on site (wait for netlify build)
    # generate cards from new images
    # change version type to cards
    # git add, commit, push

    image_builder = OnlineImagesBuilder(
        pygame=pygame, base_path=Path("tactics-site/public/")
    )
    build(image_builder)


if __name__ == "__main__":
    build_online()
