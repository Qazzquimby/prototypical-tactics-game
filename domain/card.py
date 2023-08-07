from domain.abstract import DomainEntity
from tts.guid import guid
from tts.transform import Transform


class Card(DomainEntity):
    def __init__(self, obj, count, id_):
        self._id = id_
        self.count = count
        self.object = obj
        self.image_path = ""
        self.back_image_path = "https://gamepedia.cursecdn.com/mtgsalvation_gamepedia/f/f8/Magic_card_back.jpg?version=0ddc8d41c3b69c2c3c4bb5d72669ffd7"

    def as_dict(self, transform=None):
        if not transform:
            transform = Transform.from_size_and_coords(1)
        return {
            "Name": "Card",
            "Transform": transform.as_dict(),
            "Nickname": self.object.content.name,
            "Description": "",
            "ColorDiffuse": {"r": 0, "g": 0, "b": 0},
            "LayoutGroupSortIndex": 0,
            "Value": 0,
            "Locked": False,
            "Grid": True,
            "Snap": True,
            "Autoraise": True,
            "Sticky": True,
            "Tooltip": True,
            "GridProjection": False,
            "Hands": True,
            "CardID": self.get_id(),
            "SidewaysCard": False,
            "LuaScript": self.object.content.get_lua(),
            "LuaScriptState": "",
            "ContainedObjects": [],
            "CustomDeck": {self._id: self.get_custom_deck_dict()},
            "GUID": guid(),
        }

    def get_custom_deck_dict(self):
        return {
            "FaceURL": self.image_path,
            "BackURL": self.back_image_path,
            "NumWidth": 1,
            "NumHeight": 1,
            "BackIsHidden": True,
            "UniqueBack": False,
            "Type": 0,
        }

    def get_id(self):
        return 100 * self._id


class LoneCard(Card):
    def __init__(self, obj):
        super().__init__(obj, 1, 1)

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


class DomainMap(LoneCard):
    def __init__(self, obj, local_path: str):
        super().__init__(obj)
        self.local_path = local_path

    def as_dict(self, transform=None):
        if transform is None:
            transform = Transform.from_size_and_coords(3)  # scale up map
        base_dict = super().as_dict(transform)
        return base_dict
