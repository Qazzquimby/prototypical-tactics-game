from pathlib import Path
from tts_dir import try_and_find_save_games_folder
from watch_input import yaml_file_to_tts_save


async def run(save_dir: Path):
    await yaml_file_to_tts_save(
        yaml_path="data/input.yaml",
        save_dir=save_dir,
    )
    print("Built images")


if __name__ == "__main__":
    save_dir = Path(try_and_find_save_games_folder())
    xls_path = Path("data/input_newformat.xls")

    await run(save_dir=save_dir)
