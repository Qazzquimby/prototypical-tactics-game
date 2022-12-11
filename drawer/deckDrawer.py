import pygame
from drawer.complexObjectDrawer import ComplexObjectDrawer

# todo this is really stupid organization.
#  What is the difference between draw and draw_cards?
#  draw initializes the variables. Should make a new instance each time instead of mutating on draw.
class DeckDrawer:
    def __init__(self, config):
        self.config = config

    def draw(self, deck):
        drawer = ComplexObjectDrawer(deck.cards[0].object, self.config)
        w, h = drawer.get_card_size()
        self.size = (w * 10, h * 7)
        self.card_size = (w, h)

        surf = pygame.Surface(self.size)
        self.draw_cards(surf, deck.cards)
        return surf

    def draw_cards(self, surf, cards):
        done = 0  # todo make this a proper enumerated loop.
        for i in range(0, 7):
            for j in range(0, 10):
                card_drawer = ComplexObjectDrawer(cards[done].object, self.config)
                surf.blit(
                    card_drawer.draw(), (j * self.card_size[0], i * self.card_size[1])
                )
                done += 1
                if done == len(cards):
                    return
