import time
from pathlib import Path

import pygame
import yaml.scanner
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from tts_dir import try_and_find_save_games_folder


import yaml_to_xls
from image_builders import ImagesDirImageBuilder
from core import build_file

def run(yaml_path: str, save_dir: Path):
    data_dir = Path("data").absolute()
    file_stem = Path(yaml_path).stem
    xls_path =  data_dir / f"{file_stem}.xls"

    try:
        yaml_to_xls.file_to_xls(src=yaml_path, dest=xls_path)
    except yaml.scanner.ScannerError as e:
        print(f"Error parsing {yaml_path}")
        print(e)
        return
    print("Updated xls")

    build_file(
        excel_file=xls_path,
        image_builder=ImagesDirImageBuilder(pygame, basePath=data_dir/ "images"),
        save_dir=save_dir,
        file_name=file_stem,
    )
    print("Built images")


class OnChangeUpdateTTSHandler(FileSystemEventHandler):
    def on_any_event(self, event: FileSystemEvent):
        if event.src_path.endswith(".yaml"):
            run(event.src_path, save_dir=save_dir)


if __name__ == "__main__":
    save_dir = Path(try_and_find_save_games_folder())

    run("data/input.yaml", save_dir=save_dir)

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
