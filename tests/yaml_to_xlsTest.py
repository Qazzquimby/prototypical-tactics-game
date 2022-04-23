import pytest

from yaml_to_xls import decks_to_xls, DEFAULT_XLS, SheetNames, make_deck_name, Deck, Unit, Ability, parse_decks, BASIC, \
    HERO_CARD_LABEL, SPEED_LABEL, HEALTH_LABEL

MY_TEST_CHAR_NAME = "My Test Char"
MY_TEST_CHAR_SPEED = 1
MY_TEST_CHAR_HEALTH = 2
MY_TEST_CHAR_SIZE = 3
MY_TEST_CHAR_HERO = Unit(
    name=MY_TEST_CHAR_NAME,
    speed=MY_TEST_CHAR_SPEED,
    health=MY_TEST_CHAR_HEALTH,
    size=MY_TEST_CHAR_SIZE
)
MY_TEST_CHAR__NO_ABILITIES = Deck(
    hero=MY_TEST_CHAR_HERO,
    cards=[]
)

MY_ABILITY_NAME = "My Ability"
MY_ABILITY_COST = ""
MY_ABILITY_TEXT = "My Ability Text"
MY_ABILITY = Ability(name=MY_ABILITY_NAME, type=BASIC, text=MY_ABILITY_TEXT)
MY_TEST_CHAR__WITH_ABILITY = Deck(
    hero=MY_TEST_CHAR_HERO,
    cards=[MY_ABILITY]
)


def test_empty_file():
    decks = []
    result = decks_to_xls(decks)
    assert result == DEFAULT_XLS


@pytest.mark.parametrize("sheet_name", [
    SheetNames.COMPLEX_TYPES,
    SheetNames.SHAPES,
    SheetNames.COMPLEX_OBJECTS,
    SheetNames.TOKENS,
    SheetNames.DICE,
    SheetNames.PLACEMENT,
])
def test_single_character__irrelevant_sheets_unchanged(sheet_name):
    result = decks_to_xls([MY_TEST_CHAR__NO_ABILITIES])[SheetNames.COMPLEX_TYPES]
    assert result == DEFAULT_XLS[SheetNames.COMPLEX_TYPES]


def test_single_empty_character__deck__just_hero_added():
    result = decks_to_xls([MY_TEST_CHAR__NO_ABILITIES])[SheetNames.DECKS]
    expected = DEFAULT_XLS[SheetNames.DECKS] + [[
        "Deck", make_deck_name(MY_TEST_CHAR_NAME)
    ]] + [[
        MY_TEST_CHAR__NO_ABILITIES.hero.name, "1"
    ]]

    assert result == expected

HERO_COMPLEX_OBJECT_ROW = [
        HERO_CARD_LABEL, MY_TEST_CHAR__NO_ABILITIES.hero.name,
        SPEED_LABEL, str(MY_TEST_CHAR_SPEED),
        HEALTH_LABEL, str(MY_TEST_CHAR_HEALTH),
        MY_TEST_CHAR__NO_ABILITIES.hero.name
    ]

def test_single_empty_character__complex_objects__just_hero_added():
    result = decks_to_xls([MY_TEST_CHAR__NO_ABILITIES])[SheetNames.COMPLEX_OBJECTS]
    expected = DEFAULT_XLS[SheetNames.COMPLEX_OBJECTS] + [HERO_COMPLEX_OBJECT_ROW]

    assert result == expected


def test_single_empty_character__deck_added_to_bag():
    result = decks_to_xls([MY_TEST_CHAR__NO_ABILITIES])[SheetNames.CONTAINERS]
    expected = DEFAULT_XLS[SheetNames.CONTAINERS]
    expected[1].append(make_deck_name(MY_TEST_CHAR_NAME))
    assert result == expected



def test_character_abilities_created():
    result = decks_to_xls([MY_TEST_CHAR__WITH_ABILITY])[SheetNames.COMPLEX_OBJECTS]
    expected = DEFAULT_XLS[SheetNames.COMPLEX_OBJECTS]

    expected += [HERO_COMPLEX_OBJECT_ROW, ["Ability", MY_ABILITY_NAME, BASIC, MY_ABILITY_COST, MY_ABILITY_TEXT, MY_TEST_CHAR_NAME]]
    assert result == expected


def test_parse_dict_to_models():
    decks = [
        {"hero": {
            "name": "a",
            "speed": 1,
            "health": 2,
            "size": 3,
        },
            "cards": [
                {
                    "name": "a's ability",
                    "type": BASIC,
                    "text": "ability text"
                }
            ]
        }
    ]

    result = parse_decks(decks)

    expected = [
        Deck(
            hero=Unit(name="a", speed=1, health=2, size=3),
            cards=[
                Ability(name="a's ability", type=BASIC, text="ability text")
            ]
        )
    ]

    assert result == expected