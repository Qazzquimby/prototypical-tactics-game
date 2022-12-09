import pytest

from reader.content import read_content


@pytest.mark.parametrize(
    "text, expected",
    [
        ("5xitem", [(5, "item")]),
        ("5xitem;2xother_item", [(5, "item"), (2, "other_item")]),
        ("item", [(1, "item")]),
        ("something;otherthing", [(1, "something"), (1, "otherthing")]),
        ("itemxitem", [(1, "itemxitem")]),
    ],
)
def test_content_reader(text, expected):
    assert read_content(text) == expected
