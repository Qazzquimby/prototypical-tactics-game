from functools import cached_property

from domain.abstract import DomainEntity
from tts.guid import guid
from tts.transform import Transform


class Token(DomainEntity):
    def __init__(self, name, entity, color, size):
        self.name = name
        self.entity = entity
        self.color = color
        self.size = size

    @cached_property
    def transform(self):
        return Transform.from_size_and_coords(self.size)

    def as_dict(self):
        return {
            "Name": self.get_tts_name(),
            "Transform": self.transform.as_dict(),
            "Nickname": "",
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
            "LuaScript": "",
            "LuaScriptState": "",
            "GUID": guid(),
        }


class ContentToken(Token):
    def __init__(self, name, entity, bg_color, text_color, content, size, color):
        super().__init__(name, entity, color, size)
        self.bg_color = bg_color
        self.text_color = text_color
        self.content = content
        self.image_path = ""

    def as_dict(self):
        return {
            "Name": "Custom_Token",
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
