import pygame
import sys
from GUI import ImageButton

def start_screen(screen, width, height, font, big_font, colors):
    clock = pygame.time.Clock()

    # Load background
    background_img = pygame.image.load("assets/images/BG.jpeg").convert()
    background_img = pygame.transform.scale(background_img, (width, height))

    # Load title
    title_img = pygame.image.load("assets/images/title_only.png").convert_alpha()
    title_img = pygame.transform.scale(title_img, (
        int(title_img.get_width() * 0.7),
        int(title_img.get_height() * 0.7)
    ))
    title_rect = title_img.get_rect(center=(width // 2, height // 3))

    # Load button images
    play_img = pygame.image.load("assets/images/play_button_only.png").convert_alpha()
    try:
        play_img_hover = pygame.image.load("assets/images/play_button_hover.png").convert_alpha()
    except:
        play_img_hover = play_img  # fallback nếu không có hover riêng

    # Tạo ImageButton
    button_width = int(play_img.get_width() * 0.7)
    button_height = int(play_img.get_height() * 0.7)
    play_btn = ImageButton(
        width // 2 - button_width // 2, int(height // 1.5) - button_height // 2,
        button_width, button_height,
        "", font,
        (0, 0, 0),  # không có chữ nên không quan trọng
        play_img, play_img_hover
    )

    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(background_img, (0, 0))
        screen.blit(title_img, title_rect)

        # Vẽ nút Play
        play_btn.draw(screen, mouse_pos)

        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif play_btn.is_clicked(event):
                return True

        pygame.display.flip()
        clock.tick(60)
