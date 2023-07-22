from domain.abstract import DomainEntity
from tts.guid import guid
from tts.transform import Transform


class Card(DomainEntity):
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
            "ColorDiffuse": {"r": 0, "g": 0, "b": 0},
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
            "LuaScript": self.object.content.get_lua(),
            "LuaScriptState": "",
            "ContainedObjects": [],
            "GUID": guid(),
        }


class LoneCard(Card):
    def __init__(self, obj):
        super().__init__(obj, 1, 100)
        self.image_path = ""

    def as_dict(self, transform=None):
        base_dict = super().as_dict(transform)
        base_dict["CustomDeck"] = {
            "1": {
                "FaceURL": self.image_path,
                "BackURL": self.image_path,
                "NumWidth": 1,
                "NumHeight": 1,
                "BackIsHidden": True,
                "UniqueBack": False,
                "Type": 0,
            }
        }
        return base_dict


class MapContainer(LoneCard):
    def __init__(self, obj, local_path: str):
        super().__init__(obj)
        self.local_path = local_path
        self.image_path = ""

        self.content = []

    def as_dict(self, transform=None):
        base_dict = super().as_dict(transform)
        base_dict["ContainedObjects"] = [item.as_dict() for item in self.content]
        return base_dict
