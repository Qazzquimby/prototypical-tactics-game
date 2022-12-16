from domain.complexObject import ComplexObject


def is_type_a_template(type_):
    return type_[0] == "\\"


class ComplexObjectParser:
    def __init__(self, types):
        self.types = types
        self.template_headers = {}

    def parse(self, sheet):
        complex_objects = []
        row = 1
        while row < sheet.nrows:
            name = sheet.cell(rowx=row, colx=0).value
            type_name = sheet.cell(rowx=row, colx=1).value
            if name or type_name:
                is_template = is_type_a_template(type_name)
                if is_template:
                    type_ = self.find_type(type_name)
                    content = {}
                    for column in type_.shape.areas:
                        if column >= 1000:
                            content[column] = sheet.cell(
                                rowx=row, colx=column - 1000
                            ).value
                    self.template_headers[type_.name] = content
                else:
                    type_ = self.find_type(type_name)
                    content = {}
                    for column in type_.shape.areas:
                        # headers...
                        if column < 1000:
                            content[column] = sheet.cell(rowx=row, colx=column).value
                        else:
                            try:
                                content[column] = self.template_headers[type_.name][
                                    column
                                ]
                            except KeyError:
                                raise ValueError(
                                    type_.name
                                    + " contains headers, but no template was defined for it."
                                )
                    complex_objects.append(ComplexObject(name, type_, content))
            row += 1
        return complex_objects

    def find_type(self, name):
        # handle the template column
        if name[0] == "\\":
            name = name[1:]

        for type_ in self.types:
            if type_.name == name:
                return type_
        raise ValueError(
            "The ComplexType `" + str(name) + "` does not exist."
        ) from None
