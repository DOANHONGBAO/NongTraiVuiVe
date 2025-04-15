import pygame

class Card:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def draw(self, surface, x, y, font, color_bg, color_text, color_value):
        pygame.draw.rect(surface, color_bg, (x, y, 150, 80))
        text = font.render(self.name, True, color_text)
        value = font.render(f"+{self.value} vàng", True, color_value)
        surface.blit(text, (x + 10, y + 10))
        surface.blit(value, (x + 10, y + 40))
