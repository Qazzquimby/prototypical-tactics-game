from functools import cached_property

from domain.abstract import DomainEntity
from tts.guid import guid
from tts.transform import Transform


class Die(DomainEntity):
    def __init__(self, name, color, size, sides, custom_content=None, image_path=None):
        self.name = name
        self.color = color
        self.size = size
        self.sides = sides
        self.custom_content = custom_content
        self.image_path = image_path

        if custom_content and sides != 6:
            raise ValueError("Only 6 sided dice support custom content at this time.")

        if sides not in (4, 6, 8, 10, 12, 20):
            raise ValueError("This number of dice-sides is not supported.")

    @cached_property
    def transform(self):
        return Transform.from_size_and_coords(self.size)

    def as_dict(self):
        base = {
            "name": self.name(),
            "Transform": self.transform.as_dict(),
            "Nickname": "",
            "Description": "",
            "ColorDiffuse": {
                "r": self.color[0.0],
                "g": self.color[1.0],
                "b": self.color[2.0],
            },
            "Locked": False,
            "Grid": False,
            "Snap": False,
            "Autoraise": True,
            "Sticky": True,
            "Tooltip": True,
            "GridProjection": False,
            "Hands": False,
            "MaterialIndex": 0,
            "LuaScript": "",
            "LuaScriptState": "",
            "GUID": guid(),
            "RotationValues": self.get_rot_values(),
        }
        if self.custom_content:
            base["CustomImage"] = self.custom_dice()

        return base

    def name(self):
        if self.custom_content:
            return "Custom_Dice"
        return "Die_" + str(int(self.sides))

    def custom_dice(self):
        return {
            "ImageURL": self.image_path,
            "ImageSecondaryURL": "",
            "WidthScale": 0.0,
            "CustomDice": {"Type": 1},
        }

    def get_rot_values(self):
        if self.custom_content:
            return self.get_rot_values_custom()
        if self.sides == 4:
            return ROT_VALUES_4
        if self.sides == 6:
            return ROT_VALUES_6
        if self.sides == 8:
            return ROT_VALUES_8
        if self.sides == 12:
            return ROT_VALUES_12
        if self.sides == 20:
            return ROT_VALUES_20

    def get_rot_values_custom(self):
        return [
            {
                "Value": self.custom_content[0],
                "Rotation": {"x": -90.0, "y": 0.0, "z": 0.0},
            },
            {
                "Value": self.custom_content[1],
                "Rotation": {"x": 0.0, "y": 0.0, "z": 0.0},
            },
            {
                "Value": self.custom_content[2],
                "Rotation": {"x": 0.0, "y": 0.0, "z": -90.0},
            },
            {
                "Value": self.custom_content[3],
                "Rotation": {"x": 0.0, "y": 0.0, "z": 90.0},
            },
            {
                "Value": self.custom_content[4],
                "Rotation": {"x": 0.0, "y": 0.0, "z": -180.0},
            },
            {
                "Value": self.custom_content[5],
                "Rotation": {"x": 90.0, "y": 0.0, "z": 0.0},
            },
        ]


ROT_VALUES_4 = [
    {"Value": 1, "Rotation": {"x": 18.0, "y": -241.0, "z": -120.0}},
    {"Value": 2, "Rotation": {"x": -90.0, "y": -60.0, "z": 0.0}},
    {"Value": 3, "Rotation": {"x": 18.0, "y": -121.0, "z": 0.0}},
    {"Value": 4, "Rotation": {"x": 18.0, "y": 0.0, "z": -240.0}},
]

ROT_VALUES_6 = [
    {"Value": 1, "Rotation": {"x": -90.0, "y": 0.0, "z": 0.0}},
    {"Value": 2, "Rotation": {"x": 0.0, "y": 0.0, "z": 0.0}},
    {"Value": 3, "Rotation": {"x": 0.0, "y": 0.0, "z": -90.0}},
    {"Value": 4, "Rotation": {"x": 0.0, "y": 0.0, "z": 90.0}},
    {"Value": 5, "Rotation": {"x": 0.0, "y": 0.0, "z": -180.0}},
    {"Value": 6, "Rotation": {"x": 90.0, "y": 0.0, "z": 0.0}},
]

ROT_VALUES_8 = [
    {"Value": 1, "Rotation": {"x": -33.0, "y": 0.0, "z": 90.0}},
    {"Value": 2, "Rotation": {"x": -33.0, "y": 0.0, "z": 180.0}},
    {"Value": 3, "Rotation": {"x": 33.0, "y": 180.0, "z": -180.0}},
    {"Value": 4, "Rotation": {"x": 33.0, "y": 180.0, "z": 90.0}},
    {"Value": 5, "Rotation": {"x": 33.0, "y": 180.0, "z": -90.0}},
    {"Value": 6, "Rotation": {"x": 33.0, "y": 180.0, "z": 0.0}},
    {"Value": 7, "Rotation": {"x": -33.0, "y": 0.0, "z": 0.0}},
    {"Value": 8, "Rotation": {"x": -33.0, "y": 0.0, "z": -90.0}},
]


ROT_VALUES_10 = [
    {"Value": 1, "Rotation": {"x": -38.0, "y": 0.0, "z": 234.0}},
    {"Value": 2, "Rotation": {"x": 38.0, "y": 180.0, "z": -233.0}},
    {"Value": 3, "Rotation": {"x": -38.0, "y": 0.0, "z": 20.0}},
    {"Value": 4, "Rotation": {"x": 38.0, "y": 180.0, "z": -17.0}},
    {"Value": 5, "Rotation": {"x": -38.0, "y": 0.0, "z": 90.0}},
    {"Value": 6, "Rotation": {"x": 38.0, "y": 180.0, "z": -161.0}},
    {"Value": 7, "Rotation": {"x": -38.0, "y": 0.0, "z": 307.0}},
    {"Value": 8, "Rotation": {"x": 38.0, "y": 180.0, "z": -304.0}},
    {"Value": 9, "Rotation": {"x": -38.0, "y": 0.0, "z": 163.0}},
    {"Value": 10, "Rotation": {"x": 38.0, "y": 180.0, "z": -90.0}},
]


ROT_VALUES_12 = [
    {"Value": 1, "Rotation": {"x": 27.0, "y": 0.0, "z": 72.0}},
    {"Value": 2, "Rotation": {"x": 27.0, "y": 0.0, "z": 144.0}},
    {"Value": 3, "Rotation": {"x": 27.0, "y": 0.0, "z": -72.0}},
    {"Value": 4, "Rotation": {"x": -27.0, "y": 180.0, "z": 180.0}},
    {"Value": 5, "Rotation": {"x": 90.0, "y": 180.0, "z": 0.0}},
    {"Value": 6, "Rotation": {"x": 27.0, "y": 0.0, "z": -144.0}},
    {"Value": 7, "Rotation": {"x": -27.0, "y": 180.0, "z": 36.0}},
    {"Value": 8, "Rotation": {"x": -90.0, "y": 180.0, "z": 0.0}},
    {"Value": 9, "Rotation": {"x": 27.0, "y": 0.0, "z": 0.0}},
    {"Value": 10, "Rotation": {"x": -27.0, "y": 180.0, "z": 108.0}},
    {"Value": 11, "Rotation": {"x": -27.0, "y": 108.0, "z": -36.0}},
    {"Value": 12, "Rotation": {"x": -27.0, "y": 36.0, "z": -108.0}},
]


ROT_VALUES_20 = [
    {"Value": 1, "Rotation": {"x": -11.0, "y": 60.0, "z": 17.0}},
    {"Value": 2, "Rotation": {"x": 52.0, "y": -60.0, "z": -17.0}},
    {"Value": 3, "Rotation": {"x": -11.0, "y": -180.0, "z": 90.0}},
    {"Value": 4, "Rotation": {"x": -11.0, "y": -180.0, "z": 162.0}},
    {"Value": 5, "Rotation": {"x": -11.0, "y": -60.0, "z": 234.0}},
    {"Value": 6, "Rotation": {"x": -11.0, "y": -180.0, "z": 306.0}},
    {"Value": 7, "Rotation": {"x": 52.0, "y": -60.0, "z": 55.0}},
    {"Value": 8, "Rotation": {"x": 52.0, "y": -60.0, "z": 198.0}},
    {"Value": 9, "Rotation": {"x": 52.0, "y": -60.0, "z": 127.0}},
    {"Value": 10, "Rotation": {"x": 52.0, "y": -180.0, "z": -90.0}},
    {"Value": 11, "Rotation": {"x": 308.0, "y": 0.0, "z": 90.0}},
    {"Value": 12, "Rotation": {"x": 306.0, "y": -240.0, "z": -52.0}},
    {"Value": 13, "Rotation": {"x": -52.0, "y": -240.0, "z": 18.0}},
    {"Value": 14, "Rotation": {"x": 307.0, "y": 120.0, "z": 233.0}},
    {"Value": 15, "Rotation": {"x": 11.0, "y": 120.0, "z": -234.0}},
    {"Value": 16, "Rotation": {"x": 11.0, "y": 0.0, "z": 54.0}},
    {"Value": 17, "Rotation": {"x": 11.0, "y": -120.0, "z": -17.0}},
    {"Value": 18, "Rotation": {"x": 11.0, "y": 0.0, "z": -90.0}},
    {"Value": 19, "Rotation": {"x": -52.0, "y": -240.0, "z": -198.0}},
    {"Value": 20, "Rotation": {"x": 11.0, "y": 0.0, "z": -162.0}},
]
