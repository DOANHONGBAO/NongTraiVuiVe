import pygame
import sys

def start_screen(screen, width, height, font, big_font, colors, mouse_x=None, mouse_y=None):
    screen.fill(colors["GREEN"])
    title_text = big_font.render(" Nông Trại Vui Vẻ ", True, colors["BLACK"])
    screen.blit(title_text, (width // 4, height // 4))

    # Nút Play
    play_button = pygame.Rect(width // 3, height // 2, 200, 50)
    pygame.draw.rect(screen, colors["YELLOW"], play_button)
    play_text = font.render("Play Game", True, colors["BLACK"])
    screen.blit(play_text, (width // 3 + 60, height // 2 + 10))

    # Kiểm tra nếu chuột nhấn vào nút Play
    if mouse_x and mouse_y:
        if play_button.collidepoint(mouse_x, mouse_y):
            if pygame.mouse.get_pressed()[0]:  # Chuột trái
                return True  # Trả về True nếu Play được nhấn

    pygame.display.flip()
    return False  # Trả về False nếu không nhấn Play

