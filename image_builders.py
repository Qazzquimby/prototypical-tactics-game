import abc
import asyncio
import tempfile
from pathlib import Path

import pyimgbox as pyimgbox
import pysftp
from pygame import Surface
from retry import retry


def get_image_builder(pygame, config):
    if config.ftp_base_url.get() != "":
        return FtpDirImageBuilder(
            pygame,
            config.images_dir.get(),
            config.ftp_base_url.get(),
            config.ftp_server.get(),
            config.ftp_folder.get(),
            config.ftp_username.get(),
            config.ftp_password.get(),
            config.file_name.get(),
        )
    else:
        return ImagesDirImageBuilder(pygame, config.images_dir.get())


class ImageBuilder(abc.ABC):
    async def build(self, image: Surface, file_name: str, file_extension: str) -> str:
        raise NotImplementedError


class ImgBoxImagesBuilder(ImageBuilder):
    def __init__(self, pygame, project_name: str = "prototypical_project"):
        self.pygame = pygame
        self.project_name = project_name

        self.temp_dir = tempfile.TemporaryDirectory()
        self.images_dir_builder = ImagesDirImageBuilder(
            pygame, base_path=Path(self.temp_dir.name)
        )
        self.gallery = pyimgbox.Gallery(title=self.project_name)

        self.printed_url = False

    async def build(self, image: Surface, file_name: str, file_extension: str):
        save_path = (
            await self.save_to_temp_dir(image, file_name, file_extension)
        ).split("file:///")[1]

        result = await self.upload(save_path)
        return result["image_url"]

    async def save_to_temp_dir(self, image, file_name, file_extension):
        return await self.images_dir_builder.build(image, file_name, file_extension)

    @retry(tries=10, delay=2, backoff=2, jitter=(1, 3), exceptions=ConnectionError)
    async def upload(self, save_path: str):
        result = await self.gallery.upload(save_path)
        if not result["success"]:
            raise ConnectionError(
                f"Failed to upload image to imgbox\n {result['error']}"
            )

        if not self.printed_url:
            print(
                "imgbox gallery created\n"
                f"Url: {self.gallery.url}\n"
                f"Edit url: {self.gallery.edit_url}"
            )
            self.printed_url = True
        return result

    def __del__(self):
        self.temp_dir.cleanup()
        asyncio.get_event_loop().run_until_complete(self.gallery.close())


class ImagesDirImageBuilder(ImageBuilder):
    def __init__(self, pygame, base_path):
        self.pygame = pygame
        self.base_path = base_path

    async def build(self, image: Surface, file_name: str, file_extension: str):
        path = self.base_path / f"{file_name}.{file_extension}"
        self.pygame.image.save(image, path)
        return f"file:///{path}"


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
