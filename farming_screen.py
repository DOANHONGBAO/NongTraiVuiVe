import pygame
import sys

def farming_screen(SCREEN, WIDTH, HEIGHT, FONT, BIG_FONT, COLORS, player, current_day):
    clock = pygame.time.Clock()
    BUTTON_WIDTH, BUTTON_HEIGHT = 300, 90

    while True:
        SCREEN.fill(COLORS["LIGHT_GREEN"])  # màu khác để dễ phân biệt

        # ===== VẼ GIAO DIỆN =====

        title_text = BIG_FONT.render("Khu Trồng Trọt", True, COLORS["BROWN"])
        SCREEN.blit(title_text, (WIDTH // 2 - 150, 50))

        gold_text = FONT.render(f"Vàng: {player.gold}", True, COLORS["YELLOW"])
        SCREEN.blit(gold_text, (30, 150))

        farm_text = FONT.render(f"Động vật: {len(player.animals)} | Thức ăn: {len(player.food)}", True, COLORS["BLACK"])
        SCREEN.blit(farm_text, (30, 200))

        day_text = FONT.render(f"Ngày: {current_day}", True, COLORS["BLACK"])
        SCREEN.blit(day_text, (30, 250))

        # Nút tam giác quay về gameplay
        triangle_center = (WIDTH - 30, HEIGHT // 2)
        triangle_size = 30
        triangle_points = [
            (triangle_center[0], triangle_center[1]),
            (triangle_center[0] - triangle_size, triangle_center[1] - triangle_size),
            (triangle_center[0] - triangle_size, triangle_center[1] + triangle_size),
        ]
        pygame.draw.polygon(SCREEN, COLORS["DARK_GREEN"], triangle_points)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                triangle_rect = pygame.Rect(triangle_center[0] - triangle_size, triangle_center[1] - triangle_size, triangle_size, triangle_size * 2)
                if triangle_rect.collidepoint(event.pos):
                    return "back_to_gameplay"

        pygame.display.update()
        clock.tick(60)
