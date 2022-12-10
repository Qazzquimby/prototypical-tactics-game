class ComplexObject:
    def __init__(self, name: str, type_, content):
        self.name = name
        self.type = type_
        self.content = content
        # only used if this is a board, not used if its a deck
        self.imagePath = ""

    def setImagePath(self, path):
        self.imagePath = path
