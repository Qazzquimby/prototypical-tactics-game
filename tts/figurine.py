from domain.figurine import Figurine as DomainFigurine
from tts.guid import guid


class Figurine:
    def __init__(self, transform, entity: DomainFigurine):
        self.transform = transform
        self.entity = entity

    def as_dict(self):
        print("depreciated")
        return {
            "Name": "Figurine_Custom",
            "Transform": self.transform.as_dict(),
            "Nickname": self.entity.name.split(" figurine")[0],
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
                "ImageURL": self.entity.image_path,
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
