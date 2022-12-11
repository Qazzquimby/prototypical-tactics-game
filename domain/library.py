from domain.bag import Bag
from domain.complexObject import ComplexObject
from domain.deck import Deck
from domain.die import Die
from domain.token import Token


class Library:
    def __init__(self, tokens: list[Token], dice: list[Die], complex_objects: list[ComplexObject], decks: list[Deck], bags: list[Bag]):
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
        decks = self._decks
        for bag in self.bags:
            decks += bag.get_decks()
        return decks

    @decks.setter
    def decks(self, value):
        self._decks = value