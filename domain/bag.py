from tts.guid import guid
from tts.transform import Transform


class Bag:
    def __init__(self, name, size, color, is_infinite=False):
        self.name = name
        self.size = size
        self.color = color
        self.content = []
        self.is_infinite = is_infinite

    def addContent(self, amount, content):
        for i in range(0, amount):
            self.content.append(content)

    def as_dict(self, transform=None):
        if not transform:
            transform = Transform.from_size_and_coords(self.size)
        return {
            "Name": "Infinite_Bag" if self.is_infinite else "Bag",
            "Transform": transform.as_dict(),
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


class InfiniteBag(Bag):
    def addContent(self, amount, content):
        if len(self.content) == 1:
            raise ValueError(
                "There is no point to putting more than one thing in an Infinite bag."
            )
        self.content.append(content)
