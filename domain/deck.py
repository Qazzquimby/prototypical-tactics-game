from tts.guid import guid
from tts.transform import Transform


class Deck:
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

    def get_ids(self):
        ids = []
        for card in self.cards:
            for i in range(0, card.count):
                ids.append(99 + card.id)
        return ids

    def get_card_instances(self):
        cards = []
        for card in self.cards:
            for i in range(0, card.count):
                cards.append(card.as_dict())
        return cards

    def addCard(self, card):
        self.cards.append(card)

    def nextId(self):
        return len(self.cards) + 1

    def setImagePath(self, path):
        self.imagePath = path

    def setBackImagePath(self, path):
        self.backImagePath = path
