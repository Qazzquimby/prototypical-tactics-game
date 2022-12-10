class Library:
    def __init__(self, tokens, dice, complex_objects, decks, bags):
        self.tokens = tokens
        self.dice = dice
        self.complex_objects = complex_objects
        self.decks = decks
        self.bags = bags

    def all(self):
        return self.tokens + self.dice + self.complex_objects + self.decks + self.bags
