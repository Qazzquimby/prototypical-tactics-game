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
        excel_file=StringVar(),
        save_dir=StringVar(),
        images_dir=StringVar(),
        file_name=StringVar(),
        ftp_server=StringVar(),
        ftp_folder=StringVar(),
        ftp_username=StringVar(),
        ftp_password=StringVar(),
        ftp_base_url=StringVar(),
        developer_key=StringVar(),
        search_id=StringVar(),
    ):
        self.excel_file = excel_file
        self.save_dir = save_dir
        self.images_dir = images_dir
        self.file_name = file_name
        self.ftp_server = ftp_server
        self.ftp_folder = ftp_folder
        self.ftp_username = ftp_username
        self.ftp_password = ftp_password
        self.ftp_base_url = ftp_base_url
        self.developer_key = developer_key
        self.search_id = search_id
        self.save_folder_deduced = False
        self.load_config()
        folder = try_and_find_save_games_folder()
        if folder:
            self.save_dir.set(folder)
            self.save_folder_deduced = True

    def set_excel_file(self):
        self.excel_file.set(filedialog.askopenfilename(initialdir="~"))
        self.save_config()

    def set_save_dir(self):
        self.save_dir.set(filedialog.askdirectory(initialdir="~"))
        self.save_config()

    def set_images_dir(self):
        self.images_dir.set(filedialog.askdirectory(initialdir="~"))
        self.save_config()

    def set_filename(self):
        self.file_name.set(simpledialog.askstring("Filename?", "Enter the filename:"))
        self.save_config()

    def set_ftp_settings(self):
        self.ftp_server.set(
            simpledialog.askstring("Ftp server url?", "Enter the ftp url:")
        )
        if self.ftp_server.get() == "":
            self.ftp_username.set("")
            self.ftp_password.set("")
            self.ftp_base_url.set("")
            self.save_config()
            return
        self.ftp_folder.set(
            simpledialog.askstring("Ftp folder to use?", "Enter the folder:")
        )
        self.ftp_username.set(
            simpledialog.askstring("Ftp server username?", "Enter the username:")
        )
        self.ftp_password.set(
            simpledialog.askstring("Ftp server password?", "Enter the ftp password:")
        )
        self.ftp_base_url.set(
            simpledialog.askstring("Ftp www base url?", "Enter the ftp www base url:")
        )
        self.save_config()

    def ready_to_run(self):
        return (
            self.excel_file.get()
            and self.save_dir.get()
            and self.images_dir.get()
            and self.file_name.get()
        )

    def ready_to_parse(self):
        return self.excel_file.get()

    def is_save_folder_deduced(self):
        return self.save_folder_deduced

    def load_config(self):
        try:
            with open("settings.json", "r") as infile:
                data = json.load(infile)
                self.excel_file.set(data["e"])
                self.save_dir.set(data["s"])
                self.images_dir.set(data["i"])
                self.file_name.set(data["f"])
                try:
                    self.ftp_server.set(data["f_s"])
                    self.ftp_username.set(data["f_u"])
                    self.ftp_password.set(data["f_p"])
                    self.ftp_base_url.set(data["f_w"])
                    self.ftp_folder.set(data["f_f"])
                except KeyError:
                    pass
                try:
                    self.developer_key.set(data["g_d"])
                    self.search_id.set(data["g_s"])
                except KeyError:
                    pass

        except FileNotFoundError:
            return

    def save_config(self):
        data = {
            "e": self.excel_file.get(),
            "s": self.save_dir.get(),
            "i": self.images_dir.get(),
            "f": self.file_name.get(),
            "f_s": self.ftp_server.get(),
            "f_u": self.ftp_username.get(),
            "f_p": self.ftp_password.get(),
            "f_w": self.ftp_base_url.get(),
            "f_f": self.ftp_folder.get(),
            "g_d": self.developer_key.get(),
            "g_s": self.search_id.get(),
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
        self.set_ftp_status()

        self.excel_file(frame)
        self.savedir_file(frame)
        self.imagedir_file(frame)
        self.filename(frame)
        self.ftp_settings(frame)

        button_frame = Frame(frame)
        button_frame.grid(row=6, column=1)

        self.parseButton = Button(button_frame, text="PARSE GAME", command=self.parse)
        self.parseButton.grid(row=0, column=0)

        self.buildButton = Button(button_frame, text="BUILD GAME", command=self.build)
        self.buildButton.grid(row=0, column=1)

        self.newTemplateButton = Button(
            button_frame, text="NEW TEMPLATE", command=self.template
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

    def set_ftp_status(self):
        if self.config.ftp_server.get() != "":
            if test_ftp_connection(self.config):
                self.ftpStatusText.set(
                    self.config.ftp_server.get()
                    + " as "
                    + self.config.ftp_username.get()
                )
            else:
                self.ftpStatusText.set(
                    "Failed to connect to " + self.config.ftp_server.get()
                )
        else:
            self.ftpStatusText.set("Turned off (local only)")

    def excel_file(self, frame):
        self.excel_button = Button(
            frame, text="SET SPREADSHEET", command=self.config.set_excel_file, width=30
        )
        self.excel_button.grid(row=1, column=0)

        self.excel_text = Label(frame, textvariable=self.config.excel_file)
        self.excel_text.grid(row=1, column=1)

    def savedir_file(self, frame):
        if not self.config.is_save_folder_deduced():
            self.savedir_button = Button(
                frame, text="SET SAVE DIR", command=self.config.set_save_dir, width=30
            )
            self.savedir_button.grid(row=2, column=0)

            self.savedir_text = Label(frame, textvariable=self.config.save_dir)
            self.savedir_text.grid(row=2, column=1)

    def imagedir_file(self, frame):
        self.imagedir_button = Button(
            frame, text="SET IMAGES DIR", command=self.config.set_images_dir, width=30
        )
        self.imagedir_button.grid(row=3, column=0)

        self.imagedir_text = Label(frame, textvariable=self.config.images_dir)
        self.imagedir_text.grid(row=3, column=1)

    def filename(self, frame):
        self.filename_button = Button(
            frame, text="SET GAME NAME", command=self.config.set_filename, width=30
        )
        self.filename_button.grid(row=4, column=0)

        self.filename_text = Label(frame, textvariable=self.config.file_name)
        self.filename_text.grid(row=4, column=1)

    def ftp_settings(self, frame):
        self.ftp_button = Button(
            frame, text="CONFIGURE FTP", command=self.do_ftp_settings_update, width=30
        )
        self.ftp_button.grid(row=5, column=0)

        self.ftp_text = Label(frame, textvariable=self.ftpStatusText)
        self.ftp_text.grid(row=5, column=1)

    def do_ftp_settings_update(self):
        self.config.set_ftp_settings()
        self.set_ftp_status()

    def template(self):
        file = filedialog.asksaveasfilename()
        if file:
            path = file + ".xls"
            try:
                copyfile("data/template.xls", path)
                self.push_status_message("Created a new empty template: " + path)
                if sys.platform == "win32":
                    os.startfile(path)
            except FileNotFoundError:
                self.push_error_message(
                    "The base template is missing. Please ensure that the application was installed successfully.",
                    "creating template",
                )

    def build(self):
        if self.config.ready_to_run():
            self.flush_status()
            try:
                xls_file_to_tts_save(
                    self.config.excel_file.get(),
                    get_image_builder(self.pygame, self.config),
                    self.config.save_dir.get(),
                    self.config.file_name.get(),
                    self.config,
                )
                self.push_status_message("Done building!")
            except BaseException as e:
                self.push_error_message(e)
                raise e
        else:
            self.push_error_message(
                "Missing some settings. Please ensure all 4 settings above are configured properly."
            )

    def parse(self):
        self.flush_status()
        try:
            xls_file_to_library(self.config.excel_file.get())
        except BaseException as e:
            self.push_error_message(e)
            raise e

    def push_error_message(self, e, during="building"):
        import traceback

        self.push_status_message("\n")
        index = self.status.index(INSERT)
        curline = index.split(".")[0]
        self.push_status_message("\nUh oh, there was a problem while " + during + ":")
        self.status.tag_add(
            "error", str(int(curline) + 1) + ".0", str(int(curline) + 2) + ".0"
        )
        self.push_status_message(str(e))
        self.push_status_message("\n" + traceback.format_exc())

    def push_status_message(self, msg, newline=True):
        self.status.insert(END, msg + ("\n" if newline else ""))
        self.master.update()

    def flush_status(self):
        self.status.delete(1.0, END)


def test_ftp_connection(config):
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None

    try:
        con = pysftp.Connection(
            host=config.ftp_server.get(),
            username=config.ftp_username.get(),
            password=config.ftp_password.get(),
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
