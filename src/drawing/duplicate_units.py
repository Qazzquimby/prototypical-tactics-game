from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import matplotlib.font_manager


def duplicate_number_to_letter(duplicate_number: int) -> str:
    # 1->A, 2->B
    return chr(64 + duplicate_number)


def make_duplicate_image(original_image_url: str, duplicate_number: int) -> Image:
    response = requests.get(original_image_url)
    original_image = Image.open(BytesIO(response.content))

    font_family = matplotlib.font_manager
    font_filename = font_family.findFont(
        font_family.FontProperties(family="FreeMono", style="normal")
    ).fname
    font = ImageFont.truetype(font_filename, 40)

    image_transparent = Image.new("RGBA", original_image.size, (0, 0, 0, 0))

    draw = ImageDraw.Draw(image_transparent)

    # will hold image plus caption above
    duplicate_image = Image.new(
        "RGBA", (image_transparent.width, image_transparent.height + 50), (0, 0, 0, 0)
    )

    draw.text(
        (5, 5),
        text=duplicate_number_to_letter(duplicate_number),
        font=font,
        fill="black",
    )

    duplicate_image.paste(image_transparent, (0, 0))
    duplicate_image.paste(original_image, (0, 50))

    return duplicate_image
