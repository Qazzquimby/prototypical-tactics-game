from domain.complexType import ComplexType
from domain.shape import Shape
from reader.color import ColorReader
from reader.cell import read_cell
from reader.dimensions import read_dimensions
from reader.fromlist import read_fromlist


class ComplexTypeParser:
    @staticmethod
    def parse(sheet, shape_sheet):
        complex_types = []
        row = 1
        while row < sheet.nrows:
            name = sheet.cell(rowx=row, colx=0).value
            try:
                size = read_dimensions(sheet.cell(rowx=row, colx=1).value)
            except ValueError as e:
                raise ValueError(
                    str(e) + "(while reading size for " + name + ")"
                ) from None

            try:
                top_left = read_cell(sheet.cell(rowx=row, colx=2).value)
                bottom_right = read_cell(sheet.cell(rowx=row, colx=3).value)
            except ValueError as e:
                raise ValueError(
                    str(e) + "(while reading shape for " + name + ")"
                ) from None

            try:
                shape = ComplexTypeParser.parse_shape(
                    shape_sheet, top_left, bottom_right
                )
            except ValueError as e:
                raise ValueError(
                    str(e) + " (while reading shape for " + name + ")"
                ) from None

            background_color = ColorReader.read_color(
                sheet.cell(rowx=row, colx=4).value
            )
            backside = ColorReader.read_color(sheet.cell(rowx=row, colx=5).value)
            try:
                type_ = read_fromlist(
                    sheet.cell(rowx=row, colx=6).value, ("card", "board")
                )
            except ValueError as e:
                raise ValueError(str(e) + " (while reading: " + name + ")") from None

            complex_types.append(
                ComplexType(name, size, shape, background_color, backside, type_)
            )
            row += 1
        return complex_types

    @staticmethod
    def parse_shape(shape_sheet, top_left, bottom_right):
        first_row = top_left[1]
        first_col = top_left[0]
        last_row = bottom_right[1]
        last_col = bottom_right[0]

        rows = []
        for row in range(first_row, last_row + 1):
            cols = []
            for col in range(first_col, last_col + 1):
                try:
                    cols.append(shape_sheet.cell(rowx=row, colx=col).value)
                except IndexError:
                    raise ValueError(
                        "Unable to parse a shape: it extends beyond the edge of the Shapes spreadsheet."
                    )
            rows.append(cols)

        size = (last_col - first_col + 1, last_row - first_row + 1)
        return ComplexTypeParser.construct_shape(size, rows)

    # construct a shape from the given rows of chars
    @staticmethod
    def construct_shape(size, rows):
        areas = {}
        for rowNum, row in enumerate(rows):
            for colNum, char in enumerate(row):
                ComplexTypeParser.validate_allowed(char, rowNum, colNum, areas)
                if char == 0.0:
                    continue
                if char in areas:
                    areas[char] = ComplexTypeParser.update_area(
                        areas[char], rowNum, colNum
                    )
                else:
                    areas[char] = (rowNum, colNum, rowNum, colNum)
        return Shape(size, ComplexTypeParser.reduce_names(areas))

    @staticmethod
    def validate_allowed(char, row_num: int, col_num: int, areas):
        if char in areas:
            if areas[char][1] > col_num:
                raise ValueError(
                    "Malformed Shape: trying to extend `"
                    + char
                    + "` to the left, that means this shape is not a rectangle!"
                )
            if col_num > areas[char][3] and areas[char][0] != areas[char][2]:
                raise ValueError(
                    "Malformed shape: trying to extend `"
                    + char
                    + "` to the right, but already on a second row. This shape is not a rectangle!"
                )
            if areas[char][2] + 1 < row_num:
                raise ValueError(
                    "Malformed shape: trying to extend `"
                    + char
                    + "` down by two rows at once. This shape is not a rectangle!"
                )
        for charKey, area in areas.items():
            if charKey != char:
                if row_num == area[2] and area[1] < col_num < area[3]:
                    raise ValueError(
                        "Malformed shape: a `"
                        + char
                        + "` is inside an area already claimed by `"
                        + charKey
                        + "`. This shape is not a rectangle!"
                    )
        return True

    # will expand the size of this area to include the new cell (if required)
    @staticmethod
    def update_area(current, row_num: int, col_num: int):
        if row_num > current[2]:
            current = (current[0], current[1], row_num, current[3])
        if col_num > current[3]:
            current = (current[0], current[1], current[2], col_num)
        return current

    @staticmethod
    def reduce_names(areas):
        new_areas = {}
        for char, area in areas.items():
            new_areas[ComplexTypeParser.reduce_char(char)] = area
        return new_areas

    @staticmethod
    def reduce_char(chars):
        value = 0
        is_header = False
        for char in chars:
            if char == "\\":
                is_header = True
                continue
            value *= 26
            value += ord(char.lower()) - 96

        if is_header:
            value = value + 1000
        # because 'c' is 0, a and b are reserved, and areas start from 0, but a=1
        return value - 1
