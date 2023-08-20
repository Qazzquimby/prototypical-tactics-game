import pygame

from drawer.base import BaseDrawer
from drawer.browser_drawer import BrowserDrawer
from drawer.color import convert_tts_to_pygame
from drawer.size_constants import CARD_SIZE


def draw_card_backs(drawer, surf, cards):
    if isinstance(cards[0].object.type.backside, str):
        drawer.draw_image(surf, cards[0].object.type.backside, surf.get_rect())
    else:
        surf.fill(convert_tts_to_pygame(cards[0].object.type.backside))


class CardBackDrawer(BaseDrawer):
    def __init__(self, config):
        self.config = config

    def draw(self, deck):
        drawer = BrowserDrawer(deck.cards[0].object, self.config)
        surf = pygame.Surface(CARD_SIZE)
        draw_card_backs(drawer, surf, deck.cards)
        return surf
