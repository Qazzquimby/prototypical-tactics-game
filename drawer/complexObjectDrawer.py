import asyncio
import io
from pathlib import Path

from playwright.async_api import async_playwright
import jinja2
import pygame

from drawer.base import BaseDrawer
from drawer.textrect import render_fitted_textrect
from drawer.color import convert_tts_to_pygame

EDGE_MARGIN = 10

LEFTRIGHT_MARGIN = 10
TOPBOTTOM_MARGIN = 10

TemplatesPath = Path("data/templates")

_BROWSER = None
lock= asyncio.Lock()

async def get_browser():
    global _BROWSER
    if _BROWSER is None:
        async with lock:
            if _BROWSER is None:
                p = await async_playwright().start()
                _BROWSER = await p.chromium.launch()
    return _BROWSER

def make_empty_image(filepath):
    surf = pygame.Surface((10, 10))
    pygame.image.save(surf, filepath)


class ComplexObjectDrawer(BaseDrawer):
    def __init__(self, obj, config):
        self.object = obj
        self.config = config
        self.size = obj.type.shape.size

        self.surf = None
        self.full_surf = None


    async def draw(self, _=None):
        # draws self, so doesn't need the object param
        w, h = self.get_card_size()
        image_width = w - (2 * EDGE_MARGIN)
        image_height = h - (2 * EDGE_MARGIN)
        self.surf = pygame.Surface((image_width, image_height))

        # if self.object.type.name == "Ability":
        html_template_path = TemplatesPath / "card.html"
        css_template_path = TemplatesPath / "card.css"

        name = self.object.content.name
        temp_path = Path("data/temp_images") / f"{name}.png"

        html_template = html_template_path.read_text()
        html = jinja2.Template(html_template).render(
            width=image_width- 2*EDGE_MARGIN, #shouldnt be needed but theres clipping
            height=image_height,
            name=name,
            text=self.object.content.text,
            owner="todo: owner",
        )

        browser = await get_browser()
        page = await browser.new_page()
        await page.set_viewport_size({"width": image_width, "height": image_height})
        await page.set_content(html)
        await page.add_style_tag(content=css_template_path.read_text())
        image_bytes = await page.screenshot()#path=temp_path)

        # image = pygame.image.load(temp_path)
        image = pygame.image.load(io.BytesIO(image_bytes), "img.png")

        self.surf.blit(image, (0, 0))

        self.full_surf = pygame.Surface((w, h))
        self.full_surf.fill(convert_tts_to_pygame((0, 0, 0)))

        self.full_surf.blit(self.surf, (EDGE_MARGIN, EDGE_MARGIN))
        return self.full_surf

    def get_card_size(self):
        return self.object.type.size

    # note: areas in the shape are actually row, col and not x,y
    def draw_content_to_area(self, content, area):
        w, h = self.get_card_size()
        dw = w - (2 * EDGE_MARGIN)
        dh = h - (2 * EDGE_MARGIN)
        rect = pygame.Rect(
            LEFTRIGHT_MARGIN + area[1] * dw / self.size[0],
            TOPBOTTOM_MARGIN + area[0] * dh / self.size[1],
            (area[3] + 1) * dw / self.size[0] - LEFTRIGHT_MARGIN,
            (area[2] + 1) * dh / self.size[1] - TOPBOTTOM_MARGIN,
        )
        if isinstance(content, str) and "\\icon" in content:
            self.draw_icon(self.surf, content, rect)
        elif isinstance(content, str) and "\\image" in content:
            self.draw_image(self.surf, content, rect)
        else:
            self.write(content, rect)

    def write(self, content, rect):
        if isinstance(content, float) and content.is_integer():
            content = int(content)

        # the render function expects a rect with 0,0 topleft.
        rerect = pygame.Rect((0, 0, rect[2] - rect[0], rect[3] - rect[1]))
        surf = render_fitted_textrect(str(content), rerect, (0, 0, 0), (255, 255, 255))
        if not surf:
            raise ValueError(
                "Unable to draw the card. Are you reserving enough space for all your content? Trying to write: "
                + str(content)
            )
        self.surf.blit(surf, rect)

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
