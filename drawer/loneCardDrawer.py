import pygame

from drawer.base import BaseDrawer
from drawer.complexObjectDrawer import ComplexObjectDrawer
from drawer.size_constants import CARD_WIDTH, CARD_HEIGHT, CARD_SIZE


class LoneCardDrawer(BaseDrawer):
    def __init__(self, config):
        self.config = config

    async def draw(self, card):
        try:
            size = card.object.type.size
        except AttributeError:
            size = (CARD_WIDTH, CARD_HEIGHT)

        surf = pygame.Surface(size)

        card_drawer = ComplexObjectDrawer(card.object, self.config)
        card_image = await card_drawer.draw()
        surf.blit(card_image, (0, 0))

        return surf
