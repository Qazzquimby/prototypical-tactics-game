from src.drawing.size_constants import CARD_SCALE, CARD_WIDTH, CARD_HEIGHT


def make_css():
    return f"""\
/*@import url('https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@300;400&family=Special+Elite&family=Yeseva+One&display=swap');*/
* {{
    font-family: Roboto Slab, sans-serif;
    padding: 0;
    margin: 0;
    box-sizing: border-box;
}}

.card {{
    display: flex;
    flex-flow: column;
    background-color: rgb(17, 12, 23);
    /* background image is set in html as it depends on self.image_url*/
    background-position: top 15% right 0;
    background-repeat: no-repeat;
    background-size: cover;

    font-size: {16 * CARD_SCALE}px;
    padding: 0.5em;
    margin: 0;
    color: white;
    border: {6 * CARD_SCALE}px solid black;

    width: {CARD_WIDTH}px;
    height: {CARD_HEIGHT}px;
    /*height: {CARD_HEIGHT - 37}px; sometimes fits better*/

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
    text-shadow: 0 0 4px black;
}}

.card-name {{
    font-family: Yeseva One, sans-serif;
    font-size: 1.6em;
}}

.stats {{
    align-self: flex-end;
}}

.image-box-OLD {{
    width: 70%;
    border: {2 * CARD_SCALE}px solid;
    border-radius: {5 * CARD_SCALE}px;
    background-color: #130f15;
    box-shadow: 0 0 {10 * CARD_SCALE}px;
    display: block;
    margin: auto;

    max-height: {130 * CARD_SCALE}px;
    object-fit: cover;
    /*contain*/
    object-position:top;
}}

.card-text {{
    color: black;
    background-color: rgba(210,202,205,0.8);
    border-radius: {5 * CARD_SCALE}px;
    box-shadow: 0 0 {3 * CARD_SCALE}px;
    border: {3 * CARD_SCALE}px solid rgba(158, 133, 120, 1);

    padding: {7 * CARD_SCALE}px {7 * CARD_SCALE}px 0 {7 * CARD_SCALE}px;
    margin-top: auto;
    text-align: justify;
    font-size: 0.85em;
}}

.owner {{
    font-family: Yeseva One, sans-serif;
    text-shadow: 0 0 4px black;
}}
"""
