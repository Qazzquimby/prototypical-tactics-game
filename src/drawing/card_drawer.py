import io
from pathlib import Path
import pygame

from domain.card import Card
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


CARD_CSS = make_css()


class CardDrawer(BaseDrawer):
    def __init__(self, config):
        self.config = config

    async def draw(self, card: Card) -> pygame.Surface:
        object_ = card.object
        # using browser screenshot
        try:
            card_width = object_.type.size[0]
            card_height = object_.type.size[1]
            image_width = object_.type.size[0] - (2 * EDGE_MARGIN)
            image_height = object_.type.size[1] - (2 * EDGE_MARGIN)
        except AttributeError:
            card_width = CARD_WIDTH
            card_height = CARD_HEIGHT
            image_width = IMAGE_WIDTH
            image_height = IMAGE_HEIGHT

        surf = pygame.Surface((image_width, image_height))

        browser = get_browser()
        page = await browser.new_page()
        await page.set_viewport_size({"width": image_width, "height": image_height})

        html = object_.content.get_html()
        await page.set_content(html)
        await page.add_style_tag(content=CARD_CSS)
        image_bytes = await page.screenshot()  # path=temp_path)

        image = pygame.image.load(io.BytesIO(image_bytes), "img.png")
        surf.blit(image, (0, 0))

        full_surf = pygame.Surface((card_width, card_height))
        full_surf.fill(convert_tts_to_pygame((0, 0, 0)))

        full_surf.blit(surf, (EDGE_MARGIN, EDGE_MARGIN))
        return full_surf
