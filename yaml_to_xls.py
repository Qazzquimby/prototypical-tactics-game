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


def yaml_to_xls(yaml: str):
    data = {
        SheetNames.COMPLEX_TYPES: [
            "NAME", "SIZE", "SHAPE - TOPLEFT", "SHAPE - BOTTOMRIGHT", "BG - COLOR", "BACKSIDE", "TYPE",
        ],
        SheetNames.SHAPES: [

        ],
        SheetNames.COMPLEX_OBJECTS: [
            "NAME", "TYPE", "CONTENT?"
        ],
        "Decks": ["Deck"],
        SheetNames.CONTAINERS: [
            "NAME", "TYPE", "COLOR", "SIZE", "CONTENTS",
        ],
        "Tokens": [
            "NAME", "ENTITY", "COLOR", "SIZE", "TEXT-COLOR-FRONT", "CONTENT-FRONT",
        ],
        "Dice": [
            "NAME", "COLOR", "SIZE", "SIDES", "CONTENT?"
        ],
        "PLACEMENT": [],
    }

    return data
