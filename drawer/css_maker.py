from drawer.size_constants import CARD_SCALE, CARD_WIDTH, CARD_HEIGHT


def make_css():
    return f"""\
/*@import url('https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@300;400&family=Special+Elite&family=Yeseva+One&display=swap');*/
* {{
    font-family: Roboto Slab, sans-serif;
    font-size: {16*CARD_SCALE}px;
    padding: 0;
    margin: 0;
}}

.card {{
    display: flex;
    flex-flow: column;
    background-color: rgb(17, 12, 23);
    font-size: 1rem;

    padding: 5mm;
    color: white;
    border: {0*40*CARD_SCALE}px white;

    width: {CARD_WIDTH-37}px;
    /*300px;*/
    height: {CARD_HEIGHT-37}px;
    /*height: 400px;*/

    overflow: hidden;
}}

.card pre {{
    white-space: pre-wrap;
}}

.card .ability-name {{
    font-size: 1.2em;
    font-weight: bold;
    margin-top: 0.2em
}}

.card-title-bar {{
    display: flex;
    flex-flow: row;
    justify-content: space-between;
    width: 100%;
}}

.card-name {{
    font-family: Yeseva One, serif;
    font-size: 1.6rem;
}}

.stats {{
    align-self: flex-end;
}}

.image-box {{
    width: 70%;
    border: {3*CARD_SCALE}px solid;
    border-radius: {5*CARD_SCALE}px;
    background-color: #130f15;
    box-shadow: 0 0 {10*CARD_SCALE}px;
    display: block;
    margin: auto;

    max-height: {130*CARD_SCALE}px;
    object-fit: cover;
    /*contain*/
    object-position:top;
}}

.card-text {{
    color: black;
    background-color: #fbf7d5;
    border-radius: {5*CARD_SCALE}px;
    box-shadow: 0 0 {10*CARD_SCALE}px;
    border: 12px solid white;

    padding: {7*CARD_SCALE}px {7*CARD_SCALE}px 0 {7*CARD_SCALE}px;
    margin-top: {5*CARD_SCALE}px;
    height: 100%;
    text-align: justify;
}}

/*!*.description {{*!*/
/*!*    padding: 2mm 0;*!*/
/*!*    flex-grow: 1;*!*/
/*!*    font-size: 1rem;*!*/
/*!*    white-space: pre-wrap;*!*/
/*}}*/

.owner {{
    font-family: Yeseva One, serif;
}}
"""
