from domain.abstract import DomainEntity
from domain.card import Card
from tts.guid import guid


class Deck(DomainEntity):
    def __init__(self, name):
        self.name = name
        self.cards: list[Card] = []
        self.image_path = ""
        self.back_image_path = ""

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
                    "NumWidth": 10,
                    "NumHeight": 7,
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

    def next_id(self):
        return len(self.cards) + 1
