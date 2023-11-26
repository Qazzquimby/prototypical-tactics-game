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
        on_loads = []
        deps = []

        for func in [
            self.make_setup_intro_game_button,
            self.make_floating_text,
            self.copy_rules_deck,
        ]:
            on_load, dep = func()
            on_loads.append(on_load)
            deps.append(dep)

        on_load_string = "\n\n".join(on_loads)
        deps_string = "\n\n".join(deps)

        self.lua_script = f"""\
        function onLoad()
            {on_load_string}
        end

        {deps_string}
        """

        bag_dict = super().as_dict(transform)
        return bag_dict

    def make_setup_intro_game_button(self):
        if not self.intro_set_setup:
            return "", ""
            # return f"print('No intro set setup for {self.name}')", ""

        on_load = f"""\
        local buttonParams = {{
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
        self.createButton(buttonParams)
        """

        deal_intro_hero_scripts = []
        for index, hero in enumerate(self.intro_set_setup.blue):
            deal_intro_hero_scripts.append(self.deal_intro_hero(hero, True, index))
        for index, hero in enumerate(self.intro_set_setup.red):
            deal_intro_hero_scripts.append(self.deal_intro_hero(hero, False, index))
        deal_intro_hero_scripts_string = "\n\n".join(deal_intro_hero_scripts)

        deps = f"""\
function setupIntroGame()
    print('Setting up {self.name} intro')

    local contents = self.getData().ContainedObjects
    for _, bag in ipairs(contents) do
        if string.match(bag.Nickname, 'heroes') then
            {deal_intro_hero_scripts_string}
        end
        if string.match(bag.Nickname, 'maps') then
            for _, map in ipairs(bag.ContainedObjects) do
                if string.match(map.Nickname, "{self.intro_set_setup.map}") then
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

    def copy_rules_deck(self):
        on_load = f"""\
        -- copy rules deck onto table
        local contents = self.getData().ContainedObjects
        for _, content in ipairs(contents) do
            if string.match(content.Nickname, 'rules') then
                
                local x = self.getPosition().x - 4
                local y = self.getPosition().y + 0.5
                local z = self.getPosition().z
                
                local rules_deck_params = {{
                    position={{x, y, z}},
                    rotation={{0, -90, 00}},
                    data=content
                }}
                spawnObjectData(rules_deck_params)
            end
        end
        """
        return on_load, ""

    def make_floating_text(self):
        name_string = "\n".join(self.name.split(" "))

        on_load = f"""\
        local x = self.getPosition().x
        local y = self.getPosition().y + 6
        local z = self.getPosition().z
        
        local floatingTextParams = {{
            type="3DText",
            position = {{x, y, z}},
            rotation = {{0, 90, 0}},
        }}
        local spawnedText = spawnObject(floatingTextParams)
        spawnedText.TextTool.setValue([[{name_string}]])
        """

        return on_load, ""

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
print("dealing {hero_name}")
for _, hero in ipairs(bag.ContainedObjects) do
    if string.match(hero.Nickname, "{hero_name}") then
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
