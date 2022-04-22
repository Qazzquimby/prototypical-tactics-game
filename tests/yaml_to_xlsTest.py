import pytest

from yaml_to_xls import structure_to_xls, DEFAULT_XLS, SheetNames

MY_TEST_CHAR_NAME = "My Test Char"

MY_TEST_CHAR = {"My Card": ["jeez idk"]}

MY_TEST_CHAR_STRUCTURE = {MY_TEST_CHAR_NAME: MY_TEST_CHAR}


def test_empty_file():
    yaml = {}
    result = structure_to_xls(yaml)
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
    result = structure_to_xls(MY_TEST_CHAR_STRUCTURE)[SheetNames.COMPLEX_TYPES]
    assert result == DEFAULT_XLS[SheetNames.COMPLEX_TYPES]


def test_single_character__shapes_types_unchanged():
    result = structure_to_xls(MY_TEST_CHAR_STRUCTURE)[SheetNames.COMPLEX_TYPES]
    assert result == DEFAULT_XLS[SheetNames.COMPLEX_TYPES]
