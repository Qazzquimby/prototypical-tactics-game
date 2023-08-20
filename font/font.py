import pygame

from src.paths import data_dir


class Font:
    fonts = {}

    @staticmethod
    def get_font(size):
        if size not in Font.fonts:
            Font.fonts[size] = pygame.font.Font(str(data_dir/"proto.ttf"), size)
        return Font.fonts[size]
