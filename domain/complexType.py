class ComplexType:
    def __init__(
        self,
        name,
        size,
        type_,
        background_color=(1.0, 1.0, 1.0),
        backside=(0.0, 0.0, 0.0),
    ):
        self.name = name
        self.size = size
        self.background_color = background_color
        self.backside = backside
        self.type = type_
