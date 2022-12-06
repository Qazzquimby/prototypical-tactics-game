# These are to keep the interface of xlrd books, without needing to actually read filesystem


class FakeBook:
    def __init__(self, sheets: dict):
        self.sheets = {key: FakeSheet(sheet) for key, sheet in sheets.items()}

    def sheet_by_name(self, name):
        return self.sheets[name]

    def sheet_names(self):
        return list(self.sheets.keys())


class FakeSheet:
    def __init__(self, rows: list):
        self.rows = [[Cell(value) for value in row] for row in rows]

        # pad rows with empty cells
        max_len = max([len(row) for row in self.rows])
        for row in self.rows:
            while len(row) < max_len:
                row.append(Cell(""))

    def row_values(self, row):
        return self.rows[row]

    @property
    def nrows(self):
        return len(self.rows)

    @property
    def ncols(self):
        return len(self.rows[0])

    def cell(self, rowx, colx):
        return self.rows[rowx][colx]


class Cell:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Cell({self.value})"
