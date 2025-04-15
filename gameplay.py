import pygame
import sys
from player import Player
from merchant import Merchant
from animal import Animal
def gameplay_screen(SCREEN, WIDTH, HEIGHT, FONT, BIG_FONT, COLORS):
    round_count = 0
    merchant = Merchant()
    show_merchant = False
    buy_merchant = True
    player = Player()
    selected_card = [False, False, False]
    clock = pygame.time.Clock()
    show_items = False       # Đã nhấn xem hàng chưa
    merchant_buttons = []    # Danh sách nút "Mua" cho mỗi item


    while True:
        # print(buy_merchant)
        SCREEN.fill(COLORS["GREEN"])
        round_count += 1
        if (round_count % 50 == 0) and (buy_merchant):  # Mỗi 50 lượt gọi thương gia
            merchant = Merchant()
            show_merchant = True
            buy_merchant = False

        if show_merchant and not show_items:
            see_items_button = pygame.Rect(50, 150, 250, 50)
            pygame.draw.rect(SCREEN, COLORS["BROWN"], see_items_button)
            see_text = FONT.render(" Xem hàng từ thương gia", True, COLORS["WHITE"])
            SCREEN.blit(see_text, (see_items_button.x + 10, see_items_button.y + 10))

        if show_merchant and show_items:

            merchant_buttons = []  # reset mỗi frame

            for i, item in enumerate(merchant.items):
                item_box = pygame.Rect(70 + i * 220, 190, 200, 100)
                pygame.draw.rect(SCREEN, COLORS["BROWN"], item_box)

                item_text = FONT.render(str(item), True, COLORS["WHITE"])
                SCREEN.blit(item_text, (item_box.x + 10, item_box.y + 10))

                buy_btn = pygame.Rect(item_box.x + 50, item_box.y + 60, 100, 25)
                pygame.draw.rect(SCREEN, COLORS["DARK_GREEN"], buy_btn)
                buy_text = FONT.render("Mua", True, COLORS["WHITE"])
                SCREEN.blit(buy_text, (buy_btn.x + 25, buy_btn.y + 2))

                merchant_buttons.append((buy_btn, item))

            # Nút "Không mua nữa"
            back_merchant_button = pygame.Rect(400, 320, 200, 40)
            pygame.draw.rect(SCREEN, COLORS["BLACK"], back_merchant_button)
            back_text = FONT.render("⬅️ Không mua nữa", True, COLORS["WHITE"])
            SCREEN.blit(back_text, (back_merchant_button.x + 15, back_merchant_button.y + 8))

            # Hiển thị các lá bài
            for i, card in enumerate(player.hand):
                card_x = 50 + i * 170
                card_y = 400
                card.draw(SCREEN, card_x, card_y, FONT, COLORS["BROWN"], COLORS["WHITE"], COLORS["YELLOW"])
                if selected_card[i]:
                    pygame.draw.rect(SCREEN, COLORS["YELLOW"], (card_x, card_y, 150, 80), 3)

            # Nút "Chơi bài"
            play_button = pygame.Rect(WIDTH - 220, HEIGHT - 100, 180, 60)
            pygame.draw.rect(SCREEN, COLORS["DARK_GREEN"], play_button)
            play_text = FONT.render("CHƠI BÀI", True, COLORS["WHITE"])
            SCREEN.blit(play_text, (play_button.x + 40, play_button.y + 15))
            
           


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Kiểm tra nút "Quay lại Menu"
                if back_button.collidepoint(event.pos):
                    return "back_to_menu"  

                # Bấm "Xem hàng"
                if show_merchant and not show_items:
                    if see_items_button.collidepoint(event.pos):
                        show_items = True

                # Khi đã mở hàng
                elif show_merchant and show_items:
                    # Kiểm tra các hành động khác như chọn thẻ
                    for i in range(3):
                        card_x = 50 + i * 170
                        card_rect = pygame.Rect(card_x, 400, 150, 80)
                        if card_rect.collidepoint(event.pos):
                            selected_card[i] = not selected_card[i]

                    if play_button.collidepoint(event.pos):
                        for i in range(3):
                            if selected_card[i]:
                                player.gold += player.hand[i].value
                                selected_card[i] = False
                        player.hand = player.draw_cards()
                    #logic mua hàng
                    for btn, item in merchant_buttons:
                        if btn.collidepoint(event.pos) and player.gold >= item.cost:
                            player.gold -= item.cost
                            if isinstance(item, Animal):
                                player.animals.append(item.name)
                            else:
                                player.food.append(item.name)
                            buy_merchant = True
                            show_items = False
                            show_merchant = False  # đóng shop sau khi mua

                    # Nút "Không mua nữa"
                    if back_merchant_button.collidepoint(event.pos):
                        show_items = False  # quay về không mua gì





           



        # Hiển thị vàng
        gold_text = BIG_FONT.render(f" Vàng: {player.gold}", True, COLORS["YELLOW"])
        SCREEN.blit(gold_text, (30, 30))

        # Hiển thị số lượng động vật và thức ăn
        farm_text = FONT.render(
            f" Động vật: {len(player.animals)} |  Thức ăn: {len(player.food)}",
            True, COLORS["BLACK"]
        )
        SCREEN.blit(farm_text, (30, 80))

        # Nút "Quay lại Menu"
        back_button = pygame.Rect(20, 20, 180, 60)
        pygame.draw.rect(SCREEN, COLORS["BROWN"], back_button)
        back_text = FONT.render("Quay lại Menu", True, COLORS["WHITE"])
        SCREEN.blit(back_text, (back_button.x + 40, back_button.y + 15))

        pygame.display.update()
        clock.tick(60)
