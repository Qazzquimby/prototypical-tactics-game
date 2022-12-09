import json

from pysftp.exceptions import ConnectionException

from core import xls_file_to_tts_save, xls_file_to_library
from image_builders import get_image_builder

import os, sys, pysftp
from shutil import copyfile

from tts_dir import try_and_find_save_games_folder
from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import font


class Config:
    def __init__(
        self,
        excelFile=StringVar(),
        saveDir=StringVar(),
        imagesDir=StringVar(),
        fileName=StringVar(),
        ftpServer=StringVar(),
        ftpFolder=StringVar(),
        ftpUsername=StringVar(),
        ftpPassword=StringVar(),
        ftpBaseUrl=StringVar(),
        developerKey=StringVar(),
        searchId=StringVar(),
    ):
        self.excelFile = excelFile
        self.saveDir = saveDir
        self.imagesDir = imagesDir
        self.fileName = fileName
        self.ftpServer = ftpServer
        self.ftpFolder = ftpFolder
        self.ftpUsername = ftpUsername
        self.ftpPassword = ftpPassword
        self.ftpBaseUrl = ftpBaseUrl
        self.developerKey = developerKey
        self.searchId = searchId
        self.saveFolderDeduced = False
        self.loadConfig()
        folder = try_and_find_save_games_folder()
        if folder:
            self.saveDir.set(folder)
            self.saveFolderDeduced = True

    def setExcelFile(self):
        self.excelFile.set(filedialog.askopenfilename(initialdir="~"))
        self.saveConfig()

    def setSaveDir(self):
        self.saveDir.set(filedialog.askdirectory(initialdir="~"))
        self.saveConfig()

    def setImagesDir(self):
        self.imagesDir.set(filedialog.askdirectory(initialdir="~"))
        self.saveConfig()

    def setFilename(self):
        self.fileName.set(simpledialog.askstring("Filename?", "Enter the filename:"))
        self.saveConfig()

    def setFtpSettings(self):
        self.ftpServer.set(
            simpledialog.askstring("Ftp server url?", "Enter the ftp url:")
        )
        if self.ftpServer.get() == "":
            self.ftpUsername.set("")
            self.ftpPassword.set("")
            self.ftpBaseUrl.set("")
            self.saveConfig()
            return
        self.ftpFolder.set(
            simpledialog.askstring("Ftp folder to use?", "Enter the folder:")
        )
        self.ftpUsername.set(
            simpledialog.askstring("Ftp server username?", "Enter the username:")
        )
        self.ftpPassword.set(
            simpledialog.askstring("Ftp server password?", "Enter the ftp password:")
        )
        self.ftpBaseUrl.set(
            simpledialog.askstring("Ftp www base url?", "Enter the ftp www base url:")
        )
        self.saveConfig()

    def readyToRun(self):
        return (
            self.excelFile.get()
            and self.saveDir.get()
            and self.imagesDir.get()
            and self.fileName.get()
        )

    def readyToParse(self):
        return self.excelFile.get()

    def isSaveFolderDeduced(self):
        return self.saveFolderDeduced

    def loadConfig(self):
        try:
            with open("settings.json", "r") as infile:
                data = json.load(infile)
                self.excelFile.set(data["e"])
                self.saveDir.set(data["s"])
                self.imagesDir.set(data["i"])
                self.fileName.set(data["f"])
                try:
                    self.ftpServer.set(data["f_s"])
                    self.ftpUsername.set(data["f_u"])
                    self.ftpPassword.set(data["f_p"])
                    self.ftpBaseUrl.set(data["f_w"])
                    self.ftpFolder.set(data["f_f"])
                except KeyError:
                    pass
                try:
                    self.developerKey.set(data["g_d"])
                    self.searchId.set(data["g_s"])
                except KeyError:
                    pass

        except FileNotFoundError:
            return

    def saveConfig(self):
        data = {
            "e": self.excelFile.get(),
            "s": self.saveDir.get(),
            "i": self.imagesDir.get(),
            "f": self.fileName.get(),
            "f_s": self.ftpServer.get(),
            "f_u": self.ftpUsername.get(),
            "f_p": self.ftpPassword.get(),
            "f_w": self.ftpBaseUrl.get(),
            "f_f": self.ftpFolder.get(),
            "g_d": self.developerKey.get(),
            "g_s": self.searchId.get(),
        }
        with open("settings.json", "w") as outfile:
            json.dump(data, outfile)


class App:
    def __init__(self, master):
        import pygame

        self.pygame = pygame
        self.master = master
        master.geometry("700x600")
        self.filenameVar = StringVar()
        self.config = Config(
            StringVar(),
            StringVar(),
            StringVar(),
            self.filenameVar,
            StringVar(),
            StringVar(),
            StringVar(),
            StringVar(),
            StringVar(),
            StringVar(),
            StringVar(),
        )

        frame = Frame(master)
        frame.grid()
        frame.grid_columnconfigure(1, minsize=400)

        self.customFont = font.Font(family="Arial", size=18)
        self.headerLabel = Label(frame, text="Prototypical!", font=self.customFont)
        self.headerLabel.grid(row=0, column=0, columnspan=2)

        self.ftpStatusText = StringVar()
        self.setFtpStatus()

        self.excelFile(frame)
        self.savedirFile(frame)
        self.imagedirFile(frame)
        self.filename(frame)
        self.ftpSettings(frame)

        buttonFrame = Frame(frame)
        buttonFrame.grid(row=6, column=1)

        self.parseButton = Button(buttonFrame, text="PARSE GAME", command=self.parse)
        self.parseButton.grid(row=0, column=0)

        self.buildButton = Button(buttonFrame, text="BUILD GAME", command=self.build)
        self.buildButton.grid(row=0, column=1)

        self.newTemplateButton = Button(
            buttonFrame, text="NEW TEMPLATE", command=self.template
        )
        self.newTemplateButton.grid(row=0, column=2)

        self.statusLabel = Label(frame, text="Status:")
        self.statusLabel.grid(row=7, column=0, columnspan=2)

        self.status = Text(frame)
        self.status.grid(row=8, column=0, columnspan=2)
        self.status.tag_configure("error", foreground="red", underline=True)

        try:
            version = open("data/version", "r").readline(10)
        except FileNotFoundError:
            version = "dev"

        self.statusLabel = Label(frame, text="version: " + version)
        self.statusLabel.grid(row=9, column=0, columnspan=2)

    def setFtpStatus(self):
        if self.config.ftpServer.get() != "":
            if testFtpConnection(self.config):
                self.ftpStatusText.set(
                    self.config.ftpServer.get() + " as " + self.config.ftpUsername.get()
                )
            else:
                self.ftpStatusText.set(
                    "Failed to connect to " + self.config.ftpServer.get()
                )
        else:
            self.ftpStatusText.set("Turned off (local only)")

    def excelFile(self, frame):
        self.excelButton = Button(
            frame, text="SET SPREADSHEET", command=self.config.setExcelFile, width=30
        )
        self.excelButton.grid(row=1, column=0)

        self.excelText = Label(frame, textvariable=self.config.excelFile)
        self.excelText.grid(row=1, column=1)

    def savedirFile(self, frame):
        if not self.config.isSaveFolderDeduced():
            self.savedirButton = Button(
                frame, text="SET SAVE DIR", command=self.config.setSaveDir, width=30
            )
            self.savedirButton.grid(row=2, column=0)

            self.savedirText = Label(frame, textvariable=self.config.saveDir)
            self.savedirText.grid(row=2, column=1)

    def imagedirFile(self, frame):
        self.imagedirButton = Button(
            frame, text="SET IMAGES DIR", command=self.config.setImagesDir, width=30
        )
        self.imagedirButton.grid(row=3, column=0)

        self.imagedirText = Label(frame, textvariable=self.config.imagesDir)
        self.imagedirText.grid(row=3, column=1)

    def filename(self, frame):
        self.filenameButton = Button(
            frame, text="SET GAME NAME", command=self.config.setFilename, width=30
        )
        self.filenameButton.grid(row=4, column=0)

        self.filenameText = Label(frame, textvariable=self.config.fileName)
        self.filenameText.grid(row=4, column=1)

    def ftpSettings(self, frame):
        self.ftpButton = Button(
            frame, text="CONFIGURE FTP", command=self.doFtpSettingsUpdate, width=30
        )
        self.ftpButton.grid(row=5, column=0)

        self.ftpText = Label(frame, textvariable=self.ftpStatusText)
        self.ftpText.grid(row=5, column=1)

    def doFtpSettingsUpdate(self):
        self.config.setFtpSettings()
        self.setFtpStatus()

    def template(self):
        file = filedialog.asksaveasfilename()
        if file:
            path = file + ".xls"
            try:
                copyfile("data/template.xls", path)
                self.pushStatusMessage("Created a new empty template: " + path)
                if sys.platform == "win32":
                    os.startfile(path)
            except FileNotFoundError:
                self.pushErrorMessage(
                    "The base template is missing. Please ensure that the application was installed successfully.",
                    "creating template",
                )

    def build(self):
        if self.config.readyToRun():
            self.flushStatus()
            try:
                xls_file_to_tts_save(
                    self.config.excelFile.get(),
                    get_image_builder(self.pygame, self.config),
                    self.config.saveDir.get(),
                    self.config.fileName.get(),
                    self.config,
                )
                self.pushStatusMessage("Done building!")
            except BaseException as e:
                self.pushErrorMessage(e)
                raise e
        else:
            self.pushErrorMessage(
                "Missing some settings. Please ensure all 4 settings above are configured properly."
            )

    def parse(self):
        self.flushStatus()
        try:
            xls_file_to_library(self.config.excelFile.get())
        except BaseException as e:
            self.pushErrorMessage(e)
            raise e

    def pushErrorMessage(self, e, during="building"):
        import traceback

        self.pushStatusMessage("\n")
        index = self.status.index(INSERT)
        curline = index.split(".")[0]
        self.pushStatusMessage("\nUh oh, there was a problem while " + during + ":")
        self.status.tag_add(
            "error", str(int(curline) + 1) + ".0", str(int(curline) + 2) + ".0"
        )
        self.pushStatusMessage(str(e))
        self.pushStatusMessage("\n" + traceback.format_exc())

    def pushStatusMessage(self, msg, newline=True):
        self.status.insert(END, msg + ("\n" if newline else ""))
        self.master.update()

    def flushStatus(self):
        self.status.delete(1.0, END)


def testFtpConnection(config):
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None

    try:
        con = pysftp.Connection(
            host=config.ftpServer.get(),
            username=config.ftpUsername.get(),
            password=config.ftpPassword.get(),
            cnopts=cnopts,
        )
        con.close()
        return True
    except ConnectionException:
        return False


if __name__ == "__main__":
    # runTests()

    # run the app
    root = Tk()
    root.wm_title("Prototypical")
    app = App(root)
    root.mainloop()
