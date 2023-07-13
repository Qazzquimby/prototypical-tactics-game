import io
from pathlib import Path

import pygame

from drawer.base import BaseDrawer
from drawer.complexObjectDrawer import get_browser


class HeroBoxDrawer(BaseDrawer):
    def __init__(self, config):
        self.config = config

    async def draw(self, deck):
        w, h = 2071, 1827
        box_size = (w, h)

        surf = pygame.Surface(box_size)

        browser = await get_browser()
        page = await browser.new_page()
        await page.set_viewport_size({"width": w, "height": h})

        html = Path("data/templates/box.html").read_text()
        css = Path("data/templates/box.css").read_text()

        await page.set_content(html)
        await page.add_style_tag(content=css)
        image_bytes = await page.screenshot()  # path=temp_path)

        # image = pygame.image.load(temp_path)
        image = pygame.image.load(io.BytesIO(image_bytes), "img.png")
        surf.blit(image, (0, 0))

        return surf
