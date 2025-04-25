import pygame
import sys
import pytmx
from GUI import ImageButton
from plant import Plant,Field

def create_plants():
    # Hình ảnh các giai đoạn phát triển của các loại cây
    carrot_images = [pygame.image.load(f"assets/plants/carrot/carrot{i}.png").convert_alpha() for i in range(4)]

    # Tạo các cây
    plants = [
        Plant(name="Carrot", x=0, y=0, growth_stages=[0, 1, 2, 3], growth_time=20000, images=carrot_images),
    ]
    
    return plants



# Tạo các thửa ruộng
fields = [
    Field(338, 179, 496, 440, 4, 7),  # field1 - 4 hàng, 4 cột
    Field(500, 181, 656, 442, 4, 7),  # field2 - 4 hàng, 4 cột
    Field(660, 179, 812, 439, 4, 7),  # field3 - 4 hàng, 4 cột
    Field(949, 178, 1104, 442, 4, 7),  # field4
    Field(1106, 183, 1261, 440, 4, 7),  # field5
    Field(1268, 178, 1423, 445, 4, 7),  # field6
    Field(339, 527, 495, 777, 4, 7),  # field7
    Field(502, 530, 651, 780, 4, 7),  # field8
    Field(656, 533, 816, 777, 4, 7),  # field9
    Field(946, 532, 1103, 776, 4, 7),  # field10
    Field(1106, 529, 1265, 778, 4, 7),  # field11
    Field(1266, 532, 1422, 781, 4, 7),  # field12
]

def farming_screen(SCREEN, WIDTH, HEIGHT, FONT, BIG_FONT, COLORS, player, current_day,clock):
    BUTTON_WIDTH, BUTTON_HEIGHT = 300, 90
    plants = create_plants()

    

    # Load hình ảnh nút
    image_normal = pygame.image.load("assets/GUI/ButtonsText/ButtonText_Large_GreyOutline_Round.png").convert_alpha()
    image_hover = pygame.image.load("assets/GUI/ButtonsText/ButtonText_Large_Orange_Round.png").convert_alpha()

    # Tạo nút quay lại bằng ImageButton có hiệu ứng hover
    back_btn = ImageButton(
        WIDTH - BUTTON_WIDTH - 30, HEIGHT // 2 - 50,
        BUTTON_WIDTH, BUTTON_HEIGHT,
        "Quay lại Game", FONT,
        (255, 255, 255),  # màu chữ thường
        image_normal, image_hover,
        hover_text_color=(255, 255, 0)  # màu chữ hover
    )
    
    # Load bản đồ TMX
    tmx_data = pytmx.load_pygame("assets/tiles/background_farm.tmx")
    
    selected_plant = plants[0]  # Biến lưu cây được chọn để trồng

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

        # Vẽ nút
        back_btn.draw(SCREEN, mouse_pos)
        
        # Vẽ các cây đã trồng trong các thửa ruộng
        for field in fields:
            for plant in field.plants:
                plant.update(clock.get_time())  # Cập nhật sự phát triển của cây
                plant.draw(SCREEN)  # Vẽ cây lên màn hình
        
        # ===== XỬ LÝ SỰ KIỆN =====
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                # Kiểm tra click vào thửa ruộng
                for field in fields:
                    if field.is_clicked(mouse_pos) and selected_plant is not None:
                        print(f"Đã click vào thửa ruộng {fields.index(field) + 1}")
                        # Trồng cây trong thửa ruộng đã click
                        field.plant_crops(selected_plant, selected_plant.images)  # Trồng cây trong thửa ruộng
                        # selected_plant = None  # Reset cây đã chọn sau khi trồng
                
                # Kiểm tra nếu click vào nút "Quay lại Game"
                if back_btn.is_clicked(event):  # ✅ Sửa lỗi truyền tuple
                    return "back_to_gameplay"
        
        pygame.display.update()
        clock.tick(60)
