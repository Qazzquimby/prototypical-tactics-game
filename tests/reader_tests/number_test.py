import pytest

from reader.number import read_number
from reader.number import read_float


@pytest.mark.parametrize(
    "number, expected",
    [
        ("12", 12),
        ("1", 1),
        ("0", 0),
        ("99999", 99999),
    ],
)
def test_read_number(number, expected):
    assert read_number(number) == expected


@pytest.mark.parametrize(
    "bad_number",
    [
        "2.0",
        "2.5",
        "abc",
        "",
    ],
    ids=[
        "Floats are not supported",
        "Floats are not supported",
        "Text is not supported",
        "Blank is not supported",
    ],
)
def test_read_number_fails(bad_number):
    with pytest.raises(ValueError):
        read_number(bad_number)


@pytest.mark.parametrize(
    "number, expected",
    [
        ("1.5", 1.5),
        ("1.0", 1),
        ("3", 3),
    ],
)
def test_read_float(number, expected):
    assert read_float(number) == expected


@pytest.mark.parametrize(
    "bad_number",
    [
        "abc",
        "",
    ],
    ids=[
        "Text is not supported",
        "Blank is not supported",
    ],
)
def test_read_float_fails(bad_number):
    with pytest.raises(ValueError):
        read_float(bad_number)
