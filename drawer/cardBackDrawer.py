import pygame
from drawer.complexObjectDrawer import ComplexObjectDrawer
from drawer.color import convert_tts_to_pygame


def draw_card_backs(drawer, surf, cards):
    if isinstance(cards[0].object.type.backside, str):
        drawer.draw_image(surf, cards[0].object.type.backside, surf.get_rect())
    else:
        surf.fill(convert_tts_to_pygame(cards[0].object.type.backside))


class CardBackDrawer:
    def __init__(self, config):
        self.config = config

    def draw(self, deck):
        drawer = ComplexObjectDrawer(deck.cards[0].object, self.config)
        surf = pygame.Surface(drawer.get_card_size())
        draw_card_backs(drawer, surf, deck.cards)
        return surf
