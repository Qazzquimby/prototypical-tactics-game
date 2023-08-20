import pygame

from drawer.base import BaseDrawer
from drawer.browser_drawer import BrowserDrawer
from drawer.size_constants import CARD_WIDTH, CARD_HEIGHT


class LoneCardDrawer(BaseDrawer):
    def __init__(self, config):
        self.config = config

    async def draw(self, card):
        try:
            size = card.object.type.size
        except AttributeError:
            size = (CARD_WIDTH, CARD_HEIGHT)

        surf = pygame.Surface(size)

        card_drawer = BrowserDrawer(card.object, self.config)
        card_image = await card_drawer.draw()
        surf.blit(card_image, (0, 0))

        return surf
