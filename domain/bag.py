from functools import cached_property
from typing import Optional

from domain.abstract import DomainEntity
from src.shared_types import IntroSetup
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
        self.lua_script = ""

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
            "LuaScript": self.lua_script,
            "LuaScriptState": "",
            "ContainedObjects": [
                item.as_dict() for item in self.contained_objects if item
            ],
            "GUID": guid(),
        }


class GameSetBag(Bag):
    def __init__(
        self,
        name,
        size,
        color,
        intro_setup: Optional[IntroSetup] = None,
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
        self.intro_set_setup = intro_setup

    def as_dict(self, transform=None):
        (
            setup_intro_game_on_load,
            setup_intro_game_deps,
        ) = self.make_setup_intro_game_button()

        self.lua_script = f"""\
        function onLoad()
            {setup_intro_game_on_load}
        end

        {setup_intro_game_deps}
        """

        # create floating title text
        # floating_text = {
        #     "GUID": guid(),
        #     "Name": "3DText",
        #     "Transform": {
        #         "posX": 120,
        #         "posY": 8,
        #         "posZ": z_pos,
        #         "rotX": 0.0,
        #         "rotY": 90.0,
        #         "rotZ": 0.0,
        #         "scaleX": 1.0,
        #         "scaleY": 1.0,
        #         "scaleZ": 1.0,
        #     },
        #     "Locked": True,
        #     "Text": {
        #         "Text": "\n".join(bag["Nickname"].split(" ")),
        #         "colorstate": {"r": 1.0, "g": 1.0, "b": 1.0},
        #         "fontSize": 64,
        #     },
        # }
        # tts_dict["ObjectStates"].append(floating_text)

        bag_dict = super().as_dict(transform)
        return bag_dict

    def make_setup_intro_game_button(self):
        if not self.intro_set_setup:
            return f"print('No intro set setup for {self.name}')", ""

        on_load = f"""\
        local params = {{
                click_function = 'setupIntroGame',
                function_owner = self,
                label = 'Intro Setup',
                position = {{2, 0.5, 0}},
                rotation = {{0, -90, 00}},
                scale = {{1.2, 1, 1.2}},
                width = 1500,
                height = 600,
                font_size = 250
            }}
            self.createButton(params)
        """

        deal_intro_hero_scripts = []
        for index, hero in enumerate(self.intro_set_setup.blue):
            deal_intro_hero_scripts.append(self.deal_intro_hero(hero, True, index))
        for index, hero in enumerate(self.intro_set_setup.red):
            deal_intro_hero_scripts.append(self.deal_intro_hero(hero, False, index))
        deal_intro_hero_scripts_string = "\n\n".join(deal_intro_hero_scripts)

        deps = f"""\
function setupIntroGame()
    print('Hello {self.name}')

    local contents = self.getData().ContainedObjects
    for _, bag in ipairs(contents) do
        if string.match(bag.Nickname, 'heroes') then
            {deal_intro_hero_scripts_string}
        end
        if string.match(bag.Nickname, 'maps') then
            for _, map in ipairs(bag.ContainedObjects) do
                if string.match(map.Nickname, '{self.intro_set_setup.map}') then
                    print("found map!")

                    local position = {{22, 0.5, 0}}
                    local rotation = {{0, 0, 0}}

                    spawnObjectData({{
                        data=map,
                        position=position,
                        rotation=rotation,
                        callback_function = function(spawned)
                            -- log('objToDeal ' .. logString(spawned))
                        end
                    }})
                end
            end
        end
    end                
end"""
        return on_load, deps

    def deal_intro_hero(self, hero_name: str, is_blue: bool, index: int):
        if is_blue:
            x_pos = 10 + index * 7
            z_pos = -8.5
            rot = 180
        else:
            x_pos = 35 - index * 7
            z_pos = 8.5
            rot = 0

        return f"""\
print('dealing {hero_name}')
for _, hero in ipairs(bag.ContainedObjects) do
    if string.match(hero.Nickname, '{hero_name}') then
        print("found!")

        local position = {{{x_pos}, 0.5, {z_pos}}}
        local rotation = {{0, {rot}, 0}}

        spawnObjectData({{
            data=hero,
            position=position,
            rotation=rotation,
            callback_function = function(spawned)
                -- log('objToDeal ' .. logString(spawned))
            end
        }})
    end
end"""


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
