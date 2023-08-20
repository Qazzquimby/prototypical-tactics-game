import io
from pathlib import Path
import pygame

from src.browser import get_browser
from drawer.base import BaseDrawer
from drawer.color import convert_tts_to_pygame
from drawer.css_maker import make_css
from drawer.size_constants import (
    CARD_WIDTH,
    CARD_HEIGHT,
    EDGE_MARGIN,
    IMAGE_WIDTH,
    IMAGE_HEIGHT,
)
from src.paths import data_dir

TemplatesPath = data_dir / "templates"


# CARD_CSS = (TemplatesPath / "card.css").read_text()
CARD_CSS = make_css()


class BrowserDrawer(BaseDrawer):
    def __init__(self, obj, config):
        self.object = obj
        self.config = config

        self.surf = None
        self.full_surf = None

    async def draw(self, _=None) -> pygame.Surface:
        # using browser screenshot
        try:
            card_width = self.object.type.size[0]
            card_height = self.object.type.size[1]
            image_width = self.object.type.size[0] - (2 * EDGE_MARGIN)
            image_height = self.object.type.size[1] - (2 * EDGE_MARGIN)
        except AttributeError:
            card_width = CARD_WIDTH
            card_height = CARD_HEIGHT
            image_width = IMAGE_WIDTH
            image_height = IMAGE_HEIGHT

        self.surf = pygame.Surface((image_width, image_height))

        browser = get_browser()
        page = await browser.new_page()
        await page.set_viewport_size({"width": image_width, "height": image_height})

        html = self.object.content.get_html()
        await page.set_content(html)
        await page.add_style_tag(content=CARD_CSS)
        image_bytes = await page.screenshot()  # path=temp_path)

        # image = pygame.image.load(temp_path)
        image = pygame.image.load(io.BytesIO(image_bytes), "img.png")
        self.surf.blit(image, (0, 0))

        self.full_surf = pygame.Surface((card_width, card_height))
        self.full_surf.fill(convert_tts_to_pygame((0, 0, 0)))

        self.full_surf.blit(self.surf, (EDGE_MARGIN, EDGE_MARGIN))
        return self.full_surf

    def base_draw_image(self, surf, content, rect, type_):
        import pygame

        rerect = pygame.Rect((0, 0, rect[2] - rect[0], rect[3] - rect[1]))
        if type_ == "icon":
            picture = self.obtain_icon(content)
        else:
            picture = self.obtain_image(content)
        # rescale but keep proportions
        orig_width = picture.get_width()
        orig_height = picture.get_height()
        scale_factor = min(rerect.width / orig_width, rerect.height / orig_height)

        scaled_picture = pygame.transform.scale(
            picture, (int(orig_width * scale_factor), int(orig_height * scale_factor))
        )

        surf.blit(scaled_picture, rect)

    def draw_icon(self, surf, content, rect):
        self.base_draw_image(surf, content, rect, "icon")

    def draw_image(self, surf, content, rect):
        self.base_draw_image(surf, content, rect, "image")

    def base_obtain_image(self, content, type_, replace, folder):
        name = content.replace(replace, "")
        filename = self.get_path_for_image(folder, name)
        try:
            return pygame.image.load(filename)
        except FileNotFoundError:
            if type_ == "icon":
                self.make_icon(name)
                return self.obtain_icon(content)
            else:
                self.make_image(name)
                return self.obtain_image(content)

    def obtain_icon(self, content):
        return self.base_obtain_image(content, "icon", "\\icon ", "icons")

    def obtain_image(self, content):
        return self.base_obtain_image(content, "image", "\\image ", "images")

    def make_icon(self, name):
        self.make_image_base(name, name + " icon", "icons", "gray")

    def make_image(self, name):
        self.make_image_base(name, name, "images", "color")

    def make_image_base(self, name, query, folder, color_type):
        pass
        # import requests
        # from apiclient.discovery import build
        #
        # filepath = self.get_path_for_image(folder, name)
        #
        # if self.config.developerKey.get() == "":
        #     make_empty_image(filepath)
        #     return
        #
        # service = build(
        #     "customsearch", "v1", developerKey=self.config.developerKey.get()
        # )
        # try:
        #     res = (
        #         service.cse()
        #         .list(
        #             q=name + query,
        #             cx=self.config.searchId.get(),
        #             searchType="image",
        #             num=1,
        #             fileType="jpg",
        #             imgColorType=color_type,
        #             safe="off",
        #         )
        #         .execute()
        #     )
        #
        #     if "items" not in res:
        #         raise ValueError("Could not find an icon for: " + name)
        #     else:
        #         for item in res["items"]:
        #             with open(filepath, "wb") as handler:
        #                 img_data = requests.get(item["link"]).content
        #                 handler.write(img_data)
        # except ValueError:
        #     make_empty_image(filepath)

    def get_path_for_image(self, subfolder, image_name):
        import os

        if not os.path.exists(self.config.images_dir.get() + "/" + subfolder):
            os.mkdir(self.config.images_dir.get() + "/" + subfolder)
        return (
            self.config.images_dir.get()
            + "/"
            + subfolder
            + "/"
            + image_name.replace(" ", "_")
            + ".jpg"
        )
