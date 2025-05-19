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
# from calculateScore import calculate_score, save_score
from tiles import TileMap
from GUI import ImageButton
from items import Slot,Inventory,HarvestNotification,Item
# Global constants
CARD_WIDTH, CARD_HEIGHT = 200, 300
ITEM_WIDTH, ITEM_HEIGHT = 30, 45
BUTTON_WIDTH, BUTTON_HEIGHT = 300, 90
toolbar_width = 800
toolbar_height = 126
# Vị trí để đặt ảnh thanh công cụ ở giữa dưới
toolbar_x = (1900 - toolbar_width) // 2
toolbar_y = 1000 - toolbar_height
inventory_x = toolbar_x
inventory_y = toolbar_y - 460

# toolbar_slots = []
# inventory = []
# Vị trí để đặt ảnh thanh công cụ ở giữa dưới
yard = []
merchant_buttons = []
selected_card = [False, False, False, False, False]
player = Player()

shelf_positions = [
    (473, 378,703, 528),  # Shelf 1: (left, top, right, down)
    (941, 378,1182, 531),# Shelf 2
    (474, 536,715, 682),  # Shelf 3
    (946, 534,1245, 686),# Shelf 4

]
merchant = None
last_merchant_spawn = 0

def gameplay_screen(SCREEN, WIDTH, HEIGHT, FONT, BIG_FONT, COLORS,clock,player):
    """
    Main gameplay loop where the game is played.
    Handles rendering, interaction logic, card drawing, animal display, and UI interactions.
    """
    dragging_item = None
    show_inventory = False
    show_feed_ui = False
    clock = pygame.time.Clock()
    count_select_one_day = 3
    show_merchant = False
    buy_merchant = True
    first_time = True
    show_score_summary = False
    score_saved = False
    show_card_frame = False
    current_day = 1
    rolls_left = 1
    # Biến lưu trạng thái kéo chọn vùng
    selecting = False
    start_pos = (0, 0)
    current_pos = (-1, -1)
    selection_rect = None
    merchant_buttons = []  # Reset mỗi frame
    selected_toolbar_index = 0
    global merchant, last_merchant_spawn
    tilemap = TileMap("assets/tiles/background.tmx")
    sell_sound = pygame.mixer.Sound("assets/audios/sell.mp3")
    truck_sound = pygame.mixer.Sound("assets/audios/truck.mp3")
    # Buttons
    # Load hình ảnh
    toolbar_image = pygame.image.load("assets/images/toolbar.png").convert_alpha()
    inventory_image = pygame.image.load("assets/images/inventory.png").convert_alpha()
    shop_image = pygame.image.load("assets/images/merchant.png").convert_alpha()
    shop_image = pygame.transform.scale(shop_image, (1200, 800))  # nếu cần resize
    pot_image = pygame.image.load("assets/images/pot.png").convert_alpha()
    pot_image = pygame.transform.scale(pot_image, (223, 181))  # nếu chưa đúng kích thước thì resize lại
    # Tải hình ảnh nút
    image_normal = pygame.image.load("assets/GUI/ButtonsIcons/IconButton_Large_Circle.png").convert_alpha()
    image_hover = pygame.image.load("assets/GUI/ButtonsIcons/IconButton_Large_GreyOutline_Circle.png").convert_alpha()

    coin_image = pygame.image.load("assets/images/coin.png").convert_alpha()
    coin_image = pygame.transform.scale(coin_image, (20, 20))  # Resize vừa phải


    # Tạo các nút sử dụng ImageButton với hiệu ứng hover

    toggle_card_btn = ImageButton(
        30, HEIGHT - 80, 200, 50,
        "Ẩn/Hiện bài", FONT,
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

        # Thời gian hiện tại
        now = pygame.time.get_ticks()

        # Nếu chưa có merchant hoặc đã quá 10 phút → tạo mới
        if merchant is None or now - last_merchant_spawn >= 600000:
            merchant = Merchant()
            truck_sound.play()
            last_merchant_spawn = now
            show_merchant = True



        # Animal drawing
        for animal in player.animals_on_field:
            animal.update()
            animal.draw(SCREEN)

        # Vẽ ảnh thanh công cụ
        SCREEN.blit(toolbar_image, (toolbar_x, toolbar_y))





        # Buttons rendering
        # for btn in [ toggle_card_btn]:
        #     btn.draw(SCREEN, mouse_pos)



        # --- VẼ HUD GÓC PHẢI TRÊN ---
        hud_width, hud_height = 250, 75
        hud_x = WIDTH - hud_width - 20
        hud_y = 20

        # Nền gỗ nâu trầm
        pygame.draw.rect(SCREEN, (95, 65, 40), (hud_x, hud_y, hud_width, hud_height), border_radius=8)

        # Viền vàng ánh cam
        pygame.draw.rect(SCREEN, (255, 200, 80), (hud_x, hud_y, hud_width, hud_height), 3, border_radius=8)

        # Vẽ icon coin
        SCREEN.blit(coin_image, (hud_x + 10, (hud_y + hud_height) / 2))

        # Vẽ số vàng (vàng sáng, đổ bóng nhẹ)
        gold_text = FONT.render(": "f'{player.gold}', True, (255, 255, 160))  # Vàng sáng nhẹ
        SCREEN.blit(gold_text, (hud_x + 40, hud_y + 2))

                        

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

        # selected_toolbar_index = 0
        if player.toolbar.slots:
            player.toolbar.slots[selected_toolbar_index].selected = True

        # ===================== GIAO DIỆN THƯƠNG GIA =====================
        merchant_buttons = []

        if show_merchant:
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

        if selecting and current_pos != (-1,-1):
            x1, y1 = start_pos
            x2, y2 = current_pos
            left = min(x1, x2)
            top = min(y1, y2)
            width = abs(x1 - x2)
            height = abs(y1 - y2)
            pygame.draw.rect(SCREEN, (0, 255, 0), (left, top, width, height), 2)
        if show_inventory: 
            SCREEN.blit(inventory_image, (inventory_x, inventory_y))
            for slot in player.inventory_position:
                slot.draw(SCREEN,FONT)
        # Vẽ ảnh thanh công cụ
        SCREEN.blit(toolbar_image, (toolbar_x, toolbar_y))
        #slot_toolbar
        for i, slot in enumerate(player.toolbar.slots):
            slot.selected = (i == selected_toolbar_index)
            slot.draw(SCREEN, FONT)
        if dragging_item:
            _, dragging_image, dragging_quantity = dragging_item
            if dragging_image:
                item_rect = dragging_image.image.get_rect(center=mouse_pos)
                SCREEN.blit(dragging_image.image, item_rect.topleft)
    
        if show_score_summary:
            confirm_btn.draw(SCREEN, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for animal in player.animals_on_field:
                    if animal.check_clicked(event.pos):
                        player.gold += animal.cost * 0.1
                        break  # chỉ click 1 con/lần
                # Scroll wheel interaction
                if event.button == 4:  # Scroll up
                    selected_toolbar_index = (selected_toolbar_index - 1) % len(player.toolbar.slots)
                elif event.button == 5:  # Scroll down
                    selected_toolbar_index = (selected_toolbar_index + 1) % len(player.toolbar.slots)
                if event.button == 3 :
                    start_pos = mouse_pos
                    selecting = True

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
                if show_merchant:
                    for item_box, item in merchant_buttons:  # Đổi từ (btn, item) sang (item_box, item)
                        # Kiểm tra click vào pot_image
                        if item_box.collidepoint(event.pos) and player.gold >= item.cost:
                            player.gold -= item.cost
                            if isinstance(item, Animal):
                                player.animals.append(item.name)
                                player.animals_on_field.append(item)
                            elif isinstance(item, Item):
                                player.inventory.add_item(item)  # thêm vào túi đồ
                            merchant.items.remove(item)
                            break
            
                if toggle_card_btn.is_clicked(event):
                    show_card_frame = not show_card_frame
                if event.button == 1:  # Chuột trái
                    if show_inventory:
                        for slot in player.inventory.slots:
                            if slot.is_hovered(mouse_pos) and slot.item:
                                dragging_item = (slot, slot.item, slot.quantity)
                                slot.clear()
                                break
                    if not dragging_item:
                        for slot in player.toolbar.slots:
                            if slot.is_hovered(mouse_pos) and slot.item:
                                dragging_item = (slot, slot.item, slot.quantity)
                                slot.clear()
                                break
            elif event.type == pygame.MOUSEMOTION:
                if selecting:
                    current_pos = mouse_pos
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    selecting = False
                    end_pos = mouse_pos
                    current_pos = (-1,-1)
                    # Tính vùng chọn
                    x1, y1 = start_pos
                    x2, y2 = end_pos
                    left = min(x1, x2)
                    top = min(y1, y2)
                    width = abs(x1 - x2)
                    height = abs(y1 - y2)
                    selection_rect = pygame.Rect(left, top, width, height)

                    # Kiểm tra vật phẩm nào nằm trong vùng
                    collected_items = []
                    for item in yard:
                        if selection_rect.colliderect(item.rect):
                            if not player.inventory.add_item(item):  # nếu inventory đầy
                               player.inventory.add_item(item)
                            collected_items.append(item)

                    # Xóa các item đã thu thập khỏi yard
                    for item in collected_items:
                        yard.remove(item)      
                if event.button == 1 and dragging_item:
                    from_slot, item, quantity = dragging_item
                    placed = False

                    for slot in player.inventory.slots:
                        if slot.is_hovered(mouse_pos):
                            if slot.item is None:
                                slot.item = item
                                slot.quantity = quantity
                            elif slot.item.name == item.name:
                                from_slot.item = None
                                slot.quantity += quantity
                            elif slot.item.name != item.name:
                                from_slot.item = slot.item
                                from_slot.quantity = slot.quantity
                                slot.item = item
                                slot.quantity = quantity
                            placed = True
                            break
                    if not placed:
                        for slot in player.toolbar.slots:
                            if slot.is_hovered(mouse_pos):
                                if slot.item is None:
                                    slot.item = item
                                    slot.quantity = quantity
                                elif slot.item.name == item.name:
                                    slot.quantity += quantity
                                elif slot.item.name != item.name:
                                    print("yes")
                                    from_slot.item = slot.item
                                    from_slot.quantity = slot.quantity
                                    slot.item = item
                                    slot.quantity = quantity
                                placed = True
                                break
                    if not placed:
                        # Nếu không thả được vào slot nào → trả lại chỗ cũ
                        from_slot.item = item
                        from_slot.quantity = quantity

                    dragging_item = None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    show_inventory = not show_inventory
                elif event.key == pygame.K_m:
                    show_merchant = not show_merchant
                elif event.key == pygame.K_LEFT:
                    return "go_to_farming", player, current_day
                elif event.key == pygame.K_ESCAPE:
                    return "back_to_menu"
                elif event.key == pygame.K_s:
                    # Bán item đang được kéo
                    if dragging_item:
                        from_slot, item, quantity = dragging_item
                        sell_price = 5 * quantity * 0.075  # Bán giá nửa giá gốc
                        player.gold += sell_price
                        dragging_item = None
                        sell_sound.play()  # 🔊 Phát âm thanh

        pygame.display.update()
        clock.tick(60)