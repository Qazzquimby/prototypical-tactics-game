import io
from pathlib import Path

import pygame

from domain.card import Card
from src.browser import get_browser
from src.drawing.base import BaseDrawer
from src.drawing.color import convert_tts_to_pygame
from src.drawing.css_maker import make_css
from src.drawing.size_constants import (
    CARD_WIDTH,
    CARD_HEIGHT,
    EDGE_MARGIN,
    IMAGE_WIDTH,
    IMAGE_HEIGHT,
)
from src.global_settings import global_config
from src.paths import DATA_DIR

TemplatesPath = DATA_DIR / "templates"


CARD_CSS = make_css()


class CardDrawer(BaseDrawer):
    def __init__(self, config):
        self.config = config

    async def draw(self, card: Card) -> pygame.Surface:
        card_object = card.object
        # using browser screenshot
        try:
            card_width = card_object.type.size[0]
            card_height = card_object.type.size[1]
            image_width = card_object.type.size[0] - (2 * EDGE_MARGIN)
            image_height = card_object.type.size[1] - (2 * EDGE_MARGIN)
        except AttributeError:
            card_width = CARD_WIDTH
            card_height = CARD_HEIGHT
            image_width = IMAGE_WIDTH
            image_height = IMAGE_HEIGHT

        surf = pygame.Surface((image_width, image_height))

        browser = get_browser()
        page = await browser.new_page()

        await page.set_viewport_size({"width": image_width, "height": image_height})

        html = card_object.content.get_html()
        await page.set_content(html)
        await page.add_style_tag(content=CARD_CSS)

        await page.evaluate(
            """
            () => {
                const meta = document.createElement('meta');
                // <meta http-equiv="content-type" content="text/html; charset=utf-8" />
                meta.setAttribute('http-equiv', 'content-type');
                meta.setAttribute('content', 'text/html; charset=utf-8');
                document.head.appendChild(meta);
            }
        """
        )

        if global_config["prune_for_playtest"]:
            content = await page.content()
            root = Path("card_html")
            root.mkdir(exist_ok=True)
            (root / f"{card_object.content.name}.html").write_text(
                content, encoding="utf-8"
            )

        image_bytes = await page.screenshot()  # path=temp_path)

        image = pygame.image.load(io.BytesIO(image_bytes), "img.png")
        surf.blit(image, (0, 0))

        full_surf = pygame.Surface((card_width, card_height))
        full_surf.fill(convert_tts_to_pygame((0, 0, 0)))

        full_surf.blit(surf, (EDGE_MARGIN, EDGE_MARGIN))
        return full_surf
