import pygame
import sys
from player import Player
from merchant import Merchant
from animal import Animal
from calculateScore import calculate_score, save_score


def gameplay_screen(SCREEN, WIDTH, HEIGHT, FONT, BIG_FONT, COLORS):
    player = Player()
    selected_card = [False, False, False, False, False]
    clock = pygame.time.Clock()

    merchant = Merchant()
    show_merchant = True
    show_items = False
    buy_merchant = True

    show_score_summary = False
    score_saved = False

    current_day = 1
    rolls_left = 1

    CARD_WIDTH, CARD_HEIGHT = 300, 150
    ITEM_WIDTH, ITEM_HEIGHT = 300, 150
    BUTTON_WIDTH, BUTTON_HEIGHT = 300, 90

    merchant_buttons = []

    def draw_cards():
        player.hand = player.draw_cards()
        for i in range(len(selected_card)):
            selected_card[i] = False

    draw_cards()

    while True:
        SCREEN.fill(COLORS["GREEN"])

        merchant_buttons.clear()

        # Thương gia mỗi 2 ngày
        if (current_day % 2 == 0) and buy_merchant:
            merchant = Merchant()
            show_merchant = True
            buy_merchant = False

        # ===== VẼ GIAO DIỆN =====

        gold_text = BIG_FONT.render(f"Vàng: {player.gold}", True, COLORS["YELLOW"])
        SCREEN.blit(gold_text, (30, 30))

        farm_text = BIG_FONT.render(
            f"Động vật: {len(player.animals)} | Thức ăn: {len(player.food)}",
            True, COLORS["BLACK"]
        )
        SCREEN.blit(farm_text, (30, 100))

        day_text = BIG_FONT.render(f"Ngày {current_day}", True, COLORS["BLACK"])
        SCREEN.blit(day_text, (30, 170))

        roll_text = FONT.render(f"Lượt roll còn lại: {rolls_left}", True, COLORS["BLACK"])
        SCREEN.blit(roll_text, (30, 220))

        back_button = pygame.Rect(WIDTH - BUTTON_WIDTH - 30, 30, BUTTON_WIDTH, BUTTON_HEIGHT)
        pygame.draw.rect(SCREEN, COLORS["BROWN"], back_button)
        back_text = FONT.render("Quay lại Menu", True, COLORS["WHITE"])
        SCREEN.blit(back_text, back_button.move(40, 30))

        next_day_button = pygame.Rect(WIDTH - BUTTON_WIDTH - 30, 150, BUTTON_WIDTH, 60)
        pygame.draw.rect(SCREEN, COLORS["BLACK"], next_day_button)
        next_day_text = FONT.render("➡️ Qua ngày", True, COLORS["WHITE"])
        SCREEN.blit(next_day_text, next_day_button.move(70, 10))

        roll_button = pygame.Rect(WIDTH - BUTTON_WIDTH - 30, 230, BUTTON_WIDTH, 60)
        pygame.draw.rect(SCREEN, COLORS["DARK_GREEN"], roll_button)
        roll_text_btn = FONT.render("🎲 Rút lại bài", True, COLORS["WHITE"])
        SCREEN.blit(roll_text_btn, roll_button.move(70, 10))

        play_button = pygame.Rect(WIDTH - BUTTON_WIDTH - 30, 310, BUTTON_WIDTH, 60)
        pygame.draw.rect(SCREEN, COLORS["BROWN"], play_button)
        play_text = FONT.render("▶️ Tính điểm", True, COLORS["WHITE"])
        SCREEN.blit(play_text, play_button.move(70, 10))

        if show_merchant and not show_items:
            see_items_button = pygame.Rect(50, 300, BUTTON_WIDTH, 60)
            pygame.draw.rect(SCREEN, COLORS["BROWN"], see_items_button)
            see_text = FONT.render("🛒 Xem hàng từ thương gia", True, COLORS["WHITE"])
            see_text_rect = see_text.get_rect(center=see_items_button.center)
            SCREEN.blit(see_text, see_text_rect)

        if show_merchant and show_items:
            for i, item in enumerate(merchant.items):
                item_box = pygame.Rect(70 + i * (ITEM_WIDTH + 40), 300, ITEM_WIDTH, ITEM_HEIGHT)
                pygame.draw.rect(SCREEN, COLORS["BROWN"], item_box)
                item_text = FONT.render(str(item), True, COLORS["WHITE"])
                SCREEN.blit(item_text, (item_box.x + 10, item_box.y + 10))

                buy_btn = pygame.Rect(item_box.x + 80, item_box.y + 90, 140, 40)
                pygame.draw.rect(SCREEN, COLORS["DARK_GREEN"], buy_btn)
                buy_text = FONT.render("Mua", True, COLORS["WHITE"])
                buy_text_rect = buy_text.get_rect(center=buy_btn.center)
                SCREEN.blit(buy_text, buy_text_rect)
                merchant_buttons.append((buy_btn, item))

            back_merchant_button = pygame.Rect(420, 500, BUTTON_WIDTH, 60)
            pygame.draw.rect(SCREEN, COLORS["BLACK"], back_merchant_button)
            back_text = FONT.render("⬅️ Không mua nữa", True, COLORS["WHITE"])
            back_text_rect = back_text.get_rect(center=back_merchant_button.center)
            SCREEN.blit(back_text, back_text_rect)

        for i, card in enumerate(player.hand):
            card_x = 50 + i * (CARD_WIDTH + 60)
            card_y = 650
            card.draw(SCREEN, card_x, card_y, FONT, COLORS["BROWN"], COLORS["WHITE"], COLORS["YELLOW"])
            if selected_card[i]:
                pygame.draw.rect(SCREEN, COLORS["YELLOW"], (card_x, card_y, CARD_WIDTH, CARD_HEIGHT), 5)

        if show_score_summary:
            score = calculate_score(player)
            if not score_saved:
                save_score("Người chơi", score)
                score_saved = True

            summary_box = pygame.Rect(WIDTH // 2 - 300, HEIGHT // 2 - 200, 600, 400)
            pygame.draw.rect(SCREEN, COLORS["WHITE"], summary_box)
            pygame.draw.rect(SCREEN, COLORS["BLACK"], summary_box, 4)

            summary_text = BIG_FONT.render("KẾT QUẢ", True, COLORS["BLACK"])
            SCREEN.blit(summary_text, (summary_box.x + 200, summary_box.y + 40))
            detail_text = FONT.render(f"Điểm: {score} (vàng + thú + thức ăn)", True, COLORS["BLACK"])
            SCREEN.blit(detail_text, (summary_box.x + 70, summary_box.y + 160))

            confirm_button = pygame.Rect(summary_box.x + 200, summary_box.y + 280, 200, 60)
            pygame.draw.rect(SCREEN, COLORS["DARK_GREEN"], confirm_button)
            confirm_text = FONT.render("OK. Quay lại Menu", True, COLORS["WHITE"])
            confirm_text_rect = confirm_text.get_rect(center=confirm_button.center)
            SCREEN.blit(confirm_text, confirm_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if show_score_summary:
                    if confirm_button.collidepoint(event.pos):
                        return "back_to_menu"

                # if back_button.collidepoint(event.pos):
                    # show_score_summary = True

                if play_button.collidepoint(event.pos):
                    # Tính điểm từ các lá bài và cộng vào vàng của người chơi
                    for card in player.hand:
                        player.gold += card.value  # Thêm giá trị của lá bài vào vàng
                    draw_cards()

                if next_day_button.collidepoint(event.pos):
                    current_day += 1
                    rolls_left = 1
                    draw_cards()
                    buy_merchant = True
                    show_merchant = False
                    show_items = False

                if roll_button.collidepoint(event.pos) and rolls_left > 0:
                    draw_cards()
                    rolls_left -= 1

                if show_merchant and not show_items:
                    if see_items_button.collidepoint(event.pos):
                        show_items = True

                elif show_merchant and show_items:
                    for btn, item in merchant_buttons:
                        if btn.collidepoint(event.pos) and player.gold >= item.cost:
                            player.gold -= item.cost
                            if isinstance(item, Animal):
                                player.animals.append(item.name)
                            else:
                                player.food.append(item.name)
                            merchant.items.remove(item)
                            break

                    if back_merchant_button.collidepoint(event.pos):
                        show_items = False

                for i in range(len(player.hand)):
                    card_x = 50 + i * (CARD_WIDTH + 60)
                    card_y = 650
                    card_rect = pygame.Rect(card_x, card_y, CARD_WIDTH, CARD_HEIGHT)
                    if card_rect.collidepoint(event.pos):
                        selected_card[i] = not selected_card[i]

        pygame.display.update()
        clock.tick(60)
