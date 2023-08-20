import itertools

import pygame

from drawer.base import BaseDrawer
from drawer.complexObjectDrawer import ComplexObjectDrawer
from drawer.size_constants import CARD_WIDTH, CARD_HEIGHT, CARD_SIZE

DECK_IMAGE_CARDS_PER_ROW = 1  # 10
DECK_IMAGE_CARDS_PER_COLUMN = 1  # 7


class DeckDrawer(BaseDrawer):
    def __init__(self, config):
        self.config = config

    async def draw(self, deck):
        size = (
            CARD_WIDTH * DECK_IMAGE_CARDS_PER_ROW,
            CARD_HEIGHT * DECK_IMAGE_CARDS_PER_COLUMN,
        )

        surf = pygame.Surface(size)
        await self._draw_cards(surf, deck.cards, CARD_SIZE)
        return surf

    async def _draw_cards(
        self, surf, cards, card_size: tuple[int, int]
    ):  # I think this might be mirrored on the diagonal
        for card, (y, x) in zip(
            cards,
            itertools.product(
                range(DECK_IMAGE_CARDS_PER_COLUMN), range(DECK_IMAGE_CARDS_PER_ROW)
            ),
        ):
            card_drawer = ComplexObjectDrawer(card.object, self.config)
            card_image = await card_drawer.draw()
            surf.blit(card_image, (x * card_size[0], y * card_size[1]))
