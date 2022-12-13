import pygame

from drawer.base import BaseDrawer
from font.font import Font

# 2,4,5
# 1,3,6 (1 and 6 are upside down)

# main image: 2048x2048

WIDTH = 500
HEIGHT = 500

DRAWSPOTS = [
    (71, 1462, True),  # 1
    (71, 767, False),  # 2
    (771, 1462, False),  # 3
    (771, 767, False),  # 4
    (1462, 767, False),  # 5
    (1462, 1462, True),  # 6
]


class DiceDrawer(BaseDrawer):
    def __init__(self, die):
        self.die = die
        self.large_font_obj = Font.get_font(256)
        self.smallFontObj = Font.get_font(96)

    def draw(self, _=None):
        # draws self, so doesn't need object parameter
        surf = pygame.image.load("data/D6.png")
        for pos, spot in enumerate(DRAWSPOTS):
            content = self.die.custom_content[pos]
            if isinstance(content, float) and content.is_integer():
                content = int(content)
            content = str(content)

            if len(content) > 2:
                text = self.smallFontObj.render(
                    str(content), True, (0, 0, 0), (255, 255, 255)
                )
            else:
                text = self.large_font_obj.render(
                    str(content), True, (0, 0, 0), (255, 255, 255)
                )
            rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))

            draw_surf = pygame.Surface((WIDTH, HEIGHT))
            draw_surf.fill((255, 255, 255))
            draw_surf.blit(text, rect)

            if spot[2]:  # should be upside down
                draw_surf = pygame.transform.rotate(draw_surf, 180)

            surf.blit(draw_surf, (spot[0], spot[1]))
        return surf
