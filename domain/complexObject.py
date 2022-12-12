from domain.abstract import DomainEntity
from tts.guid import guid


class ComplexObject(DomainEntity):
    def __init__(self, name: str, type_, content):
        self.name = name
        self.type = type_
        self.content = content
        # only used if this is a board, not used if it's a deck
        self.image_path = ""

    def as_dict(self):
        # assumes this is a board
        return {
            "Name": "Custom_Board",
            "Transform": self.transform.as_dict(),
            "Nickname": "",
            "Description": "",
            "ColorDiffuse": {"r": 0.7867647, "g": 0.7867647, "b": 0.7867647},
            "Locked": True,
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
                "WidthScale": 1.42857146,
            },
            "LuaScript": "",
            "LuaScriptState": "",
            "GUID": guid(),
        }
