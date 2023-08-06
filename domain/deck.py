from domain.abstract import DomainEntity
from domain.card import Card, LoneCard
from drawer.deckDrawer import DECK_IMAGE_CARDS_PER_ROW, DECK_IMAGE_CARDS_PER_COLUMN
from tts.guid import guid


class Deck(DomainEntity):
    def __init__(self, name):
        self.name = name
        self.cards: list[Card] = []
        self.image_path = ""
        self.back_image_path = ""

    @classmethod
    def from_cards(cls, name, cards: list[Card]):
        # if 0 cards, return None
        if len(cards) == 0:
            raise ValueError("Cannot create deck from 0 cards")
        if len(cards) == 1:
            return LoneCard(cards[0].object)

        deck = cls(name)
        deck.cards = cards
        return deck

    def as_dict(self):
        return {
            "Name": "DeckCustom",
            "Transform": self.transform.as_dict(),
            "Nickname": self.name,
            "Description": "",
            "ColorDiffuse": {"r": 0, "g": 0, "b": 0},
            "Locked": False,
            "Grid": True,
            "Snap": True,
            "Autoraise": True,
            "Sticky": True,
            "Tooltip": True,
            "GridProjection": False,
            "Hands": False,
            "SidewaysCard": False,
            "DeckIDs": self.get_ids(),
            "CustomDeck": {
                "1": {
                    "FaceURL": self.image_path,
                    "BackURL": self.back_image_path,
                    "NumWidth": DECK_IMAGE_CARDS_PER_ROW,
                    "NumHeight": DECK_IMAGE_CARDS_PER_COLUMN,
                    "BackIsHidden": False,
                    "UniqueBack": False,
                }
            },
            "LuaScript": "",
            "LuaScriptState": "",
            "ContainedObjects": self.get_card_instances(),
            "GUID": guid(),
        }

    def get_ids(self):
        ids = []
        for card in self.cards:
            for _ in range(0, card.count):
                ids.append(99 + card.id)
        return ids

    def get_card_instances(self):
        card_dicts = []
        for card in self.cards:
            for _ in range(0, card.count):
                card_dicts.append(card.as_dict())
        return card_dicts
