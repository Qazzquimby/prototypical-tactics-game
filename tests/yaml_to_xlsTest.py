import pytest

from yaml_to_xls import (
    game_to_xls,
    DEFAULT_XLS,
    SheetNames,
    make_deck_name,
    Deck,
    UnitCard,
    Ability,
    parse_game,
    BASIC,
    HERO_CARD_LABEL,
    SPEED_LABEL,
    HEALTH_LABEL,
    Game,
    HeroBox,
    Hero,
    GameSet,
    make_box_name,
)

MY_TEST_CHAR_NAME = "My Test Char"
MY_TEST_CHAR_SPEED = 1
MY_TEST_CHAR_HEALTH = 2
MY_TEST_CHAR_SIZE = 3
MY_TEST_CHAR_HERO = Hero(
    name=MY_TEST_CHAR_NAME,
    speed=MY_TEST_CHAR_SPEED,
    health=MY_TEST_CHAR_HEALTH,
    size=MY_TEST_CHAR_SIZE,
)
MY_TEST_CHAR__NO_ABILITIES = HeroBox(hero=MY_TEST_CHAR_HERO, decks=[])

MY_ABILITY_NAME = "My Ability"
MY_ABILITY_COST = ""
MY_ABILITY_TEXT = "My Ability Text"
MY_ABILITY = Ability(name=MY_ABILITY_NAME, type=BASIC, text=MY_ABILITY_TEXT)
MY_TEST_CHAR__WITH_ABILITY = HeroBox(
    hero=MY_TEST_CHAR_HERO, decks=[Deck(abilities=[MY_ABILITY])]
)


def test_empty_file():
    decks = Game(sets=[])
    result = game_to_xls(decks)
    assert result == DEFAULT_XLS


def sets_to_xls(sets):
    return game_to_xls(Game(sets=sets))


def make_set(hero_boxes, name="set0"):
    return GameSet(name=name, hero_boxes=hero_boxes)


@pytest.mark.parametrize(
    "sheet_name",
    [
        SheetNames.COMPLEX_TYPES,
        SheetNames.SHAPES,
        SheetNames.COMPLEX_OBJECTS,
        SheetNames.TOKENS,
        SheetNames.DICE,
        SheetNames.PLACEMENT,
    ],
)
def test_single_character__irrelevant_sheets_unchanged(sheet_name):
    xls = sets_to_xls(
        [
            make_set(
                hero_boxes=[MY_TEST_CHAR__NO_ABILITIES],
            )
        ]
    )
    result_complex_types = xls[SheetNames.COMPLEX_TYPES]
    assert result_complex_types == DEFAULT_XLS[SheetNames.COMPLEX_TYPES]


HERO_COMPLEX_OBJECT_ROW = [
    MY_TEST_CHAR__NO_ABILITIES.hero.name,
    HERO_CARD_LABEL,
    MY_TEST_CHAR__NO_ABILITIES.hero.name,
    SPEED_LABEL,
    str(MY_TEST_CHAR_SPEED),
    HEALTH_LABEL,
    str(MY_TEST_CHAR_HEALTH),
    MY_TEST_CHAR__NO_ABILITIES.hero.name,
]


TEST_DEFAULT_XLS = DEFAULT_XLS.copy()


def test_single_empty_character__complex_objects__just_hero_added():
    xls = sets_to_xls([make_set(hero_boxes=[MY_TEST_CHAR__NO_ABILITIES])])
    result = xls[SheetNames.COMPLEX_OBJECTS]
    expected = TEST_DEFAULT_XLS[SheetNames.COMPLEX_OBJECTS] + [HERO_COMPLEX_OBJECT_ROW]
    assert result == expected


def test_single_empty_character__deck_added_to_bag():
    xls = sets_to_xls([make_set(hero_boxes=[MY_TEST_CHAR__NO_ABILITIES])])
    result = xls[SheetNames.CONTAINERS]

    expected = TEST_DEFAULT_XLS[SheetNames.CONTAINERS]
    expected[1].append("set0")
    expected.append(
        [
            make_box_name(MY_TEST_CHAR_NAME),
            "bag",
            "red",
            "1",
            make_deck_name(MY_TEST_CHAR_NAME),
        ]
    )
    expected.append(["set0", "bag", "black", "2", make_box_name(MY_TEST_CHAR_NAME)])

    assert result == expected


def test_character_abilities_created():
    xls = sets_to_xls([make_set(hero_boxes=[MY_TEST_CHAR__WITH_ABILITY])])
    result = xls[SheetNames.COMPLEX_OBJECTS]
    expected = TEST_DEFAULT_XLS[SheetNames.COMPLEX_OBJECTS]

    expected += [
        HERO_COMPLEX_OBJECT_ROW,
        [
            MY_ABILITY_NAME,
            "Ability",
            MY_ABILITY_NAME,
            BASIC,
            MY_ABILITY_COST,
            MY_ABILITY_TEXT,
            MY_TEST_CHAR_NAME,
        ],
    ]
    assert result == expected


def test_single_empty_character__deck__just_hero_added():
    xls = sets_to_xls([make_set(hero_boxes=[MY_TEST_CHAR__NO_ABILITIES])])
    result = xls[SheetNames.DECKS]
    expected = (
        TEST_DEFAULT_XLS[SheetNames.DECKS]
        + [["Deck", make_deck_name(MY_TEST_CHAR_NAME)]]
        + [[MY_TEST_CHAR__NO_ABILITIES.hero.name, "1"]]
    )

    assert result == expected


def test_single_character__deck__all_added():
    xls = sets_to_xls([make_set(hero_boxes=[MY_TEST_CHAR__WITH_ABILITY])])
    result = xls[SheetNames.DECKS]
    expected = (
        TEST_DEFAULT_XLS[SheetNames.DECKS]
        + [["Deck", make_deck_name(MY_TEST_CHAR_NAME)]]
        + [[MY_TEST_CHAR__NO_ABILITIES.hero.name, "1"]]
        + [
            [
                MY_ABILITY_NAME,
                "1",
            ]
        ]
    )
    assert result == expected


def test_parse_dict_to_models():
    game = {
        "decks": [
            {
                "hero": {
                    "name": "a",
                    "speed": 1,
                    "health": 2,
                    "size": 3,
                },
                "abilities": [
                    {"name": "a's ability", "type": BASIC, "text": "ability text"}
                ],
            }
        ]
    }

    result = parse_game(game)

    expected = Game(
        decks=[
            Deck(
                hero=UnitCard(name="a", speed=1, health=2, size=3),
                abilities=[
                    Ability(name="a's ability", type=BASIC, text="ability text")
                ],
            )
        ]
    )

    assert result == expected
