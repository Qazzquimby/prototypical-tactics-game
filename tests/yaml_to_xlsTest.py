from yaml_to_xls import structure_to_xls, DEFAULT_XLS, SheetNames

MY_TEST_CHAR_NAME = "My Test Char"

def test_empty_file():
    yaml = {}
    result = structure_to_xls(yaml)
    assert result == DEFAULT_XLS

def test_single_empty_character__complex_types_unchanged():
    structure = {
        MY_TEST_CHAR_NAME: []

    }
    result = structure_to_xls(structure)[SheetNames.COMPLEX_TYPES]
    assert result == DEFAULT_XLS[SheetNames.COMPLEX_TYPES]