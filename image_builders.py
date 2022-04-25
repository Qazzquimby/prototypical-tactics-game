import pysftp


def get_image_builder(pygame, config):
    if config.ftpBaseUrl.get() != "":
        return ftpDirImageBuilder(
            pygame,
            config.imagesDir.get(),
            config.ftpBaseUrl.get(),
            config.ftpServer.get(),
            config.ftpFolder.get(),
            config.ftpUsername.get(),
            config.ftpPassword.get(),
            config.fileName.get(),
        )
    else:
        return ImagesDirImageBuilder(pygame, config.imagesDir.get())


class ImagesDirImageBuilder:
    def __init__(self, pygame, basePath):
        self.pygame = pygame
        self.basePath = basePath

    def build(self, image, file, extension):
        path = self.basePath + "/" + file + "." + extension
        self.pygame.image.save(image, path)
        return "file:///" + path


class ftpDirImageBuilder:
    def __init__(
        self,
        pygame,
        imageBasePath,
        ftpBasePath,
        ftpServer,
        ftpFolder,
        ftpUsername,
        ftpPassword,
        gameName,
    ):
        self.imageBasePath = imageBasePath
        self.ftpBasePath = ftpBasePath
        self.pygame = pygame
        self.ftpServer = ftpServer
        self.ftpFolder = ftpFolder
        self.ftpUsername = ftpUsername
        self.ftpPassword = ftpPassword
        self.gameName = gameName

    def build(self, image, file, extension):
        localPath = self.imageBasePath + "/" + file + "." + extension
        localName = file + "." + extension
        self.pygame.image.save(image, localPath)
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        con = pysftp.Connection(
            host=self.ftpServer,
            username=self.ftpUsername,
            password=self.ftpPassword,
            cnopts=cnopts,
        )
        with pysftp.cd(self.imageBasePath):
            con.chdir(self.ftpFolder)
            if not con.exists(self.gameName):
                con.mkdir(self.gameName)
            con.chdir(self.gameName)
            if con.exists(self.gameName):
                con.remove(localName)
            con.put(localName)
        con.close()
        return self.ftpBasePath + "/" + self.gameName + "/" + file + "." + extension
