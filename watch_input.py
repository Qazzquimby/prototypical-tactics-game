import asyncio
import time
from pathlib import Path

import pygame
import yaml.scanner
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent

from tts_dir import try_and_find_save_games_folder


import yaml_parsing
from image_builders import ImgBoxImagesBuilder
from core import save_tts, game_to_library, library_to_tts_dict


def yaml_file_to_tts_save(yaml_path: str, save_dir: Path):
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
            image_builder=ImgBoxImagesBuilder(pygame=pygame, project_name="tactics"),
            file_name="TestGame",
        ),
        debug=True,
    )
    save_tts(tts_dict, save_dir=save_dir, file_name=file_stem)
    print("Built images")


class OnChangeUpdateTTSHandler(FileSystemEventHandler):
    def on_any_event(self, event: FileSystemEvent):
        if event.src_path.endswith(".yaml"):
            yaml_file_to_tts_save(event.src_path, save_dir=save_dir)


if __name__ == "__main__":
    save_dir = Path(try_and_find_save_games_folder())

    yaml_file_to_tts_save("data/input.yaml", save_dir=save_dir)

    path = "data"
    event_handler = OnChangeUpdateTTSHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)

    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
