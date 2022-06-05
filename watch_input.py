import time
from pathlib import Path

import pygame
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent

import yaml_to_xls
from image_builders import ImagesDirImageBuilder
from core import build_file


def run(yaml_path: str):
    data_dir = "data"
    file_stem = Path(yaml_path).stem
    xls_path = f"{data_dir}/{file_stem}.xls"

    yaml_to_xls.file_to_xls(src=yaml_path, dest=xls_path)
    print("Updated xls")

    build_file(
        excel_file=xls_path,
        image_builder=ImagesDirImageBuilder(pygame, basePath=f"{data_dir}/images"),
        save_dir=data_dir,
        file_name=file_stem,
    )
    print("Built images")


class OnChangeUpdateTTSHandler(FileSystemEventHandler):
    def on_any_event(self, event: FileSystemEvent):
        if event.src_path.endswith(".yaml"):
            run(event.src_path)


if __name__ == "__main__":
    run("data/input.yaml")

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
