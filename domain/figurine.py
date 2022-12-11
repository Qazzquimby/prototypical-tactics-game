from domain.abstract import DomainEntity
from tts.guid import guid
from tts.transform import Transform


class Figurine(DomainEntity):
    def __init__(self, name, size, image_path):
        self.name = name
        self.size = size
        self.image_path = image_path

    def as_dict(self, transform=None):
        if not transform:
            transform = Transform.from_size_and_coords(self.size)
        return {
            "Name": "Figurine_Custom",
            "Transform": transform.as_dict(),
            "Nickname": self.name.split(" figurine")[0],
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
            "CustomImage": {
                "ImageURL": self.image_path,
                "ImageSecondaryURL": "",
                "WidthScale": 0.0,
                "CustomToken": {
                    "Thickness": 0.1,
                    "MergeDistancePixels": 15.0,
                    "Stackable": False,
                },
            },
            "LuaScript": "",
            "LuaScriptState": "",
            "GUID": guid(),
        }
