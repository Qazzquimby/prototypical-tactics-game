from domain.figurine import Figurine
from reader.number import read_float


class FigurineParser:
    @staticmethod
    def parse(sheet):
        figurines = []
        row = 1
        while row < sheet.nrows:
            name = sheet.cell(rowx=row, colx=0).value
            size = read_float(sheet.cell(rowx=row, colx=1).value)
            image_path = sheet.cell(rowx=row, colx=2).value
            figurine = Figurine(name=name, size=size, image_path=image_path)

            figurines.append(figurine)
            row += 1
        return figurines
