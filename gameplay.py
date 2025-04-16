import pygame
import sys
from player import Player
from merchant import Merchant
from animal import Animal
from calculateScore import calculate_score, save_score
from tiles import TileMap
import math
import random

def gameplay_screen(SCREEN, WIDTH, HEIGHT, FONT, BIG_FONT, COLORS):
    player = Player()
    selected_card = [False, False, False, False, False]
    clock = pygame.time.Clock()
    count_select_one_day = 3
    merchant = Merchant()
    show_merchant = True
    show_items = False
    buy_merchant = True

    show_score_summary = False
    score_saved = False
    show_card_frame = True  # Khung bài đang hiển thị


    current_day = 1
    rolls_left = 1

    CARD_WIDTH, CARD_HEIGHT = 200, 300
    ITEM_WIDTH, ITEM_HEIGHT = 300, 450
    BUTTON_WIDTH, BUTTON_HEIGHT = 300, 90

    merchant_buttons = []

    def draw_cards():
        player.hand = player.draw_cards()
        for i in range(len(selected_card)):
            selected_card[i] = False

    draw_cards()

    tilemap = TileMap("assets/tiles/background.tmx")  # đường dẫn đến file .tmx

    while True:
        SCREEN.fill(COLORS["GREEN"])
        tilemap.draw(SCREEN)

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
        next_day_text = FONT.render(" Qua ngày", True, COLORS["WHITE"])
        SCREEN.blit(next_day_text, next_day_button.move(70, 10))

        roll_button = pygame.Rect(WIDTH - BUTTON_WIDTH - 30, 230, BUTTON_WIDTH, 60)
        pygame.draw.rect(SCREEN, COLORS["DARK_GREEN"], roll_button)
        roll_text_btn = FONT.render(" Rút lại bài", True, COLORS["WHITE"])
        SCREEN.blit(roll_text_btn, roll_button.move(70, 10))

        play_button = pygame.Rect(WIDTH - BUTTON_WIDTH - 30, 310, BUTTON_WIDTH, 60)
        pygame.draw.rect(SCREEN, COLORS["BROWN"], play_button)
        play_text = FONT.render(" Tính điểm", True, COLORS["WHITE"])
        SCREEN.blit(play_text, play_button.move(70, 10))

        toggle_card_button = pygame.Rect(30, HEIGHT - 80, 200, 50)
        pygame.draw.rect(SCREEN, COLORS["BROWN"], toggle_card_button)
        toggle_text = FONT.render(" Ẩn/Hiện bài", True, COLORS["WHITE"])
        SCREEN.blit(toggle_text, toggle_card_button.move(40, 10))

        farm_button = pygame.Rect(0, HEIGHT // 2 - 60, 60, 120)
        pygame.draw.polygon(SCREEN, COLORS["WHITE"], [
            (farm_button.x + 10, farm_button.y + 60), 
            (farm_button.x + 50, farm_button.y + 20),
            (farm_button.x + 50, farm_button.y + 100)
        ])

        if "card_y_offsets" not in player.__dict__ or len(player.card_y_offsets) != len(player.hand):
            player.card_y_offsets = [random.randint(-5, 5) for _ in player.hand]

        if show_card_frame:
            mouse_pos = pygame.mouse.get_pos()
            hovered_index = None

            num_cards = len(player.hand)
            card_spacing = 175
            total_width = (num_cards - 1) * card_spacing
            start_x = WIDTH // 2 - total_width // 2

            card_height = player.hand[0].get_image().get_height()
            base_y = HEIGHT - card_height - 30  # Sát viền dưới, nhưng không chạm hẳn

            hover_offset = -20
            select_offset = -40

            for i, card in enumerate(player.hand):
                card_x = start_x + i * card_spacing
                card_y = base_y + player.card_y_offsets[i]  # lệch nhẹ mỗi lá

                card_img = card.get_image()
                rect = card_img.get_rect(midtop=(card_x, card_y))
                mask = pygame.mask.from_surface(card_img)

                # Kiểm tra hover
                offset = (mouse_pos[0] - rect.left, mouse_pos[1] - rect.top)
                if 0 <= offset[0] < rect.width and 0 <= offset[1] < rect.height:
                    if mask.get_at(offset):
                        hovered_index = i

                # Dịch khi chọn hoặc hover
                if selected_card[i]:
                    rect.y += select_offset
                elif hovered_index == i:
                    rect.y += hover_offset

                SCREEN.blit(card_img, rect.topleft)

                # if selected_card[i]:
                #     pygame.draw.rect(SCREEN, COLORS["YELLOW"], rect, 4)





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
                if show_score_summary and confirm_button.collidepoint(event.pos):
                    return "back_to_menu", None, None
                if toggle_card_button.collidepoint(event.pos):
                    show_card_frame = not show_card_frame
                if farm_button.collidepoint(event.pos):
                    return "go_to_farming", player, current_day
                if show_card_frame:
                    for i, card in enumerate(player.hand):
                        card_x = start_x + i * card_spacing
                        card_y = base_y + player.card_y_offsets[i]

                        card_img = card.get_image()
                        rect = card_img.get_rect(midtop=(card_x, card_y))
                        mask = pygame.mask.from_surface(card_img)

                        offset = (event.pos[0] - rect.left, event.pos[1] - rect.top)
                        if 0 <= offset[0] < rect.width and 0 <= offset[1] < rect.height:
                            if mask.get_at(offset):
                                if not selected_card[i] and sum(selected_card) < count_select_one_day:
                                    selected_card[i] = True
                                elif selected_card[i]:
                                    selected_card[i] = False
                                break



                if back_button.collidepoint(event.pos):
                    show_score_summary = True

                if play_button.collidepoint(event.pos):
                    # Tính điểm từ các lá bài và cộng vào vàng của người chơi
                    temp = []
                    for i,card in enumerate(player.hand):
                        if selected_card[i]:
                            player.gold += card.value  # Thêm giá trị của lá bài vào vàng
                            temp.append(card)
                            count_select_one_day -= 1
                            selected_card[i] = False   
                    for card in temp:
                        player.hand.remove(card)
                if next_day_button.collidepoint(event.pos):
                    current_day += 1
                    rolls_left = 1
                    draw_cards()
                    buy_merchant = True
                    show_merchant = False
                    show_items = False
                    count_select_one_day = 3

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

        pygame.display.update()
        clock.tick(60)