from domain.abstract import DomainEntity
from tts.guid import guid
from tts.transform import Transform
from tts.deck import Deck as TTSDeck


class Deck(DomainEntity):
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.imagePath = ""
        self.backImagePath = ""

    def as_dict(self, transform=None):
        if not transform:
            transform = Transform.from_size_and_coords(1)
        return {
            "Name": "DeckCustom",
            "Transform": transform.as_dict(),
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
                    "FaceURL": self.imagePath,
                    "BackURL": self.backImagePath,
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

    def to_tts(self):
        transform = Transform.from_size_and_coords(1)
        transform.rot_y = 180
        transform.rot_z = 180

        deck = TTSDeck(
            transform, self.name, self.cards, self.imagePath, self.backImagePath
        )
        return deck

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
                cards.append(card.as_dict())
        return cards

    def next_id(self):
        return len(self.cards) + 1
