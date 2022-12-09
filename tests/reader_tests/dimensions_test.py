import pytest

from reader.dimensions import read_dimensions

assert read_dimensions("200x300") == (200, 300)
assert read_dimensions("1x1") == (1, 1)
assert read_dimensions("1500x1200") == (1500, 1200)


@pytest.mark.parametrize(
    "text, expected",
    [
        ("200x300", (200, 300)),
        ("1x1", (1, 1)),
        ("1500x1200", (1500, 1200)),
    ],
)
def test_read_dimensions(text, expected):
    assert read_dimensions(text) == expected


@pytest.mark.parametrize(
    "text",
    ["0x100", "-100x100", "100x-100", "100", "100n50", "text", "100x", "x100"],
    ids=[
        "Zero should not be allowed",
        "Negatives should not be allowed",
        "Negatives should not be allowed",
        "An x should be required",
        "An x should be required",
        "Both sides should be numbers.",
        "Both sides should exist.",
        "Both sides should exist.",
    ],
)
def test_invalid_dimensions(text):
    with pytest.raises(ValueError):
        read_dimensions(text)
