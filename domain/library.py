from domain.bag import Bag, CustomBag
from domain.card import LoneCard
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

    @property
    def lone_cards(self):
        result = []
        for bag in self.bags:
            result += recursive_search(bag, LoneCard)
        return result


def get_hero_boxes(library: Library):
    hero_boxes = []
    game_bag = library.bags[0]
    set_bags = [item for item in game_bag.content if isinstance(item, Bag)]
    for set_bag in set_bags:
        hero_boxes_in_bag = [
            item for item in set_bag.content if isinstance(item, CustomBag)
        ]
        hero_boxes += hero_boxes_in_bag

    return hero_boxes


def recursive_search(container, type_):
    results = []

    try:
        content = container.content
    except AttributeError:
        return results

    for item in content:
        if isinstance(item, type_):
            results.append(item)
        results += recursive_search(item, type_)
    return results
