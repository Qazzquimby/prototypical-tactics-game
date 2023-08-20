from drawer.base import BaseDrawer
from src.drawing.card_drawer import CardDrawer


class LoneCardDrawer(BaseDrawer):
    def __init__(self, config):
        self.config = config

    async def draw(self, card):
        card_drawer = CardDrawer(card.object, self.config)
        return await card_drawer.draw()
