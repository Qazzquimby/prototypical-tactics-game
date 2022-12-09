import time
from pathlib import Path

import pygame
import yaml.scanner
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent

from tts.fake_xls_books import FakeBook
from tts_dir import try_and_find_save_games_folder


import yaml_to_xls
from image_builders import ImagesDirImageBuilder
from core import sheets_to_tts_json, save_tts


def yaml_file_to_tts_save(yaml_path: str, save_dir: Path):
    data_dir = Path("data").absolute()
    file_stem = Path(yaml_path).stem

    try:
        yaml_content = yaml_to_xls.read_yaml_file(yaml_path)
    except yaml.scanner.ScannerError as e:
        print(f"Error parsing {yaml_path}")
        print(e)
        return
    print("Updated xls")

    sheets = yaml_to_xls.yaml_content_to_sheets(yaml_content)
    fake_book = FakeBook(sheets)

    tts_json = sheets_to_tts_json(
        sheets=fake_book.sheets,
        image_builder=ImagesDirImageBuilder(pygame, basePath=data_dir / "images"),
        file_name="TestGame",
    )

    save_tts(tts_json, save_dir=save_dir, file_name=file_stem)
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
