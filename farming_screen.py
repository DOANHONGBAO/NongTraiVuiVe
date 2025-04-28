import pygame
import sys
import pytmx
from GUI import ImageButton
from plant import Plant,Field
import random
from items import Slot,Inventory,HarvestNotification
def create_plants():
    # Hình ảnh các giai đoạn phát triển của các loại cây
    carrot_images = [pygame.image.load(f"assets/plants/carrot/carrot{i}.png").convert_alpha() for i in range(4)]
    corn_images = [pygame.image.load(f"assets/plants/corn/corn{i}.png").convert_alpha() for i in range(4)]
    straw_berry_images = [pygame.image.load(f"assets/plants/straw_berry/straw_berry{i}.png").convert_alpha() for i in range(4)]
    carbage_images = [pygame.image.load(f"assets/plants/carbage/carbage{i}.png").convert_alpha() for i in range(4)]
    rice_images = [pygame.image.load(f"assets/plants/rice/rice{i}.png").convert_alpha() for i in range(4)]
    # Tạo các cây
    plants = [
        Plant(name="Carrot", x=0, y=0, growth_stages=[0, 1, 2, 3], growth_time=4000, images=carrot_images,index = 0,indexob = 2),
        Plant(name="Corn", x=0, y=0, growth_stages=[0, 1, 2, 3], growth_time=10000, images=corn_images,indexob = 7),
        Plant(name="Straw_berry", x=0, y=0, growth_stages=[0, 1, 2, 3], growth_time=10000, images=straw_berry_images, indexob = 4),
        Plant(name="Carbage", x=0, y=0, growth_stages=[0, 1, 2, 3], growth_time=10000, images=carbage_images, indexob = 28),
        Plant(name="Rice", x=0, y=0, growth_stages=[0, 1, 2, 3], growth_time=10000, images=ric, indexob = 3),
    ]
    
    return plants


yard = []

# Tạo các thửa ruộng
fields = [
    # Tầng 1
    Field(321, 165, 478, 317, 4, 4),  # field1
    Field(482, 166, 638, 314, 4, 4),  # field2
    Field(643, 163, 799, 315, 4, 4),  # field3
    Field(803, 163, 959, 315, 4, 4),  # field4
    Field(964, 164, 1119, 314, 4, 4), # field5
    Field(1123, 163, 1279, 314, 4, 4), # field6

    # Tầng 2 (y - 10)
    Field(321, 325, 478, 477, 4, 4),  # field7
    Field(482, 325, 638, 477, 4, 4),  # field8
    Field(643, 325, 799, 477, 4, 4),  # field9
    Field(803, 325, 959, 477, 4, 4),  # field10
    Field(964, 325, 1119,477, 4, 4), # field11
    Field(1123,325, 1279,477, 4, 4), # field12

    # Tầng 3 (y - 10 tiếp)
    Field(321, 485, 478, 637, 4, 4),  # field13
    Field(482, 485, 638, 637, 4, 4),  # field14
    Field(643, 485, 799, 637, 4, 4),  # field15
    Field(803, 485, 959, 637, 4, 4),  # field16
    Field(964, 485, 1119,637, 4, 4), # field17
    Field(1123,485, 1279,637, 4, 4), # field18

    # Tầng 4 (y - 10 tiếp lần nữa)
    Field(321, 645, 478, 797, 4, 4),  # field19
    Field(482, 645, 638, 797, 4, 4),  # field20
    Field(643, 645, 799, 797, 4, 4),  # field21
    Field(803, 645, 959, 797, 4, 4),  # field22
    Field(964, 645, 1119,797, 4, 4), # field23
    Field(1123,645, 1279,797, 4, 4), # field24
]

toolbar_width = 800
toolbar_height = 126
# Vị trí để đặt ảnh thanh công cụ ở giữa dưới
toolbar_x = (1900 - toolbar_width) // 2
toolbar_y = 1000 - toolbar_height
inventory_x = toolbar_x
inventory_y = toolbar_y - 460
toolbar_slots = []
raw_positions = [
    ((578, 903), (645, 966)),
    ((655, 904), (719, 966)),
    ((729, 906), (792, 968)),
    ((804, 905), (868, 966)),
    ((880, 903), (941, 966)),
    ((955, 903), (1019, 965)),
    ((1031, 904), (1094, 963)),
    ((1105, 905), (1171, 969)),
    ((1178, 901), (1246, 970)),
    ((1259, 906), (1322, 970))
]

raw_inventory_position = [
    ((578, 444), (652, 516)), ((652, 444), (726, 516)), ((726, 444), (800, 516)), ((800, 444), (874, 516)), ((874, 444), (948, 516)),
    ((948, 444), (1022, 516)), ((1022, 444), (1096, 516)), ((1096, 444), (1170, 516)), ((1170, 444), (1244, 516)), ((1244, 444), (1318, 516)),

    ((578, 516), (652, 588)), ((652, 516), (726, 588)), ((726, 516), (800, 588)), ((800, 516), (874, 588)), ((874, 516), (948, 588)),
    ((948, 516), (1022, 588)), ((1022, 516), (1096, 588)), ((1096, 516), (1170, 588)), ((1170, 516), (1244, 588)), ((1244, 516), (1318, 588)),

    ((578, 588), (652, 660)), ((652, 588), (726, 660)), ((726, 588), (800, 660)), ((800, 588), (874, 660)), ((874, 588), (948, 660)),
    ((948, 588), (1022, 660)), ((1022, 588), (1096, 660)), ((1096, 588), (1170, 660)), ((1170, 588), (1244, 660)), ((1244, 588), (1318, 660)),

    ((578, 660), (652, 734)), ((652, 660), (726, 734)), ((726, 660), (800, 734)), ((800, 660), (874, 734)), ((874, 660), (948, 734)),
    ((948, 660), (1022, 734)), ((1022, 660), (1096, 734)), ((1096, 660), (1170, 734)), ((1170, 660), (1244, 734)), ((1244, 660), (1318, 734)),

    ((578, 734), (652, 808)), ((652, 734), (726, 808)), ((726, 734), (800, 808)), ((800, 734), (874, 808)), ((874, 734), (948, 808)),
    ((948, 734), (1022, 808)), ((1022, 734), (1096, 808)), ((1096, 734), (1170, 808)), ((1170, 734), (1244, 808)), ((1244, 734), (1318, 808)),
]


inventory_position = [Slot(topleft,bottomright) for topleft,bottomright in raw_inventory_position] 
inventory = Inventory(inventory_position)

slot_positions = [Slot(topleft, bottomright) for topleft, bottomright in raw_positions]
toolbar = Inventory(slot_positions)

def farming_screen(SCREEN, WIDTH, HEIGHT, FONT, BIG_FONT, COLORS, player, current_day,clock):
    BUTTON_WIDTH, BUTTON_HEIGHT = 300, 90
    plants = create_plants()
    harvest_notifications = []
    # Biến lưu trạng thái kéo chọn vùng
    show_inventory = False
    selecting = False
    start_pos = (0, 0)
    current_pos = (-1, -1)
    selection_rect = None
    dragging_item = None
    # Load hình ảnh nút
    toolbar_image = pygame.image.load("assets/images/toolbar.png").convert_alpha()
    image_normal = pygame.image.load("assets/GUI/ButtonsText/ButtonText_Large_GreyOutline_Round.png").convert_alpha()
    image_hover = pygame.image.load("assets/GUI/ButtonsText/ButtonText_Large_Orange_Round.png").convert_alpha()
    image_btn_see_inventory = pygame.image.load("assets/GUI/ButtonsIcons/IconButton_Large_Circle.png").convert_alpha()
    image_see_inventory_hover = pygame.image.load("assets/GUI/ButtonsIcons/IconButton_Large_GreyOutline_Circle.png").convert_alpha()

    # Tạo nút quay lại bằng ImageButton có hiệu ứng hover
    back_btn = ImageButton(
        WIDTH - BUTTON_WIDTH - 30, HEIGHT // 2 - 50,
        BUTTON_WIDTH, BUTTON_HEIGHT,
        "Quay lại Game", FONT,
        (255, 255, 255),  # màu chữ thường
        image_normal, image_hover,
        hover_text_color=(255, 255, 0)  # màu chữ hover
    )
    see_inventory_btn = ImageButton(
        1370, 883, 100, 100,
        "", FONT,
        (255, 255, 255),
        image_btn_see_inventory, image_see_inventory_hover,
        hover_text_color=(255, 255, 0)
    )
    
    # Load bản đồ TMX
    tmx_data = pytmx.load_pygame("assets/tiles/background_farm.tmx")
    inventory_image = pygame.image.load("assets/images/inventory.png").convert_alpha()
    
    selected_plant = plants[3]  # Biến lưu cây được chọn để trồng

    while True:
        mouse_pos = pygame.mouse.get_pos()
        SCREEN.fill(COLORS["LIGHT_GREEN"])
        
        # ===== VẼ BẢN ĐỒ =====
        for layer in tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, tile in layer:
                    tile_image = tmx_data.get_tile_image_by_gid(tile)
                    if tile_image:
                        SCREEN.blit(tile_image, (x * tmx_data.tilewidth, y * tmx_data.tileheight))

        # ===== VẼ GIAO DIỆN =====
        title_text = BIG_FONT.render("Khu Trồng Trọt", True, COLORS["BROWN"])
        SCREEN.blit(title_text, (WIDTH // 2 - 150, 50))

        gold_text = FONT.render(f"Vàng: {player.gold}", True, COLORS["YELLOW"])
        SCREEN.blit(gold_text, (30, 150))

        farm_text = FONT.render(f"Động vật: {len(player.animals)} | Thức ăn: {len(player.food)}", True, COLORS["BLACK"])
        SCREEN.blit(farm_text, (30, 200))

        day_text = FONT.render(f"Ngày: {current_day}", True, COLORS["BLACK"])
        SCREEN.blit(day_text, (30, 250))


        # Vẽ các cây đã trồng trong các thửa ruộng
        for field in fields:
            if field.plants:
                # Nếu tất cả cây trong field đều chín
                if all(plant.is_ready_to_harvest() for plant in field.plants):
                    already_has_notification = any(
                        hasattr(noti, "field_id") and noti.field_id == id(field) for noti in harvest_notifications
                    )
                    if not already_has_notification:
                        # Nếu chưa có noti thì tạo mới
                        first_plant = field.plants[0]
                        noti = HarvestNotification(first_plant.images[-1])
                        noti.field_id = id(field)
                        noti.x = field.rect.centerx
                        noti.y = field.rect.top - 30
                        harvest_notifications.append(noti)
            else:
                # Nếu field.plants == [] (đã thu hoạch hết) ➔ Xóa noti của field này
                harvest_notifications = [n for n in harvest_notifications if not (hasattr(n, "field_id") and n.field_id == id(field))]

            for plant in field.plants:
                plant.update(clock.get_time())
                plant.draw(SCREEN)
        # Update và Draw tất cả harvest notifications
        for noti in harvest_notifications:
            # noti.update()  # nhớ chia 1000 để ra giây
            noti.draw(SCREEN)

        # Xóa noti hết hạn
        harvest_notifications = [n for n in harvest_notifications if n.timer > 0]

        for item in yard:
            item.draw(SCREEN)
            item.update()

        if selecting and current_pos != (-1,-1):
            x1, y1 = start_pos
            x2, y2 = current_pos
            left = min(x1, x2)
            top = min(y1, y2)
            width = abs(x1 - x2)
            height = abs(y1 - y2)
            pygame.draw.rect(SCREEN, (0, 255, 0), (left, top, width, height), 2)   
        # Buttons rendering
        for btn in [back_btn,see_inventory_btn]:
            btn.draw(SCREEN, mouse_pos)
        if show_inventory: 
            SCREEN.blit(inventory_image, (inventory_x, inventory_y))
            for slot in inventory_position:
                slot.draw(SCREEN,FONT)
        # Vẽ ảnh thanh công cụ
        SCREEN.blit(toolbar_image, (toolbar_x, toolbar_y))
        #slot_toolbar
        for slot in slot_positions:
            slot.draw(SCREEN,FONT)
        if dragging_item:
            _, dragging_image, dragging_quantity = dragging_item
            if dragging_image:
                item_rect = dragging_image.image.get_rect(center=mouse_pos)
                SCREEN.blit(dragging_image.image, item_rect.topleft)
    
        # ===== XỬ LÝ SỰ KIỆN =====
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # print(mouse_pos)
                if event.button == 3 :
                    start_pos = mouse_pos
                    selecting = True
                #Giả sử bạn có object `selected_plant` để trồng lại
                if not show_inventory : 
                    for field in fields:
                        if field.is_clicked(mouse_pos) and event.button == 1:
                            field.plant_crops(selected_plant, selected_plant.images)
                            dropped = field.try_harvest()
                            yard.extend(dropped)
                if see_inventory_btn.is_clicked(event):
                    show_inventory = not show_inventory
                if event.button == 1:  # Chuột trái
                    if show_inventory:
                        for slot in inventory.slots:
                            if slot.is_hovered(mouse_pos) and slot.item:
                                dragging_item = (slot, slot.item, slot.quantity)
                                slot.clear()
                                break
                    if not dragging_item:
                        for slot in toolbar.slots:
                            if slot.is_hovered(mouse_pos) and slot.item:
                                dragging_item = (slot, slot.item, slot.quantity)
                                slot.clear()
                                break
                # Kiểm tra nếu click vào nút "Quay lại Game"
                if back_btn.is_clicked(event):  # ✅ Sửa lỗi truyền tuple
                    return "back_to_gameplay"
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
                            if not inventory.add_item(item):  # nếu inventory đầy
                                inventory.add_item(item)
                            collected_items.append(item)

                    # Xóa các item đã thu thập khỏi yard
                    for item in collected_items:
                        yard.remove(item)      
                if event.button == 1 and dragging_item:
                    from_slot, item, quantity = dragging_item
                    placed = False
                    if show_inventory:
                        for slot in inventory.slots:
                            if slot.is_hovered(mouse_pos):
                                if slot.item is None:
                                    slot.item = item
                                    slot.quantity = quantity
                                elif slot.item.name == item.name:
                                    slot.quantity += quantity
                                placed = True
                                break
                    if not placed:
                        for slot in toolbar.slots:
                            if slot.is_hovered(mouse_pos):
                                if slot.item is None:
                                    slot.item = item
                                    slot.quantity = quantity
                                elif slot.item.name == item.name:
                                    slot.quantity += quantity
                                placed = True
                                break
                    if not placed:
                        # Nếu không thả được vào slot nào → trả lại chỗ cũ
                        from_slot.item = item
                        from_slot.quantity = quantity

                    dragging_item = None
        
        pygame.display.update()
        clock.tick(60)
