from domain.abstract import DomainEntity
from domain.card import Card, LoneCard
from tts.guid import guid


class Deck(DomainEntity):
    def __init__(self, name, set_name):
        self.name = name
        self.cards: list[Card] = []
        self.set_name = set_name

    @classmethod
    def from_cards(cls, set_name: str, name: str, cards: list[Card]):
        # if 0 cards, return None
        if len(cards) == 0:
            raise ValueError("Cannot create deck from 0 cards")
        if len(cards) == 1:
            return LoneCard(cards[0].object)

        deck = cls(set_name=set_name, name=name)
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
            "CustomDeck": self.get_custom_deck_dict(),
            "LuaScript": "",
            "LuaScriptState": "",
            "ContainedObjects": self.get_card_instances(),
            "GUID": guid(),
        }

    def get_ids(self):
        ids = []
        for card in self.cards:
            for _ in range(0, card.count):
                ids.append(card.get_id_for_values())
        return ids

    def get_custom_deck_dict(self):
        custom_deck_dict = {}
        for card in self.cards:
            custom_deck_dict[card.id_for_keys] = card.get_custom_deck_dict()
        return custom_deck_dict

    def get_card_instances(self):
        card_dicts = []
        for card in self.cards:
            for _ in range(0, card.count):
                card_dicts.append(card.as_dict())
        return card_dicts
