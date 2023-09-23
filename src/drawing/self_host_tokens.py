import hashlib
import subprocess
import typing
from pathlib import Path
from time import sleep

import requests
import yaml

from src import yaml_parsing
from src.global_settings import global_config
from src.paths import SITE_PUBLIC_DIR, SITE_URL

if typing.TYPE_CHECKING:
    from src.yaml_parsing import Game

IMAGE_URL_KEY = "image_url"

url_replacements = {}

VERSION_PATH = Path(SITE_PUBLIC_DIR / "version.yaml")


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

    def get_hosted_address(self) -> str:
        return SITE_URL + self.get_local_name() + ".jpg"


def get_hosted_address(url, name):
    if global_config["production"]:
        return TokenImage(url=url, name=name).get_hosted_address()
    return url


def host_external_images(game: "Game", wait=True):
    image_urls = game.get_token_images()
    unsaved_image_urls = filter_unsaved_image_urls(image_urls)
    for token_image in unsaved_image_urls:
        save_image(token_image)

    if unsaved_image_urls:
        new_version = bump_version(mode="images")
        update_git()

        if wait:
            wait_for_version(new_version)


def save_image(token_image: TokenImage):
    if "tactics.toren.dev" in token_image.url:
        return  # already saved.

    name = token_image.get_local_name()
    print(f"Saving {name}")
    # if not exists
    dest_path = SITE_PUBLIC_DIR / f"{name}.jpg"
    if not dest_path.exists():
        with open(dest_path, "wb+") as f:
            f.write(requests.get(token_image.url).content)
    url_replacements[token_image.url] = (
        SITE_URL + dest_path.relative_to(SITE_PUBLIC_DIR).as_posix()
    )


def filter_unsaved_image_urls(token_images: list[TokenImage]) -> list[TokenImage]:
    unsaved_image_urls = []
    for token_image in token_images:
        if token_image.url.startswith(SITE_URL):
            continue  # already live

        local_image_name = token_image.get_local_name()
        local_image_path = SITE_PUBLIC_DIR / f"{local_image_name}.jpg"
        if not local_image_path.exists():
            unsaved_image_urls.append(token_image)

    return unsaved_image_urls


def bump_version(mode: typing.Literal["images", "cards"]):
    version_dict = yaml_parsing.read_yaml_file(str(VERSION_PATH))
    if version_dict["mode"] == "cards":
        version_dict["version"] += 1

    version_dict["mode"] = mode

    yaml_parsing.write_yaml_file(path=str(VERSION_PATH), content_dict=version_dict)
    return version_dict


def update_git():
    subprocess.check_call(["git", "add", SITE_PUBLIC_DIR])
    subprocess.check_call(["git", "commit", "-m", "update images"])
    subprocess.check_call(["git", "push"])


def wait_for_version(version_dict):
    # exponential dropoff wait for new version number to be live on site (wait for netlify build)
    max_wait_seconds = 60 * 5
    current_wait_seconds = 20

    while True:
        current_version = fetch_current_version()

        if current_version == version_dict:
            break

        if current_wait_seconds > max_wait_seconds:
            print("Waited too long for the expected version to propagate.")
            break

        print(f"Waiting {current_wait_seconds} seconds before trying again.")
        sleep(current_wait_seconds)
        current_wait_seconds *= 2


def fetch_current_version():
    response = requests.get(SITE_URL + "version.yaml")
    version_dict = yaml.safe_load(response.content)
    return version_dict


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
