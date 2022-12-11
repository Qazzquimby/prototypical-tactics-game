from tts.guid import guid


class Bag:
    def __init__(self, transform, color, name, content, is_infinite=False):
        self.transform = transform
        self.content = content
        self.name = name
        self.color = color
        self.isInfinite = is_infinite

    def contentItems(self):
        contentItems = []
        for item in self.content:
            contentItems.append(item.as_dict())
        return contentItems

    def as_dict(self):
        print("deprecated")
        return {
            "Name": "Infinite_Bag" if self.isInfinite else "Bag",
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
            "ContainedObjects": self.contentItems(),
            "GUID": guid(),
        }
