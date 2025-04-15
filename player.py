import random
from card import Card

class Player:
    def __init__(self):
        self.gold = 50
        self.animals = []
        self.food = []
        self.hand = self.draw_cards()

    def draw_cards(self):
        cards = [
            Card("Thu hoạch mùa", 7),
            Card("Lễ hội làng", 5),
            Card("Bán rau củ", 4),
            Card("Lao động", 6),
            Card("Bạn bè tặng quà", 3),
        ]
        return random.sample(cards, 3)
