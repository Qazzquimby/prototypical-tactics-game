import time
from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent

import yaml_to_xls
from prototypical import build_file, parse_file, App


def run(yaml_path: str):
    xls_path = f"data/{Path(yaml_path).stem}_cards.xls"
    yaml_to_xls.file_to_xls(src=yaml_path, dest=xls_path)
    print("Updated xls")

    library = parse_file(excelFile=xls_path, progressCallback=lambda x, y=None: None)
    print(library)

    build_file(
        excelFile=xls_path,
        imageBuilder=None,
        saveDir="data",
        fileName=Path(yaml_path).stem,
        progressCallback=None,
        config=None,
    )


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
