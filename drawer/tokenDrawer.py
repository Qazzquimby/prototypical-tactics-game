import pygame

from drawer.base import BaseDrawer
from drawer.color import convert_tts_to_pygame
from font.font import Font

MARGIN = 10


class TokenDrawer(BaseDrawer):
    def __init__(self, token):
        self.token = token
        self.fontObj = Font.get_font(32)

    def draw(self, _=None):
        # draws self, so doesn't need object parameter
        content = self.token.content
        if isinstance(content, float) and content.is_integer():
            content = int(content)

        text = self.fontObj.render(
            str(content),
            True,
            convert_tts_to_pygame(self.token.text_color),
            convert_tts_to_pygame(self.token.bg_color),
        )
        rect = text.get_rect()
        surf = pygame.Surface((rect[2] + 2 * MARGIN, rect[3] + 2 * MARGIN))
        surf.fill(convert_tts_to_pygame(self.token.bg_color))

        surf.blit(text, (MARGIN, MARGIN))
        return surf
