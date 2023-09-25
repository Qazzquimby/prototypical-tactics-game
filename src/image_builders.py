import abc
import asyncio
import tempfile
from pathlib import Path

import pyimgbox as pyimgbox
import pysftp
from pygame import Surface
from retry import retry

from src.paths import SITE_URL


class ImageBuilder(abc.ABC):
    async def build(self, image: Surface, file_name: str, file_extension: str) -> str:
        raise NotImplementedError

    def get_path(self, file_name: str, file_extension: str):
        raise NotImplementedError

    async def initialize(self):
        pass  # by default doesnt need initializing


class ImgBoxImagesBuilder(ImageBuilder):
    def __init__(self, pygame, project_name: str = "prototypical_project"):
        self.pygame = pygame
        self.project_name = project_name

        self.temp_dir = tempfile.TemporaryDirectory()
        self.images_dir_builder = DirectoryImagesBuilder(
            pygame, base_path=Path(self.temp_dir.name)
        )
        self.gallery = pyimgbox.Gallery(title="prototypical_project")

    async def initialize(self):
        await self.gallery.create()
        print(
            "imgbox gallery created\n"
            f"Url: {self.gallery.url}\n"
            f"Edit url: {self.gallery.edit_url}"
        )

    async def build(self, image: Surface, file_name: str, file_extension: str):
        save_path = (
            await self.save_to_temp_dir(image, file_name, file_extension)
        ).split("file:///")[1]

        result = await self.upload(save_path)
        return result["image_url"]

    def get_path(self, file_name: str, file_extension: str):
        raise NotImplementedError  # this builder cant get the path without uploading

    async def save_to_temp_dir(self, image, file_name, file_extension):
        return await self.images_dir_builder.build(image, file_name, file_extension)

    @retry(tries=10, delay=2, backoff=2, jitter=(1, 3), exceptions=ConnectionError)
    async def upload(self, save_path: str):
        result = await self.gallery.upload(save_path)
        if not result["success"]:
            raise ConnectionError(
                f"Failed to upload image to imgbox\n {result['error']}"
            )
        return result

    def __del__(self):
        self.temp_dir.cleanup()
        asyncio.gather(self.gallery.close())


class DirectoryImagesBuilder(ImageBuilder):
    def __init__(self, pygame, base_path):
        self.pygame = pygame
        self.base_path = base_path

    async def build(self, image: Surface, file_name: str, file_extension: str) -> str:
        path = self._get_local_path(file_name, file_extension)
        self.pygame.image.save(image, path)

    def get_path(self, file_name: str, file_extension: str):
        self._get_local_path(file_name, file_extension)

    def _get_local_path(self, file_name: str, file_extension: str):
        path = self.base_path / f"image_{file_name}.{file_extension}"
        return f"file:///{path}"


class OnlineImagesBuilder(DirectoryImagesBuilder):
    def __init__(self, pygame, base_path):
        super().__init__(pygame, base_path)

    async def build(self, image: Surface, file_name: str, file_extension: str):
        await super().build(image, file_name, file_extension)

    def get_path(self, file_name: str, file_extension: str):
        return f"{SITE_URL}image_{file_name}.{file_extension}"


class FtpDirImageBuilder(ImageBuilder):
    def __init__(
        self,
        pygame,
        image_base_path,
        ftp_base_path,
        ftp_server,
        ftp_folder,
        ftp_username,
        ftp_password,
        game_name,
    ):
        self.image_base_path = image_base_path
        self.ftp_base_path = ftp_base_path
        self.pygame = pygame
        self.ftp_server = ftp_server
        self.ftp_folder = ftp_folder
        self.ftp_username = ftp_username
        self.ftp_password = ftp_password
        self.game_name = game_name

    async def build(self, image, file_name, file_extension):
        local_path = self.image_base_path + "/" + file_name + "." + file_extension
        local_name = file_name + "." + file_extension
        self.pygame.image.save(image, local_path)
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        con = pysftp.Connection(
            host=self.ftp_server,
            username=self.ftp_username,
            password=self.ftp_password,
            cnopts=cnopts,
        )
        with pysftp.cd(self.image_base_path):
            con.chdir(self.ftp_folder)
            if not con.exists(self.game_name):
                con.mkdir(self.game_name)
            con.chdir(self.game_name)
            if con.exists(self.game_name):
                con.remove(local_name)
            con.put(local_name)
        con.close()
        return (
            self.ftp_base_path
            + "/"
            + self.game_name
            + "/"
            + file_name
            + "."
            + file_extension
        )
