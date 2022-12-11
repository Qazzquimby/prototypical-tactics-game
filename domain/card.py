from tts.guid import guid
from tts.transform import Transform


class Card:
    def __init__(self, obj, count, id_):
        self.id = id_
        self.count = count
        self.object = obj

    def as_dict(self, transform=None):
        if not transform:
            transform = Transform.from_size_and_coords(1)
        return {
            "Name": "Card",
            "Transform": transform.as_dict(),
            "Nickname": self.object.name,
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
            "CardID": 99 + self.id,
            "SidewaysCard": False,
            "LuaScript": "",
            "LuaScriptState": "",
            "ContainedObjects": [],
            "GUID": guid(),
        }