import itertools

import pygame

from drawer.base import BaseDrawer
from drawer.complexObjectDrawer import ComplexObjectDrawer

DECK_IMAGE_CARDS_PER_ROW = 10
DECK_IMAGE_CARDS_PER_COLUMN = 7


class DeckDrawer(BaseDrawer):
    def __init__(self, config):
        self.config = config

    def draw(self, deck):
        drawer = ComplexObjectDrawer(deck.cards[0].object, self.config)
        w, h = drawer.get_card_size()
        size = (w * DECK_IMAGE_CARDS_PER_ROW, h * DECK_IMAGE_CARDS_PER_COLUMN)
        card_size = (w, h)

        surf = pygame.Surface(size)
        self._draw_cards(surf, deck.cards, card_size)
        return surf

    def _draw_cards(
        self, surf, cards, card_size: tuple[int, int]
    ):  # I think this might be mirrored on the diagonal
        for card, (y, x) in zip(
            cards,
            itertools.product(
                range(DECK_IMAGE_CARDS_PER_COLUMN), range(DECK_IMAGE_CARDS_PER_ROW)
            ),
        ):
            card_drawer = ComplexObjectDrawer(card.object, self.config)
            surf.blit(card_drawer.draw(), (x * card_size[0], y * card_size[1]))
