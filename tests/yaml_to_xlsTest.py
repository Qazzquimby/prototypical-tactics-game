import pytest

from yaml_to_xls import decks_to_xls, DEFAULT_XLS, SheetNames, make_deck_name, Deck, Unit, Ability, parse_decks

MY_TEST_CHAR_NAME = "My Test Char"

MY_TEST_CHAR = {"My Card": ["jeez idk"]}

MY_TEST_CHAR_STRUCTURE = {MY_TEST_CHAR_NAME: MY_TEST_CHAR}


def test_empty_file():
    yaml = {}
    result = decks_to_xls(yaml)
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
    result = decks_to_xls(MY_TEST_CHAR_STRUCTURE)[SheetNames.COMPLEX_TYPES]
    assert result == DEFAULT_XLS[SheetNames.COMPLEX_TYPES]


def test_single_empty_character__empty_deck_added():
    result = decks_to_xls({MY_TEST_CHAR_NAME: {}})[SheetNames.DECKS]
    expected = DEFAULT_XLS[SheetNames.DECKS] + [[
        "Deck", make_deck_name(MY_TEST_CHAR_NAME)
    ]]

    assert result == expected


def test_single_empty_character__deck_added_to_bag():
    result = decks_to_xls({MY_TEST_CHAR_NAME: {}})[SheetNames.CONTAINERS]
    expected = DEFAULT_XLS[SheetNames.CONTAINERS]
    expected[1].append(make_deck_name(MY_TEST_CHAR_NAME))
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
                    "type": "Basic",
                    "text": "ability text"
                }
            ]
        }
    ]

    result = parse_decks(decks)

    expected = [Deck(hero=Unit(name="a", speed=1, health=2, size=3),
                     cards=[Ability(name="a's ability", type="Basic", text="ability text")])]

    assert result == expected
