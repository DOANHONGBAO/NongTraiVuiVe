import pygame
import sys
from player import Player
from merchant import Merchant
from animal import Animal
from calculateScore import calculate_score, save_score

def gameplay_screen(SCREEN, WIDTH, HEIGHT, FONT, BIG_FONT, COLORS):
    round_count = 0
    player = Player()
    selected_card = [False, False, False]
    clock = pygame.time.Clock()

    # Merchant and UI states
    merchant = Merchant()
    show_merchant = False
    show_items = False
    buy_merchant = True

    # Score summary state
    show_score_summary = False
    score_saved = False

    # Tăng kích thước các thành phần giao diện theo độ phân giải lớn hơn
    CARD_WIDTH, CARD_HEIGHT = 300, 150
    ITEM_WIDTH, ITEM_HEIGHT = 300, 150
    BUTTON_WIDTH, BUTTON_HEIGHT = 300, 90

    while True:
        SCREEN.fill(COLORS["GREEN"])
        round_count += 1

        if (round_count % 50 == 0) and buy_merchant:
            merchant = Merchant()
            show_merchant = True
            buy_merchant = False

        # ===== VẼ GIAO DIỆN =====

        gold_text = BIG_FONT.render(f"Vàng: {player.gold}", True, COLORS["YELLOW"])
        gold_rect = gold_text.get_rect(topleft=(30, 30))
        SCREEN.blit(gold_text, gold_rect)

        farm_text = BIG_FONT.render(
            f"Động vật: {len(player.animals)} |  Thức ăn: {len(player.food)}",
            True, COLORS["BLACK"]
        )
        SCREEN.blit(farm_text, (30, 130))

        # Nút quay lại menu
        back_button = pygame.Rect(WIDTH - BUTTON_WIDTH - 30, 30, BUTTON_WIDTH, BUTTON_HEIGHT)
        pygame.draw.rect(SCREEN, COLORS["BROWN"], back_button)
        back_text = FONT.render("Quay lại Menu", True, COLORS["WHITE"])
        back_text_rect = back_text.get_rect(center=back_button.center)
        SCREEN.blit(back_text, back_text_rect)

        merchant_buttons = []
        if show_merchant and not show_items:
            see_items_button = pygame.Rect(50, 200, BUTTON_WIDTH, BUTTON_HEIGHT)
            pygame.draw.rect(SCREEN, COLORS["BROWN"], see_items_button)
            see_text = FONT.render("Xem hàng từ thương gia", True, COLORS["WHITE"])
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
            back_text = FONT.render(" Không mua nữa", True, COLORS["WHITE"])
            back_text_rect = back_text.get_rect(center=back_merchant_button.center)
            SCREEN.blit(back_text, back_text_rect)

            for i, card in enumerate(player.hand):
                card_x = 50 + i * (CARD_WIDTH + 60)
                card_y = 650
                card.draw(SCREEN, card_x, card_y, FONT, COLORS["BROWN"], COLORS["WHITE"], COLORS["YELLOW"])
                if selected_card[i]:
                    pygame.draw.rect(SCREEN, COLORS["YELLOW"], (card_x, card_y, CARD_WIDTH, CARD_HEIGHT), 4)

            play_button = pygame.Rect(WIDTH - BUTTON_WIDTH - 30, HEIGHT - BUTTON_HEIGHT - 30, BUTTON_WIDTH, BUTTON_HEIGHT)
            pygame.draw.rect(SCREEN, COLORS["DARK_GREEN"], play_button)
            play_text = FONT.render("CHƠI BÀI", True, COLORS["WHITE"])
            play_text_rect = play_text.get_rect(center=play_button.center)
            SCREEN.blit(play_text, play_text_rect)

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

        # ===== XỬ LÝ SỰ KIỆN =====

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if show_score_summary:
                    if confirm_button.collidepoint(event.pos):
                        return "back_to_menu"

                if back_button.collidepoint(event.pos):
                    show_score_summary = True

                if show_merchant and not show_items:
                    if see_items_button.collidepoint(event.pos):
                        show_items = True

                elif show_merchant and show_items:
                    for i in range(3):
                        card_x = 50 + i * (CARD_WIDTH + 60)
                        card_rect = pygame.Rect(card_x, 650, CARD_WIDTH, CARD_HEIGHT)
                        if card_rect.collidepoint(event.pos):
                            selected_card[i] = not selected_card[i]

                    if play_button.collidepoint(event.pos):
                        for i in range(3):
                            if selected_card[i]:
                                player.gold += player.hand[i].value
                                selected_card[i] = False
                        player.hand = player.draw_cards()

                    for btn, item in merchant_buttons:
                        if btn.collidepoint(event.pos) and player.gold >= item.cost:
                            player.gold -= item.cost
                            if isinstance(item, Animal):
                                player.animals.append(item.name)
                            else:
                                player.food.append(item.name)
                            buy_merchant = True
                            show_items = False
                            show_merchant = False

                    if back_merchant_button.collidepoint(event.pos):
                        show_items = False

        pygame.display.update()
        clock.tick(60)
