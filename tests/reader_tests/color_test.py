import pytest
from reader.color import ColorReader


@pytest.mark.parametrize(
    "color, expected",
    [
        ("red", (1, 0, 0)),
        ("#00ff00", (0, 1, 0)),
        ("#000099", (0, 0, 0.6)),
        ("#999900", (0.6, 0.6, 0)),
    ],
)
def test_color_reader(color, expected):
    assert ColorReader.read_color(color) == expected


@pytest.mark.parametrize("bad_color", ["123", "text", "]"])
def test_color_reader_rejects_invalid(bad_color):
    with pytest.raises(ValueError):
        ColorReader.read_color(bad_color)
