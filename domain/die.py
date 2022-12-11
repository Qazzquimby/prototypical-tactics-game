from domain.abstract import DomainEntity
from tts.transform import Transform
from tts.die import Die as TTSDie


class Die(DomainEntity):
    def __init__(self, name, color, size, sides, custom_content=None, image_path=None):
        self.name = name
        self.color = color
        self.size = size
        self.sides = sides
        self.custom_content = custom_content
        self.image_path = image_path

        if custom_content and sides != 6:
            raise ValueError("Only 6 sided dice support custom content at this time.")

        if sides not in (4, 6, 8, 10, 12, 20):
            raise ValueError("This number of dice-sides is not supported.")

    def to_tts(self):
        transform = Transform.from_size_and_coords(self.size)
        die = TTSDie(
            self.sides,
            self.color,
            transform,
            self.custom_content,
            self.image_path,
        )
        return die
