from functools import cached_property

from domain.abstract import DomainEntity
from tts.guid import guid
from tts.transform import Transform


class Die(DomainEntity):
    def __init__(self, name, color, size, sides, custom_content=None, image_path=None):
        self.name = name
        self.color = color
        self.size = size
        self.sides = sides
        self.custom_content = custom_content
        self.image_path = image_path

        if custom_content and sides != 6:
            raise ValueError("Only 6 sided dice support custom content at this time.")

        if sides not in (4, 6, 8, 10, 12, 20):
            raise ValueError("This number of dice-sides is not supported.")

    @cached_property
    def transform(self):
        return Transform.from_size_and_coords(self.size)

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
