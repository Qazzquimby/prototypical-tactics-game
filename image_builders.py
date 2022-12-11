import pysftp


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


class ImagesDirImageBuilder:
    def __init__(self, pygame, base_path):
        self.pygame = pygame
        self.basePath = base_path

    def build(self, image, file, extension):
        path = self.basePath / f"{file}.{extension}"
        self.pygame.image.save(image, path)
        return f"file:///{path}"


class FtpDirImageBuilder:
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

    def build(self, image, file, extension):
        local_path = self.image_base_path + "/" + file + "." + extension
        local_name = file + "." + extension
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
        return self.ftp_base_path + "/" + self.game_name + "/" + file + "." + extension
