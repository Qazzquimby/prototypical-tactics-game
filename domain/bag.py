from functools import cached_property

from domain.abstract import DomainEntity
from domain.deck import Deck
from tts.guid import guid
from tts.transform import Transform


class Bag(DomainEntity):
    def __init__(self, name, size, color, is_infinite=False):
        self.name = name
        self.size = size
        self.color = color
        self.content = []
        self.is_infinite = is_infinite

    def add_content(self, amount, content):
        for _ in range(0, amount):
            self.content.append(content)

    @cached_property
    def transform(self):
        return Transform.from_size_and_coords(self.size)

    def as_dict(self, transform=None):
        return {
            "Name": "Infinite_Bag" if self.is_infinite else "Bag",
            "Transform": self.transform.as_dict(),
            "Nickname": self.name,
            "Description": "",
            "ColorDiffuse": {
                "r": self.color[0],
                "g": self.color[1],
                "b": self.color[2],
            },
            "Locked": False,
            "Grid": True,
            "Snap": True,
            "Autoraise": True,
            "Sticky": True,
            "Tooltip": True,
            "GridProjection": False,
            "Hands": False,
            "MaterialIndex": -1,
            "MeshIndex": -1,
            "LuaScript": "",
            "LuaScriptState": "",
            "ContainedObjects": [item.as_dict() for item in self.content],
            "GUID": guid(),
        }

    def get_decks(self):
        # recursively get decks from self and internal bags
        decks = []
        for item in self.content:
            if isinstance(item, Bag):
                decks += item.get_decks()
            elif isinstance(item, Deck):
                decks.append(item)
        return decks


class InfiniteBag(Bag):
    def add_content(self, amount, content):
        # depreciate infinite bags
        if len(self.content) == 1:
            raise ValueError(
                "There is no point to putting more than one thing in an Infinite bag."
            )
        self.content.append(content)
