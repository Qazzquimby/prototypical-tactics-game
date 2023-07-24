from functools import cached_property

from domain.abstract import DomainEntity
from domain.deck import Deck
from tts.guid import guid
from tts.transform import Transform


class Bag(DomainEntity):
    def __init__(self, name, size, color, is_infinite=False, description=""):
        self.name = name
        self.description = description
        self.size = size
        self.color = color
        self.contained_objects = []
        self.is_infinite = is_infinite

    def add_content(self, amount, content):
        for _ in range(0, amount):
            self.contained_objects.append(content)

    @cached_property
    def transform(self):
        return Transform.from_size_and_coords(self.size)

    def as_dict(self, transform=None):
        return {
            "Name": "Infinite_Bag" if self.is_infinite else "Bag",
            "Transform": self.transform.as_dict(),
            "Nickname": self.name,
            "Description": self.description,
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
            "ContainedObjects": [item.as_dict() for item in self.contained_objects],
            "GUID": guid(),
        }


BOX_MESH_URL = "http://cloud-3.steamusercontent.com/ugc/1469815240708973394/DA07673D2A5C47A5544D2024B92585069B40EE91/"


class CustomBag(Bag):
    def __init__(
        self,
        name,
        size,
        color,
        diffuse_url,
        mesh_url=BOX_MESH_URL,
        is_infinite=False,
        description="",
    ):
        super().__init__(
            name=name,
            size=size,
            color=color,
            is_infinite=is_infinite,
            description=description,
        )
        self.mesh_url = mesh_url
        self.diffuse_url = diffuse_url

    def as_dict(self, transform=None):
        bag_dict = super().as_dict(transform)
        bag_dict["Name"] = "Custom_Model_Bag"
        bag_dict["CustomMesh"] = {
            "MeshURL": self.mesh_url,
            "DiffuseURL": self.diffuse_url,
            # "http://cloud-3.steamusercontent.com/ugc/1469815174066637129/930D22149972BB2B9C6164FB8D1819249640546B/",
            "NormalURL": "",
            "ColliderURL": "",
            "Convex": True,
            "MaterialIndex": 3,
            "TypeIndex": 6,
            "CustomShader": {
                "SpecularColor": {"r": 1.0, "g": 1.0, "b": 1.0},
                "SpecularIntensity": 0.0,
                "SpecularSharpness": 2.0,
                "FresnelStrength": 0.0,
            },
            "CastShadows": True,
        }
        return bag_dict
