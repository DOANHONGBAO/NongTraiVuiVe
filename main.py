import pygame
import sys
from menu import start_screen
from gameplay import gameplay_screen

pygame.init()
WIDTH, HEIGHT = 1915, 1020 
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(" Nông Trại Vui Vẻ ")

# Màu sắc và font
COLORS = {
    "WHITE": (255, 255, 255),
    "GREEN": (150, 200, 150),
    "DARK_GREEN": (60, 130, 60),
    "BLACK": (0, 0, 0),
    "YELLOW": (255, 215, 0),
    "BROWN": (160, 100, 50)
}
FONT = pygame.font.Font("assets/fonts/arcade-among-1.otf", 24)
BIG_FONT = pygame.font.Font("assets/fonts/arcade-among-1.otf", 36)

# Các trạng thái của game
STATE_MENU = "menu"
STATE_GAMEPLAY = "gameplay"
current_state = STATE_MENU

# Hàm chính
def main():
    global current_state

    clock = pygame.time.Clock()

    while True:
        # Lấy sự kiện toàn cục
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Gọi hàm xử lý tương ứng với từng trạng thái
        if current_state == STATE_MENU:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            play_clicked = start_screen(SCREEN, WIDTH, HEIGHT, FONT, BIG_FONT, COLORS, mouse_x, mouse_y)
            if play_clicked:
                current_state = STATE_GAMEPLAY

        elif current_state == STATE_GAMEPLAY:
            result = gameplay_screen(SCREEN, WIDTH, HEIGHT, FONT, BIG_FONT, COLORS)
            if result == "back_to_menu":
                current_state = STATE_MENU  # Quay lại menu khi nhận được "back_to_menu"

        clock.tick(60)

# Chạy game
if __name__ == "__main__":
    main()