import pygame


class Font:
    fonts = {}

    @staticmethod
    def get_font(size):
        if not size in Font.fonts:
            Font.fonts[size] = pygame.font.Font("data/proto.ttf", size)
        return Font.fonts[size]
