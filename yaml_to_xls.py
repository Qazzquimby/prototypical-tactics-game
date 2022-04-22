import dataclasses
from pathlib import Path
import pyexcel

data_path = Path(r"data/")


@dataclasses.dataclass
class Sheet:
    pass


class SheetNames:
    COMPLEX_TYPES = "ComplexTypes"
    SHAPES = "Shapes"
    COMPLEX_OBJECTS = "ComplexObjects"
    CONTAINERS = "Containers"


DEFAULT_XLS = {
    SheetNames.COMPLEX_TYPES: [
        ["NAME", "SIZE", "SHAPE - TOPLEFT", "SHAPE - BOTTOMRIGHT", "BG - COLOR", "BACKSIDE", "TYPE", ],
        ["Board", "3000x2500", "A1", "G5", "Brown", "White", "board", ],
        ["HeroCard", "500x500", "A12", "D17", "White", "Black", "card", ],
        ["Ability", "500x500", "A19", "D24", "White", "Black", "card", ],
        ["Field", "500x500", "A19", "D24", "White", "Black", "card", ],
        ["Status", "500x500", "A19", "D24", "White", "Black", "card", ],

    ],
    SheetNames.SHAPES: [
        ["c", "d", "e", "f", "g", "h", "I", ],
        ["j", "k", "l", "m", "n", "o", "p", ],
        ["q", "r", "s", "t", "u", "v", "w", ],
        ["x", "y", "z", "aa", "ab", "ac", "ad", ],
        ["ae", "af", "ag", "ah", "aj", "ak", "al", ],

        ["c", "c", "c", "c", ],
        ["d", "e", "0", "0", ],
        ["f", "g", "0", "0", ],  # Hero cards
        ["h", "I", "0", "0", ],
        ["0", "0", "0", "0", ],
        ["0", "0", "0", "0", ],
        ["c", "c", "c", "d", ],  # Ability cards
        ["e", "e", "e", "e", ],
        ["f", "f", "f", "f", ],
        ["f", "f", "f", "f", ],
        ["f", "f", "f", "f", ],
        ["0", "g", "g", "0", ],

    ],
    SheetNames.COMPLEX_OBJECTS: [
        ["NAME", "TYPE", "CONTENT?"],
        ["GameBoard", "Board"],
    ],
    "Decks": [["Deck"]],
    SheetNames.CONTAINERS: [
        ["NAME", "TYPE", "COLOR", "SIZE", "CONTENTS", ]
    ],
    "Tokens": [
        ["NAME", "ENTITY", "COLOR", "SIZE", "TEXT-COLOR-FRONT", "CONTENT-FRONT", ],
        ["Team1Pawn", "Pawn", "Red", "1"],
        ["Team2Pawn", "Pawn", "Blue", "1"]
    ],
    "Dice": [
        ["NAME", "COLOR", "SIZE", "SIDES", "CONTENT?"],
        ["HealthDie", "white", "1", "6"]
    ],
    "PLACEMENT": [
        ["", "", "", "", "Characters"]
    ],
}


def structure_to_xls(yaml: dict):
    data = DEFAULT_XLS

    return data
