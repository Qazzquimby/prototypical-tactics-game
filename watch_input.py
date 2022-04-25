import time
from pathlib import Path

import pydantic
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent

import yaml_to_xls


class OnChangeUpdateTTSHandler(FileSystemEventHandler):
    def on_any_event(self, event: FileSystemEvent):
        if event.src_path.endswith('.yaml'):
            dest = f"data/{Path(event.src_path).stem}_cards.xls"
            yaml_to_xls.file_to_xls(src=event.src_path, dest=dest)
            print("Updated xls")




if __name__ == "__main__":
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
