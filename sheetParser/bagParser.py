import math

from domain.bag import Bag, InfiniteBag

from reader.fromlist import read_fromlist
from reader.color import ColorReader
from reader.number import read_float
from reader.content import read_content


class BagParser:
    def __init__(self, types):
        self.types = types

    def parse(self, sheet):
        bags = []

        # bags can go in bags, which means types may not be defined and may fail on first pass.
        # I'm having it loop through the sheet until it makes no further progress on successive passes.
        last_num_rows_to_parse = math.inf
        rows_to_parse = list(range(1, sheet.nrows))
        while 0 < len(rows_to_parse) < last_num_rows_to_parse:
            last_num_rows_to_parse = len(rows_to_parse)
            new_bags, rows_to_parse = self.parse_rows(sheet, rows_to_parse)
            bags.extend(new_bags)
            self.types.extend(new_bags)
        return bags

    def parse_rows(self, sheet, rows: list[int]):
        bags = []
        rows_with_unknown_type = []
        for row in rows:
            try:
                bag = self.parse_row(sheet, row)
                bags.append(bag)
            except ValueError:
                rows_with_unknown_type.append(row)
        return bags, rows_with_unknown_type

    def parse_row(self, sheet, row):
        name = sheet.cell(rowx=row, colx=0).value
        type_name = read_fromlist(
            sheet.cell(rowx=row, colx=1).value, ("bag", "infinite-bag")
        )
        color = ColorReader.read_color(sheet.cell(rowx=row, colx=2).value)
        size = read_float(sheet.cell(rowx=row, colx=3).value)

        object_type = {"bag": Bag, "infinite-bag": InfiniteBag}[type_name]
        bag = object_type(name, size, color)

        content_num = 0
        while content_num < (sheet.ncols - 4):
            content = read_content(sheet.cell(rowx=row, colx=content_num + 4).value)
            for key, item in enumerate(content):
                bag.add_content(item[0], self.find_type(item[1]))
            content_num += 1
        return bag

    def find_type(self, name):
        for object_type in self.types:
            if object_type.name == name:
                return object_type
        raise ValueError("Unknown bag content: `" + str(name) + "`.") from None
