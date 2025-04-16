import pygame
import sys


def start_screen(screen, width, height, font, big_font, colors, mouse_x=None, mouse_y=None):
    background_img = pygame.image.load("assets/images/BG.jpeg").convert()
    background_img = pygame.transform.scale(background_img, (width, height))
    screen.blit(background_img, (0, 0))

    # Load và hiển thị tiêu đề
    title_img = pygame.image.load("assets/images/title_only.png").convert_alpha()
    title_img = pygame.transform.scale(title_img, (int(title_img.get_width() * 0.7), int(title_img.get_height() * 0.7)))
    title_rect = title_img.get_rect(center=(width // 2, height // 3))
    screen.blit(title_img, title_rect)

    # Load và hiển thị nút Play
    play_img = pygame.image.load("assets/images/play_button_only.png").convert_alpha()
    play_img = pygame.transform.scale(play_img, (int(play_img.get_width() * 0.7), int(play_img.get_height() * 0.7)))
    play_rect = play_img.get_rect(center=(width // 2, height // 1.5))

    # Kiểm tra nếu chuột hover vào nút Play
    if play_rect.collidepoint(mouse_x, mouse_y):
        # Tăng kích thước nút khi hover
        play_img = pygame.transform.scale(play_img, (int(play_img.get_width() * 0.95), int(play_img.get_height() * 0.95)))
        play_rect = play_img.get_rect(center=(width // 2, height // 1.5))
    screen.blit(play_img, play_rect)

    # Kiểm tra nếu chuột nhấn vào nút Play
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_rect.collidepoint(event.pos):  # Nếu click vào nút Play
                return True  # Quay về True khi Play được nhấn
    
    pygame.display.flip()
    return False  # Không làm gì nếu không nhấn Play
