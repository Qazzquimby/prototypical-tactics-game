from pathlib import Path
import pygame
from tts_dir import try_and_find_save_games_folder
from image_builders import ImagesDirImageBuilder
from core import xls_file_to_tts_save


async def run(xls_path: Path, save_dir: Path):
    data_dir = Path("data").absolute()

    await xls_file_to_tts_save(
        xls_file_path=str(xls_path),
        image_builder=ImagesDirImageBuilder(pygame, base_path=data_dir / "images"),
        save_dir=save_dir,
        file_name=xls_path.stem,
    )
    print("Built images")


if __name__ == "__main__":
    save_dir = Path(try_and_find_save_games_folder())
    xls_path = Path("data/input_newformat.xls")

    await run(xls_path, save_dir=save_dir)
