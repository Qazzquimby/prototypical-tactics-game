from pathlib import Path

import requests

from schema import yaml_parsing
from src.paths import data_dir, site_public_dir

# iterate through entire nested dict. When find an "image_url" key
# save the image to site_tokens_dir / name.jpg
# then update the dict with the new path

IMAGE_URL_KEY = "image_url"

url_replacements = {}


def localize_image_urls(data: dict):
    old_data = data.copy()
    keys = list(data.keys())
    for key in keys:
        value = data[key]
        if isinstance(value, dict):
            data[key] = localize_image_urls(data[key])
        if isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, dict):
                    data[key][i] = localize_image_urls(item)
        elif key == IMAGE_URL_KEY:
            save_image(value, data)
    return data


def save_image(url: str, data: dict):
    if "http" in url or "tactics.toren.dev" in url:
        return  # already saved.

    name = f"image_token_{data['name']}_{str(hash(url))}"
    print(f"Saving {name}")
    # if not exists
    dest_path = site_public_dir / f"{name}.jpg"
    if not dest_path.exists():
        with open(dest_path, "wb+") as f:
            f.write(requests.get(url).content)
    url_replacements[url] = dest_path.relative_to(site_public_dir).as_posix()


def main():
    yaml_path = data_dir / "input.yaml"
    yaml_content = yaml_parsing.read_yaml_file(yaml_path)

    result = localize_image_urls(yaml_content)

    with open(yaml_path, "r", encoding="utf8") as yaml_file:
        yaml_string = yaml_file.read()

    for url, replacement in url_replacements.items():
        yaml_string = yaml_string.replace(url, replacement)

    with open(yaml_path, "w", encoding="utf8") as yaml_file:
        yaml_file.write(yaml_string)

    print("done")


# def oops_fix_naming():
#     public_dir = Path("tactics-site").absolute() / "public"
#     tokens_dir = public_dir / "images" / "tokens"
#     for file in tokens_dir.iterdir():
#         # file.copy
#         content = file.read_bytes()
#         new_path = public_dir / f"image_token_{file.stem}.jpg"
#         new_path.write_bytes(content)


if __name__ == "__main__":
    main()
