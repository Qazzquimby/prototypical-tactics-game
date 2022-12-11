from domain.abstract import DomainEntity
from tts.transform import Transform
from tts.board import Board as TTSBoard

class ComplexObject(DomainEntity):
    def __init__(self, name: str, type_, content):
        self.name = name
        self.type = type_
        self.content = content
        # only used if this is a board, not used if its a deck
        self.imagePath = ""

    def setImagePath(self, path):
        self.imagePath = path

    def to_tts(self):
        if self.type.type == "board":
            transform = Transform.from_size_and_coords(size=1)
            board = TTSBoard(transform, self)
            return board
        else:
            raise ValueError(
                "Only ComplexTypes of the 'board' type can be placed directly. The others go into a deck! (Tried placing a "
                + self.name
                + ")"
            )
