"""
Gameplay UI module

This module contains the gameplay screen logic for the game, including UI rendering, user interaction, and game mechanics.
It uses a reusable `ImageButton` class to manage GUI buttons with hover effects and image-based styles.
"""

import pygame
import sys
import math
import random
from player import Player
from merchant import Merchant
from animal import Animal
from calculateScore import calculate_score, save_score
from tiles import TileMap
from GUI import ImageButton

# Global constants
CARD_WIDTH, CARD_HEIGHT = 200, 300
ITEM_WIDTH, ITEM_HEIGHT = 30, 45
BUTTON_WIDTH, BUTTON_HEIGHT = 300, 90
toolbar_width = 800
toolbar_height = 126

merchant_buttons = []
animals_on_field = []
feed_bar_slots = [None] * 9
food_inventory = []
selected_card = [False, False, False, False, False]
player = Player()
shelf_positions = [
    (473, 378,703, 528),  # Shelf 1: (left, top, right, down)
    (941, 378,1182, 531),# Shelf 2
    (474, 536,715, 682),  # Shelf 3
    (946, 534,1245, 686),# Shelf 4

]

def gameplay_screen(SCREEN, WIDTH, HEIGHT, FONT, BIG_FONT, COLORS,clock):
    """
    Main gameplay loop where the game is played.
    Handles rendering, interaction logic, card drawing, animal display, and UI interactions.
    """
    show_feed_ui = False
    clock = pygame.time.Clock()
    count_select_one_day = 3
    merchant = Merchant()
    show_merchant = True
    show_items = False
    buy_merchant = True
    first_time = True
    show_score_summary = False
    score_saved = False
    show_card_frame = False
    current_day = 1
    rolls_left = 1
    merchant_buttons = []  # Reset mỗi frame
    tilemap = TileMap("assets/tiles/background.tmx")

    # Buttons
    # Load hình ảnh
    toolbar_image = pygame.image.load("assets/images/toolbar.png").convert_alpha()
    shop_image = pygame.image.load("assets/images/merchant.png").convert_alpha()
    shop_image = pygame.transform.scale(shop_image, (1200, 800))  # nếu cần resize
    pot_image = pygame.image.load("assets/images/pot.png").convert_alpha()
    pot_image = pygame.transform.scale(pot_image, (223, 181))  # nếu chưa đúng kích thước thì resize lại
    # Tải hình ảnh nút
    image_normal = pygame.image.load("assets/GUI/ButtonsText/ButtonText_Large_GreyOutline_Round.png").convert_alpha()
    image_hover = pygame.image.load("assets/GUI/ButtonsText/ButtonText_Large_Orange_Round.png").convert_alpha()

    # Tải hình tam giác
    image_triangle = pygame.image.load("assets/GUI/Sliders/ScrollSlider_Arrow.png").convert_alpha()
    image_triangle = pygame.transform.rotate(image_triangle, 180)
    image_triangle = pygame.transform.scale(image_triangle, (60, 60))
    #Tải hình ảnh quay lại
    image_return = pygame.image.load("assets/GUI/Icons/Icon_Small_WhiteOutline_Arrow.png").convert_alpha()
    image_return = pygame.transform.rotate(image_return,180)
    image_return_hover = pygame.image.load("assets/GUI/Icons/Icon_Small_Blank_Arrow.png").convert_alpha()
    # Tạo các nút sử dụng ImageButton với hiệu ứng hover
    back_btn = ImageButton(
        WIDTH - BUTTON_WIDTH - 30, 30, BUTTON_WIDTH, BUTTON_HEIGHT,
        "Quay lại Menu", FONT,
        (255, 255, 255),  # màu chữ bình thường
        image_normal, image_hover,
        hover_text_color=(255, 255, 0)  # vàng khi hover
    )

    next_day_btn = ImageButton(
        WIDTH - BUTTON_WIDTH - 30, 150, BUTTON_WIDTH, BUTTON_HEIGHT,
        "Qua ngày", FONT,
        (255, 255, 255),
        image_normal, image_hover,
        hover_text_color=(255, 255, 0)
    )

    roll_btn = ImageButton(
        WIDTH - BUTTON_WIDTH - 30, 230, BUTTON_WIDTH, BUTTON_HEIGHT,
        "Rút lại bài", FONT,
        (255, 255, 255),
        image_normal, image_hover,
        hover_text_color=(255, 255, 0)
    )

    play_btn = ImageButton(
        WIDTH - BUTTON_WIDTH - 30, 310, BUTTON_WIDTH, BUTTON_HEIGHT,
        "Tính điểm", FONT,
        (255, 255, 255),
        image_normal, image_hover,
        hover_text_color=(255, 255, 0)
    )

    toggle_card_btn = ImageButton(
        30, HEIGHT - 80, 200, 50,
        "Ẩn/Hiện bài", FONT,
        (255, 255, 255),
        image_normal, image_hover,
        hover_text_color=(255, 255, 0)
    )

    farm_btn = ImageButton(
        0, HEIGHT // 2 - 30, 60, 60,
        "", FONT,  # không có text
        (0, 0, 0),
        image_triangle,
        image_triangle  # có thể dùng cùng một hình cho hover nếu không có ảnh riêng
    )

    see_items_btn = ImageButton(
        50, 300, BUTTON_WIDTH, 60,
        "Xem hàng từ thương gia", FONT,
        (255, 255, 255),
        image_normal, image_hover,
        hover_text_color=(255, 255, 0)
    )

    back_merchant_btn = ImageButton(
        1375, 158, 120, 90,
        "",FONT,
        (255, 255, 255),
        image_return, image_return,
        hover_text_color=(255, 255, 0)
    )
    confirm_btn = ImageButton(
        WIDTH // 2 - 100, HEIGHT // 2 + 80, 200, 60,
        "OK. Quay lại Menu", FONT,
        (255, 255, 255),
        image_normal, image_hover,
        hover_text_color=(255, 255, 0)
    )


    def draw_cards():
        player.hand = player.draw_cards()
        for i in range(len(selected_card)):
            selected_card[i] = False

    draw_cards()

    while True:
        mouse_pos = pygame.mouse.get_pos()
        SCREEN.fill(COLORS["GREEN"])
        tilemap.draw(SCREEN)

        merchant_buttons.clear()
        if (current_day % 2 == 0) and buy_merchant:
            merchant = Merchant()
            show_merchant = True
            buy_merchant = False

        # UI Text
        SCREEN.blit(BIG_FONT.render(f"Vàng: {player.gold}", True, COLORS["YELLOW"]), (30, 30))
        SCREEN.blit(BIG_FONT.render(f"Ngày {current_day}", True, COLORS["BLACK"]), (30, 100))
        SCREEN.blit(FONT.render(f"Lượt roll còn lại: {rolls_left}", True, COLORS["BLACK"]), (30, 220))


        # Vị trí để đặt ảnh thanh công cụ ở giữa dưới
        toolbar_x = (1900 - toolbar_width) // 2
        toolbar_y = 1000 - toolbar_height

        # Vẽ ảnh thanh công cụ
        SCREEN.blit(toolbar_image, (toolbar_x, toolbar_y))
        # Buttons rendering
        for btn in [back_btn, next_day_btn, roll_btn, play_btn, toggle_card_btn,farm_btn]:
            btn.draw(SCREEN, mouse_pos)

        # Animal drawing
        for animal in animals_on_field:
            animal.update()
            animal.draw(SCREEN)
        

        # Card logic
        if "card_y_offsets" not in player.__dict__ or len(player.card_y_offsets) != len(player.hand):
            player.card_y_offsets = [random.randint(-5, 5) for _ in player.hand]

        if show_card_frame:
            hovered_index = None
            num_cards = len(player.hand)
            card_spacing = 175
            total_width = (num_cards - 1) * card_spacing
            start_x = WIDTH // 2 - total_width // 2
            card_height = player.hand[0].get_image().get_height()
            base_y = HEIGHT - card_height - 30 - 124
            hover_offset = -20
            select_offset = -40

            for i, card in enumerate(player.hand):
                card_x = start_x + i * card_spacing
                card_y = base_y + player.card_y_offsets[i]
                card_img = card.get_image()
                rect = card_img.get_rect(midtop=(card_x, card_y))
                mask = pygame.mask.from_surface(card_img)

                offset = (mouse_pos[0] - rect.left, mouse_pos[1] - rect.top)
                if 0 <= offset[0] < rect.width and 0 <= offset[1] < rect.height:
                    if mask.get_at(offset):
                        hovered_index = i

                if selected_card[i]:
                    rect.y += select_offset
                elif hovered_index == i:
                    rect.y += hover_offset

                SCREEN.blit(card_img, rect.topleft)



        # ===================== GIAO DIỆN THƯƠNG GIA =====================
        merchant_buttons = []

        if show_merchant and not show_items:
            see_items_btn.draw(SCREEN,mouse_pos)


        elif show_merchant and show_items:
            # Xác định kích thước của cửa hàng
            shop_width = shop_image.get_width() # 1200
            shop_height = shop_image.get_height() #800

            # Tính toán vị trí của cửa hàng sao cho nó nằm ở giữa màn hình
            screen_width, screen_height = SCREEN.get_size()  # Kích thước màn hình
            shop_x = (screen_width - shop_width) // 2
            shop_y = (screen_height - shop_height) // 2

            # Vẽ cửa hàng ở giữa màn hình
            SCREEN.blit(shop_image, (shop_x, shop_y))

            # Vẽ các item trong cửa hàng
            for i, item in enumerate(merchant.items):
                if i < len(shelf_positions):
                    left, top, right, bottom = shelf_positions[i]

                    shelf_center_x = (left + right) // 2
                    shelf_center_y = (top + bottom) // 2

                    item_box = pygame.Rect(0, 0, 223, 181)
                    item_box.center = (shelf_center_x, shelf_center_y - 10)

                    # Vẽ ảnh pot thay cho khung chữ nhật
                    SCREEN.blit(pot_image, pot_image.get_rect(center=item_box.center))

                    # Vẽ tên item
                    item_text = FONT.render(item.name, True, COLORS["WHITE"])
                    SCREEN.blit(item_text, (item_box.x + 5, item_box.y + 5))


                    merchant_buttons.append((item_box, item))  # Lưu item_box thay vì buy_btn

            back_merchant_btn.draw(SCREEN,mouse_pos)

        if show_score_summary:
            confirm_btn.draw(SCREEN, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(mouse_pos)
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

                if show_merchant and not show_items:
                    if see_items_btn.is_clicked(event):
                        show_items = True

                elif show_merchant and show_items:
                    for item_box, item in merchant_buttons:  # Đổi từ (btn, item) sang (item_box, item)
                        # Kiểm tra click vào pot_image
                        if item_box.collidepoint(event.pos) and player.gold >= item.cost:
                            player.gold -= item.cost

                            if isinstance(item, Animal):
                                player.animals.append(item.name)
                                animals_on_field.append(item)
                            else:
                                player.food.append(item.name)

                            merchant.items.remove(item)
                            break

                    if back_merchant_btn.is_clicked(event):
                        show_items = False


                if show_score_summary and confirm_btn.is_clicked(event):
                    return "main_menu"

                if back_btn.is_clicked(event):
                    show_score_summary = True
                if toggle_card_btn.is_clicked(event):
                    show_card_frame = not show_card_frame
                if play_btn.is_clicked(event):
                    temp = []
                    for i, card in enumerate(player.hand):
                        if selected_card[i]:
                            player.gold += card.value
                            temp.append(card)
                            count_select_one_day -= 1
                            selected_card[i] = False
                    for card in temp:
                        player.hand.remove(card)
                if next_day_btn.is_clicked(event):
                    current_day += 1
                    rolls_left = 1
                    draw_cards()
                    buy_merchant = True
                    show_merchant = False
                    show_items = False
                    count_select_one_day = 3
                if roll_btn.is_clicked(event) and rolls_left > 0:
                    draw_cards()
                    rolls_left -= 1
                if farm_btn.is_clicked(event):
                    return "go_to_farming", player, current_day

        pygame.display.update()
        clock.tick(60)
