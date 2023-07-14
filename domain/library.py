from domain.bag import Bag
from domain.complexObject import ComplexObject
from domain.deck import Deck
from domain.die import Die
from domain.token import Token


class Library:
    def __init__(
        self,
        tokens: list[Token],
        dice: list[Die],
        complex_objects: list[ComplexObject],
        decks: list[Deck],
        bags: list[Bag],
    ):
        self.tokens = tokens
        self.dice = dice
        self.complex_objects = complex_objects
        self._decks = decks
        self.bags = bags

    def all(self):
        return self.tokens + self.dice + self.complex_objects + self.decks + self.bags

    @property
    def decks(self):
        # search bags for decks
        current_decks = self._decks.copy()
        for bag in self.bags:
            current_decks += bag.get_decks()
        return current_decks

    @decks.setter
    def decks(self, value):
        self._decks = value


def get_hero_boxes(library: Library):
    hero_boxes = []
    game_bag = library.bags[0]
    set_bags = [item for item in game_bag.content if isinstance(item, Bag)]
    for set_bag in set_bags:
        hero_boxes += set_bag.content

    return hero_boxes
