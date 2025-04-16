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
    def draw(self, surface, x, y, font, border_color, text_color, highlight_color, bg_image=None):
        if bg_image:
            surface.blit(bg_image, (x, y))
        else:
            pygame.draw.rect(surface, border_color, (x, y, 300, 150))  # fallback

        # Vẽ nội dung bài
        name_text = font.render(self.name, True, text_color)
        surface.blit(name_text, (x + 20, y + 20))

        value_text = font.render(f"{self.value}💰", True, text_color)
        surface.blit(value_text, (x + 20, y + 100))
