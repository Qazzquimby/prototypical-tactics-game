from domain.abstract import DomainEntity
from tts.simpletoken import SimpleToken
from tts.transform import Transform
from tts.token import Token as TTSToken

class Token(DomainEntity):
    def __init__(self, name, entity, color, size):
        self.name = name
        self.entity = entity
        self.color = color
        self.size = size

    def to_tts(self):
        transform = Transform.from_size_and_coords(self.size)
        bs = SimpleToken(self.entity, transform, self.color)
        return bs

class ContentToken(Token):
    def __init__(self, name, entity, bg_color, text_color, content, size, color):
        super().__init__(name, entity, color, size)
        self.bg_color = bg_color
        self.text_color = text_color
        self.content = content
        self.imagePath = ""

    def setImagePath(self, path):
        self.imagePath = path

    def to_tts(self):
        transform = Transform.from_size_and_coords(self.size)
        transform.rotY = 180
        bs = TTSToken(transform, self.imagePath)
        return bs