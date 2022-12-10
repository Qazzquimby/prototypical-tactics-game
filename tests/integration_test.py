from yaml_to_xls import (
    GameSet,
    HeroBox,
    Deck,
    Ability,
    BASIC,
    Hero,
)

import json
from pathlib import Path

import pygame
import yaml

from core import sheets_to_tts_json
from image_builders import ImagesDirImageBuilder
from tts.fake_xls_books import FakeBook
from yaml_to_xls import Game, game_to_sheets

BASIC_GAME = Game(
    sets=[
        GameSet(
            name="TestSet",
            hero_boxes=[
                HeroBox(
                    hero=Hero(name="TestHero", speed=3, health=8),
                    image="TestImage",
                    decks=[
                        Deck(
                            abilities=[
                                Ability(
                                    name="TestAbility",
                                    type=BASIC,
                                    text="TestText",
                                )
                            ]
                        )
                    ],
                )
            ],
        )
    ]
)


def test_basic_char():
    game = BASIC_GAME
    tts_dict = game_to_tts_dict(game)
    expected_dict = json.loads(EXPECTED_TTS_JSON, strict=False)

    deep_clean(tts_dict)
    deep_clean(expected_dict)

    assert tts_dict == expected_dict


def deep_clean(tts_dict: dict) -> dict:
    # search deep for any nondeterministic key and delete it
    for key, value in list(tts_dict.items()):
        if key in ("Transform", "GUID"):
            del tts_dict[key]
        elif isinstance(value, dict):
            tts_dict[key] = deep_clean(value)
        elif isinstance(tts_dict[key], list):
            for item in tts_dict[key]:
                if isinstance(item, dict):
                    tts_dict[key] = deep_clean(item)
    return tts_dict


yaml_string = """\
sets:
  - name: TestSet
    hero_boxes:
      - hero:
          name: TestHero
          health: 8
          speed: 3
        image: TestImage
        decks:
          - abilities:
            - name: TestAbility
              text: |-
                TestAbilityText
"""


EXPECTED_TTS_JSON = r"""{
  "SaveName": "TestGame",
  "GameMode": "Custom",
  "Date": "10/19/2017 10:24:32 PM",
  "Table": "Table_RPG",
  "Sky": "Sky_Regal",
  "Note": "",
  "Rules": "",
  "LuaScript": "--[[ Lua code. See documentation: http://berserk-games.com/knowledgebase/scripting/ --]]\n\n--[[ The onLoad event is called after the game save finishes loading. --]]\nfunction onLoad()\n    --[[ print('onLoad!') --]]\nend\n\n--[[ The onUpdate event is called once per frame. --]]\nfunction onUpdate ()\n    --[[ print('onUpdate loop!') --]]\nend",
  "LuaScriptState": "",
  "Grid": {
    "Type": 0,
    "Lines": false,
    "Color": {
      "r": 0.0,
      "g": 0.0,
      "b": 0.0
    },
    "Opacity": 0.75,
    "ThickLines": false,
    "Snapping": false,
    "Offset": false,
    "BothSnapping": false,
    "xSize": 2.0,
    "ySize": 2.0,
    "PosOffset": {
      "x": 0.0,
      "y": 1.0,
      "z": 0.0
    }
  },
  "Lighting": {
    "LightIntensity": 0.54,
    "LightColor": {
      "r": 1.0,
      "g": 0.9804,
      "b": 0.8902
    },
    "AmbientIntensity": 1.3,
    "AmbientType": 0,
    "AmbientSkyColor": {
      "r": 0.5,
      "g": 0.5,
      "b": 0.5
    },
    "AmbientEquatorColor": {
      "r": 0.5,
      "g": 0.5,
      "b": 0.5
    },
    "AmbientGroundColor": {
      "r": 0.5,
      "g": 0.5,
      "b": 0.5
    },
    "ReflectionIntensity": 1.0,
    "LutIndex": 0,
    "LutContribution": 1.0
  },
  "Hands": {
    "Enable": true,
    "DisableUnused": false,
    "Hiding": 0,
    "HandTransforms": [
      {
        "Color": "Red",
        "Transform": {
          "posX": -15.1108065,
          "posY": 4.81034231,
          "posZ": -20.1076221,
          "rotX": 0.0,
          "rotY": 0.0,
          "rotZ": 0.0,
          "scaleX": 11.7725115,
          "scaleY": 9.174497,
          "scaleZ": 4.87123871
        }
      },
      {
        "Color": "Yellow",
        "Transform": {
          "posX": -30.2150211,
          "posY": 4.81034231,
          "posZ": 10.17524,
          "rotX": 0.0,
          "rotY": 90.0,
          "rotZ": 0.0,
          "scaleX": 11.6590471,
          "scaleY": 9.174497,
          "scaleZ": 4.921982
        }
      },
      {
        "Color": "Purple",
        "Transform": {
          "posX": 30.25128,
          "posY": 4.81034231,
          "posZ": 9.59069252,
          "rotX": 0.0,
          "rotY": 270.0,
          "rotZ": 0.0,
          "scaleX": 11.6590395,
          "scaleY": 9.174497,
          "scaleZ": 4.921982
        }
      },
      {
        "Color": "Blue",
        "Transform": {
          "posX": 15.4749184,
          "posY": 4.81034231,
          "posZ": 19.8365288,
          "rotX": 0.0,
          "rotY": 179.8,
          "rotZ": 0.0,
          "scaleX": 11.7760649,
          "scaleY": 9.174497,
          "scaleZ": 4.87342262
        }
      },
      {
        "Color": "White",
        "Transform": {
          "posX": 15.1961479,
          "posY": 4.81034231,
          "posZ": -20.1400986,
          "rotX": 0.0,
          "rotY": 0.0,
          "rotZ": 0.0,
          "scaleX": 11.7725019,
          "scaleY": 9.17449951,
          "scaleZ": 4.87123871
        }
      },
      {
        "Color": "Green",
        "Transform": {
          "posX": -15.1927767,
          "posY": 4.81034231,
          "posZ": 19.787817,
          "rotX": 0.0,
          "rotY": 180.0,
          "rotZ": 0.0,
          "scaleX": 11.7725019,
          "scaleY": 9.174497,
          "scaleZ": 4.87123871
        }
      },
      {
        "Color": "Pink",
        "Transform": {
          "posX": 30.10358,
          "posY": 4.81034231,
          "posZ": -8.449126,
          "rotX": 0.0,
          "rotY": 270.0,
          "rotZ": 0.0,
          "scaleX": 11.6590366,
          "scaleY": 9.174497,
          "scaleZ": 4.921982
        }
      },
      {
        "Color": "Orange",
        "Transform": {
          "posX": -30.247818,
          "posY": 4.81034231,
          "posZ": -8.822588,
          "rotX": 0.0,
          "rotY": 90.0,
          "rotZ": 0.0,
          "scaleX": 11.6590509,
          "scaleY": 9.174497,
          "scaleZ": 4.921982
        }
      }
    ]
  },
  "Turns": {
    "Enable": false,
    "Type": 0,
    "TurnOrder": [],
    "Reverse": false,
    "SkipEmpty": false,
    "DisableInteractions": false,
    "PassTurns": true
  },
  "DrawImage": "iVBORw0KGgoAAAANSUhEUgAAAWAAAADQCAYAAAA53LuNAAAFFElEQVR4Ae3QgQAAAADDoPlTH+SFUGHAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgy8DQx5DAABHyNK3wAAAABJRU5ErkJggg==",
  "VectorLines": [],
  "ObjectStates": [
    {
      "Name": "Bag",
      "Transform": {
        "posX": -26.44366819300996,
        "posY": 1,
        "posZ": -6.311935646677911,
        "rotX": 0,
        "rotY": 0,
        "rotZ": 0,
        "scaleX": 3.0,
        "scaleY": 3.0,
        "scaleZ": 3.0
      },
      "Nickname": "Sets",
      "Description": "",
      "ColorDiffuse": {
        "r": 1.0,
        "g": 1.0,
        "b": 1.0
      },
      "Locked": false,
      "Grid": true,
      "Snap": true,
      "Autoraise": true,
      "Sticky": true,
      "Tooltip": true,
      "GridProjection": false,
      "Hands": false,
      "MaterialIndex": -1,
      "MeshIndex": -1,
      "LuaScript": "",
      "LuaScriptState": "",
      "ContainedObjects": [
        {
          "Name": "Bag",
          "Transform": {
            "posX": -26.44366819300996,
            "posY": 1,
            "posZ": -6.311935646677911,
            "rotX": 0,
            "rotY": 0,
            "rotZ": 0,
            "scaleX": 2.0,
            "scaleY": 2.0,
            "scaleZ": 2.0
          },
          "Nickname": "TestSet",
          "Description": "",
          "ColorDiffuse": {
            "r": 0.0,
            "g": 0.0,
            "b": 0.0
          },
          "Locked": false,
          "Grid": true,
          "Snap": true,
          "Autoraise": true,
          "Sticky": true,
          "Tooltip": true,
          "GridProjection": false,
          "Hands": false,
          "MaterialIndex": -1,
          "MeshIndex": -1,
          "LuaScript": "",
          "LuaScriptState": "",
          "ContainedObjects": [
            {
              "Name": "Bag",
              "Transform": {
                "posX": -26.44366819300996,
                "posY": 1,
                "posZ": -6.311935646677911,
                "rotX": 0,
                "rotY": 0,
                "rotZ": 0,
                "scaleX": 1.0,
                "scaleY": 1.0,
                "scaleZ": 1.0
              },
              "Nickname": "TestHero box",
              "Description": "",
              "ColorDiffuse": {
                "r": 1.0,
                "g": 0.0,
                "b": 0.0
              },
              "Locked": false,
              "Grid": true,
              "Snap": true,
              "Autoraise": true,
              "Sticky": true,
              "Tooltip": true,
              "GridProjection": false,
              "Hands": false,
              "MaterialIndex": -1,
              "MeshIndex": -1,
              "LuaScript": "",
              "LuaScriptState": "",
              "ContainedObjects": [
                {
                  "Name": "Figurine_Custom",
                  "Transform": {
                    "posX": -26.44366819300996,
                    "posY": 2,
                    "posZ": -6.311935646677911,
                    "rotX": 0,
                    "rotY": 180,
                    "rotZ": 0,
                    "scaleX": 1.0,
                    "scaleY": 1.0,
                    "scaleZ": 1.0
                  },
                  "Nickname": "TestHero",
                  "Description": "",
                  "ColorDiffuse": {
                    "r": 0.713235259,
                    "g": 0.713235259,
                    "b": 0.713235259
                  },
                  "Locked": false,
                  "Grid": true,
                  "Snap": true,
                  "Autoraise": true,
                  "Sticky": true,
                  "Tooltip": true,
                  "GridProjection": false,
                  "Hands": false,
                  "CustomImage": {
                    "ImageURL": "TestImage",
                    "ImageSecondaryURL": "",
                    "WidthScale": 0.0,
                    "CustomToken": {
                      "Thickness": 0.1,
                      "MergeDistancePixels": 15.0,
                      "Stackable": false
                    }
                  },
                  "LuaScript": "",
                  "LuaScriptState": "",
                  "GUID": "f91f9242f9cd4bdfb7f922e5515e268e"
                },
                {
                  "Name": "DeckCustom",
                  "Transform": {
                    "posX": -26.44366819300996,
                    "posY": 2,
                    "posZ": -6.311935646677911,
                    "rotX": 0,
                    "rotY": 180,
                    "rotZ": 180,
                    "scaleX": 1,
                    "scaleY": 1,
                    "scaleZ": 1
                  },
                  "Nickname": "",
                  "Description": "",
                  "ColorDiffuse": {
                    "r": 0.713235259,
                    "g": 0.713235259,
                    "b": 0.713235259
                  },
                  "Locked": false,
                  "Grid": true,
                  "Snap": true,
                  "Autoraise": true,
                  "Sticky": true,
                  "Tooltip": true,
                  "GridProjection": false,
                  "Hands": false,
                  "SidewaysCard": false,
                  "DeckIDs": [
                    100,
                    101
                  ],
                  "CustomDeck": {
                    "1": {
                      "FaceURL": "file:///D:\\Users\\User\\PycharmProjects\\prototypical-tactics-game\\data\\images\\TestHero deck.jpg",
                      "BackURL": "file:///D:\\Users\\User\\PycharmProjects\\prototypical-tactics-game\\data\\images\\TestHero deck_back.jpg",
                      "NumWidth": 10,
                      "NumHeight": 7,
                      "BackIsHidden": false,
                      "UniqueBack": false
                    }
                  },
                  "LuaScript": "",
                  "LuaScriptState": "",
                  "ContainedObjects": [
                    {
                      "Name": "Card",
                      "Transform": {
                        "posX": -26.44366819300996,
                        "posY": 2,
                        "posZ": -6.311935646677911,
                        "rotX": 0,
                        "rotY": 180,
                        "rotZ": 180,
                        "scaleX": 1,
                        "scaleY": 1,
                        "scaleZ": 1
                      },
                      "Nickname": "TestHero deck",
                      "Description": "",
                      "ColorDiffuse": {
                        "r": 0.713235259,
                        "g": 0.713235259,
                        "b": 0.713235259
                      },
                      "Locked": false,
                      "Grid": true,
                      "Snap": true,
                      "Autoraise": true,
                      "Sticky": true,
                      "Tooltip": true,
                      "GridProjection": false,
                      "Hands": true,
                      "CardID": 100,
                      "SidewaysCard": false,
                      "LuaScript": "",
                      "LuaScriptState": "",
                      "ContainedObjects": [],
                      "GUID": "65022a8523bf4a25a6843434aab52adc"
                    },
                    {
                      "Name": "Card",
                      "Transform": {
                        "posX": -26.44366819300996,
                        "posY": 2,
                        "posZ": -6.311935646677911,
                        "rotX": 0,
                        "rotY": 180,
                        "rotZ": 180,
                        "scaleX": 1,
                        "scaleY": 1,
                        "scaleZ": 1
                      },
                      "Nickname": "TestHero deck",
                      "Description": "",
                      "ColorDiffuse": {
                        "r": 0.713235259,
                        "g": 0.713235259,
                        "b": 0.713235259
                      },
                      "Locked": false,
                      "Grid": true,
                      "Snap": true,
                      "Autoraise": true,
                      "Sticky": true,
                      "Tooltip": true,
                      "GridProjection": false,
                      "Hands": true,
                      "CardID": 101,
                      "SidewaysCard": false,
                      "LuaScript": "",
                      "LuaScriptState": "",
                      "ContainedObjects": [],
                      "GUID": "cc4fdbe5c2204bb88f2a93ef5599a19e"
                    }
                  ],
                  "GUID": "3d24fb8208af4ded9056341822537cb4"
                }
              ],
              "GUID": "ad35131f68c8447aae400c8af4d7b659"
            }
          ],
          "GUID": "10b4dd0364bc43f2ba9a256c8d08850b"
        }
      ],
      "GUID": "b022636c1d5e4be7b9cbd104eb5b9c90"
    }
  ],
  "DecalPallet": [],
  "TabStates": {
    "0": {
      "title": "Rules",
      "body": "",
      "color": "Grey",
      "visibleColor": {
        "r": 0.5,
        "g": 0.5,
        "b": 0.5
      },
      "id": 0
    },
    "1": {
      "title": "White",
      "body": "",
      "color": "White",
      "visibleColor": {
        "r": 1.0,
        "g": 1.0,
        "b": 1.0
      },
      "id": 1
    },
    "2": {
      "title": "Brown",
      "body": "",
      "color": "Brown",
      "visibleColor": {
        "r": 0.443,
        "g": 0.231,
        "b": 0.09
      },
      "id": 2
    },
    "3": {
      "title": "Red",
      "body": "",
      "color": "Red",
      "visibleColor": {
        "r": 0.856,
        "g": 0.1,
        "b": 0.094
      },
      "id": 3
    },
    "4": {
      "title": "Orange",
      "body": "",
      "color": "Orange",
      "visibleColor": {
        "r": 0.956,
        "g": 0.392,
        "b": 0.113
      },
      "id": 4
    },
    "5": {
      "title": "Yellow",
      "body": "",
      "color": "Yellow",
      "visibleColor": {
        "r": 0.905,
        "g": 0.898,
        "b": 0.172
      },
      "id": 5
    },
    "6": {
      "title": "Green",
      "body": "",
      "color": "Green",
      "visibleColor": {
        "r": 0.192,
        "g": 0.701,
        "b": 0.168
      },
      "id": 6
    },
    "7": {
      "title": "Blue",
      "body": "",
      "color": "Blue",
      "visibleColor": {
        "r": 0.118,
        "g": 0.53,
        "b": 1.0
      },
      "id": 7
    },
    "8": {
      "title": "Teal",
      "body": "",
      "color": "Teal",
      "visibleColor": {
        "r": 0.129,
        "g": 0.694,
        "b": 0.607
      },
      "id": 8
    },
    "9": {
      "title": "Purple",
      "body": "",
      "color": "Purple",
      "visibleColor": {
        "r": 0.627,
        "g": 0.125,
        "b": 0.941
      },
      "id": 9
    },
    "10": {
      "title": "Pink",
      "body": "",
      "color": "Pink",
      "visibleColor": {
        "r": 0.96,
        "g": 0.439,
        "b": 0.807
      },
      "id": 10
    },
    "11": {
      "title": "Black",
      "body": "",
      "color": "Black",
      "visibleColor": {
        "r": 0.25,
        "g": 0.25,
        "b": 0.25
      },
      "id": 11
    }
  },
  "VersionNumber": "v9.9"
}"""

data_dir = Path("data").absolute()


def game_to_tts_dict(game: Game) -> dict:
    sheets = game_to_sheets(game)
    fake_book = FakeBook(sheets)
    tts_dict = sheets_to_tts_json(
        sheets=fake_book.sheets,
        image_builder=ImagesDirImageBuilder(pygame, basePath=data_dir / "images"),
        file_name="TestGame",
    )
    return tts_dict


if __name__ == "__main__":
    generate_new_expected = False

    if generate_new_expected:
        # This generates the expected tts json, for use if the expectations change
        yaml_content = yaml.safe_load(yaml_string)
        game = Game.parse_obj(yaml_content)
        tts_dict = game_to_tts_dict(game)
        out = json.dumps(tts_dict, indent=2)
        print(tts_dict)
        print("done")
