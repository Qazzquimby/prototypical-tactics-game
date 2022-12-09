import pytest
from sheetParser.complexTypeParser import ComplexTypeParser


@pytest.mark.parametrize(
    "char, row_num, col_num, areas",
    [
        ("a", 0, 0, {}),
        ("a", 0, 1, {"b": (0, 0, 0, 0)}),
        ("a", 0, 1, {"a": (0, 0, 0, 0)}),
        ("a", 1, 0, {"a": (0, 0, 0, 0)}),
        ("\\c", 0, 0, {}),
    ],
    ids=[
        "Any char should be allowed in the top left corner",
        "A new char can follow a different one",
        "The same char can follow on the next cell",
        "The same char can follow on the next line",
        "A backlash column should be allowed",
    ],
)
def test_valid_input(char, row_num, col_num, areas):
    ComplexTypeParser.validateAllowed(char, row_num, col_num, areas)


@pytest.mark.parametrize(
    "char, row_num, col_num, areas",
    [
        ("a", 1, 1, {"a": (0, 2, 0, 4)}),
        ("a", 2, 0, {"a": (0, 0, 0, 4)}),
        ("e", 1, 1, {"a": (0, 0, 1, 2)}),
    ],
    ids=[
        "Should not be possible for a char to be more left than its bounding box.",
        "Should not be possible for a char to skip a row.",
        "Should not be possible for the wrong char to be inside another area.",
    ],
)
def test_invalid_input(char, row_num, col_num, areas):
    with pytest.raises(ValueError):
        ComplexTypeParser.validateAllowed(char, row_num, col_num, areas)
