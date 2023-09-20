import hashlib
import typing

import requests

from src import yaml_parsing
from src.paths import data_dir, site_public_dir, site_url

if typing.TYPE_CHECKING:
    from src.yaml_parsing import Game

IMAGE_URL_KEY = "image_url"

url_replacements = {}


class TokenImage:
    def __init__(self, url: str, name: str):
        self.url = url
        self.name = name

    def __repr__(self):
        return f"TokenImage(url={self.url}, name={self.name})"

    def get_local_name(self) -> str:
        hashed = hashlib.sha256(self.url.encode())
        short_hash = hashed.hexdigest()[:6]

        cleaned_name = (
            self.name.replace(" ", "_")
            .replace("'", "")
            .replace("(", "")
            .replace(")", "")
            .replace(",", "")
            .replace(".", "")
        )

        return f"image_token_{cleaned_name}_{short_hash}"


def host_external_images(game: "Game"):
    image_urls = game.get_token_images()
    unsaved_image_urls = filter_unsaved_image_urls(image_urls)
    for token_image in unsaved_image_urls:
        save_image(token_image)

    bump_version()

# def localize_image_urls(data: dict):
#     old_data = data.copy()
#     keys = list(data.keys())
#     for key in keys:
#         value = data[key]
#         if isinstance(value, dict):
#             data[key] = localize_image_urls(data[key])
#         if isinstance(value, list):
#             for i, item in enumerate(value):
#                 if isinstance(item, dict):
#                     data[key][i] = localize_image_urls(item)
#         elif key == IMAGE_URL_KEY:
#             save_image(value, data)
#     return data


def save_image(token_image: TokenImage):
    if "tactics.toren.dev" in token_image.url:
        return  # already saved.

    name = token_image.get_local_name()
    print(f"Saving {name}")
    # if not exists
    dest_path = site_public_dir / f"{name}.jpg"
    if not dest_path.exists():
        with open(dest_path, "wb+") as f:
            f.write(requests.get(token_image.url).content)
    url_replacements[token_image.url] = (
        site_url + dest_path.relative_to(site_public_dir).as_posix()
    )


def filter_unsaved_image_urls(token_images: list[TokenImage]) -> list[TokenImage]:
    unsaved_image_urls = []
    for token_image in token_images:
        if token_image.url.startswith(site_url):
            continue  # already live

        local_image_name = token_image.get_local_name()
        local_image_path = site_public_dir / f"{local_image_name}.jpg"
        if not local_image_path.exists():
            unsaved_image_urls.append(token_image)

    return unsaved_image_urls

def bump_version():
    return

# def main():
#     yaml_path = data_dir / "input.yaml"
#     yaml_content = yaml_parsing.read_yaml_file(yaml_path)
#
#     result = localize_image_urls(yaml_content)
#
#     with open(yaml_path, "r", encoding="utf8") as yaml_file:
#         yaml_string = yaml_file.read()
#
#     for url, replacement in url_replacements.items():
#         yaml_string = yaml_string.replace(url, replacement)
#
#     with open(yaml_path, "w", encoding="utf8") as yaml_file:
#         yaml_file.write(yaml_string)
#
#     print("done")
#
#
# # def oops_fix_naming():
# #     public_dir = Path("tactics-site").absolute() / "public"
# #     tokens_dir = public_dir / "images" / "tokens"
# #     for file in tokens_dir.iterdir():
# #         # file.copy
# #         content = file.read_bytes()
# #         new_path = public_dir / f"image_token_{file.stem}.jpg"
# #         new_path.write_bytes(content)
#
#
# if __name__ == "__main__":
#     main()
