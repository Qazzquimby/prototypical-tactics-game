from yaml_to_xls import yaml_to_xls


def test_empty_file():
    yaml = ""
    result = yaml_to_xls(yaml)
    assert result == {
        "ComplexTypes": [
            "NAME", "SIZE", "SHAPE - TOPLEFT", "SHAPE - BOTTOMRIGHT", "BG - COLOR", "BACKSIDE", "TYPE",
        ],
        "Shapes": [

        ],
        "ComplexObjects": [
            "NAME", "TYPE", "CONTENT?"
        ],
        "Decks": ["Deck"],
        "Containers":[
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

