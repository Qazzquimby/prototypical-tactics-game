from tts.abstract import TtsEntity
from tts.guid import guid


class Deck(TtsEntity):
    def __init__(self, transform, name, cards, image_path, back_image_path):
        self.transform = transform
        self.cards = cards
        self.name = name
        self.image_path = image_path
        self.back_image_path = back_image_path

    def get_ids(self):
        ids = []
        for card in self.cards:
            for _ in range(0, card.count):
                ids.append(99 + card.id)
        return ids

    def get_card_instances(self):
        cards = []
        for card in self.cards:
            for _ in range(0, card.count):
                cards.append(self.card_as_dict(card))
        return cards

    def card_as_dict(self, card):
        return {
            "Name": "Card",
            "Transform": self.transform.as_dict(),
            "Nickname": self.name,
            "Description": "",
            "ColorDiffuse": {"r": 0.713235259, "g": 0.713235259, "b": 0.713235259},
            "Locked": False,
            "Grid": True,
            "Snap": True,
            "Autoraise": True,
            "Sticky": True,
            "Tooltip": True,
            "GridProjection": False,
            "Hands": True,
            "CardID": 99 + card.id,
            "SidewaysCard": False,
            "LuaScript": "",
            "LuaScriptState": "",
            "ContainedObjects": [],
            "GUID": guid(),
        }

    def as_dict(self):
        return {
            "Name": "DeckCustom",
            "Transform": self.transform.as_dict(),
            "Nickname": "",
            "Description": "",
            "ColorDiffuse": {"r": 0.713235259, "g": 0.713235259, "b": 0.713235259},
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
