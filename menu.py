import pygame
import sys
import math
import random
import time
import json
import os
from GUI import ImageButton
from transitions import FadeTransition, SlideTransition, ZoomTransition, PixelateTransition
from settings_manager import Settings, settings_screen

# Tạo placeholder cho các hình ảnh không tìm thấy
def create_placeholder_image(size=(800, 600), color=(100, 100, 150)):
    surf = pygame.Surface(size, pygame.SRCALPHA)
    pygame.draw.rect(surf, color, (0, 0, size[0], size[1]), 0)
    
    # Vẽ một số họa tiết để nhận diện là placeholder
    pygame.draw.line(surf, (200, 200, 220), (0, 0), (size[0], size[1]), 5)
    pygame.draw.line(surf, (200, 200, 220), (0, size[1]), (size[0], 0), 5)
    
    # Tạo hiệu ứng gradient
    for i in range(0, size[1], 4):
        alpha = 150 - i // 4
        if alpha < 0:
            alpha = 0
        line_color = (100, 100, 150, alpha)
        pygame.draw.line(surf, line_color, (0, i), (size[0], i), 1)
    
    return surf

def load_image_safely(path, alt_path=None, size=None):
    """Tải hình ảnh an toàn với xử lý lỗi và placeholder"""
    try:
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
        elif alt_path and os.path.exists(alt_path):
            img = pygame.image.load(alt_path).convert_alpha()
        else:
            print(f"Lỗi khi tải hình ảnh: No file '{path}' found in working directory '{os.getcwd()}'.")
            # Tạo hình ảnh tạm thời
            if size:
                return create_placeholder_image(size)
            else:
                return create_placeholder_image()
                
        # Nếu cần resize
        if size:
            img = pygame.transform.scale(img, size)
        
        return img
    except Exception as e:
        print(f"Lỗi khi tải hình {path}: {e}")
        if size:
            return create_placeholder_image(size)
        else:
            return create_placeholder_image()

def start_screen(screen, width, height, font, big_font, colors, clock):
    """
    Màn hình menu được nâng cấp với các hiệu ứng chuyển động và thiết kế hình ảnh đẹp hơn.
    """
    # Khởi tạo cài đặt
    game_settings = Settings()
    
    # Khởi tạo hiệu ứng chuyển tiếp
    transition = None
    transition_active = False
    transition_target = None  # Màn hình đích sau khi chuyển tiếp
    # Biến cho hiệu ứng và hoạt ảnh
    title_y_offset = -200  # Bắt đầu từ ngoài màn hình
    title_target_y = height // 3
    button_alpha = 0
    particles = []
    floating_elements = []
    button_scale = 1.0
    button_scale_direction = 0.0005
    
    # Đặt thời gian bắt đầu
    start_time = pygame.time.get_ticks()
    
    # Tải và xử lý hình nền
    try:
        background_img = pygame.image.load("assets/images/BG.jpeg").convert()
        background_img = pygame.transform.scale(background_img, (width, height))
        
        # Tạo lớp overlay mờ để tạo chiều sâu
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 30))  # Màu đen với độ trong suốt
    except Exception as e:
        print(f"Lỗi khi tải hình nền: {e}")
        background_img = pygame.Surface((width, height))
        background_img.fill(colors["GREEN"])
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)

    # Tải hình ảnh tiêu đề
    try:
        title_img = pygame.image.load("assets/images/title_only.png").convert_alpha()
        title_img = pygame.transform.scale(title_img, (
            int(title_img.get_width() * 0.7),
            int(title_img.get_height() * 0.7)
        ))
    except Exception as e:
        print(f"Lỗi khi tải hình tiêu đề: {e}")
        title_img = pygame.Surface((600, 150), pygame.SRCALPHA)
        title_text = big_font.render("NÔNG TRẠI VUI VẺ", True, colors["YELLOW"])
        title_img.blit(title_text, (title_img.get_width()//2 - title_text.get_width()//2, 
                                   title_img.get_height()//2 - title_text.get_height()//2))

    # Tải hình nút chơi
    try:
        play_img = pygame.image.load("assets/images/play_button_only.png").convert_alpha()
        play_img_hover = pygame.image.load("assets/images/play_button_hover.png").convert_alpha()
    except Exception as e:
        print(f"Lỗi khi tải hình nút: {e}")
        # Tạo nút chơi mặc định nếu không tải được
        play_img = pygame.Surface((200, 80), pygame.SRCALPHA)
        pygame.draw.rect(play_img, colors["DARK_GREEN"], (0, 0, 200, 80), border_radius=15)
        play_text = font.render("CHƠI NGAY", True, colors["WHITE"])
        play_img.blit(play_text, (play_img.get_width()//2 - play_text.get_width()//2, 
                                 play_img.get_height()//2 - play_text.get_height()//2))
        play_img_hover = pygame.Surface((200, 80), pygame.SRCALPHA)
        pygame.draw.rect(play_img_hover, colors["GREEN"], (0, 0, 200, 80), border_radius=15)
        play_img_hover.blit(play_text, (play_img.get_width()//2 - play_text.get_width()//2, 
                                       play_img.get_height()//2 - play_text.get_height()//2))

    # Tạo các yếu tố trang trí
    decorative_elements = create_decorative_elements(width, height)
    
    # Tạo các button chính
    button_width = int(play_img.get_width() * 0.7)
    button_height = int(play_img.get_height() * 0.7)
    play_btn = ImageButton(
        width // 2 - button_width // 2, int(height // 1.5) - button_height // 2,
        button_width, button_height,
        "", font, (0, 0, 0),
        play_img, play_img_hover
    )
    
    # Tạo các button phụ (Cài đặt, Thông tin, v.v.)
    # Tạo nút tròn nhỏ cho cài đặt
    settings_img = pygame.Surface((60, 60), pygame.SRCALPHA)
    settings_img_hover = pygame.Surface((60, 60), pygame.SRCALPHA)
    
    # Vẽ biểu tượng cài đặt
    pygame.draw.circle(settings_img, colors["DARK_GREEN"], (30, 30), 30)
    pygame.draw.circle(settings_img, colors["WHITE"], (30, 30), 26, 2)
    # Vẽ bánh răng
    for i in range(8):
        angle = i * 45
        x = 30 + 15 * math.cos(math.radians(angle))
        y = 30 + 15 * math.sin(math.radians(angle))
        pygame.draw.circle(settings_img, colors["WHITE"], (int(x), int(y)), 4)
    
    # Phiên bản hover
    pygame.draw.circle(settings_img_hover, colors["GREEN"], (30, 30), 30)
    pygame.draw.circle(settings_img_hover, colors["YELLOW"], (30, 30), 26, 2)
    for i in range(8):
        angle = i * 45
        x = 30 + 15 * math.cos(math.radians(angle))
        y = 30 + 15 * math.sin(math.radians(angle))
        pygame.draw.circle(settings_img_hover, colors["YELLOW"], (int(x), int(y)), 4)
    
    settings_btn = ImageButton(
        width - 80, 30, 60, 60,
        "", font, (0, 0, 0),
        settings_img, settings_img_hover
    )
    
    # Tạo nút thông tin
    info_img = pygame.Surface((60, 60), pygame.SRCALPHA)
    info_img_hover = pygame.Surface((60, 60), pygame.SRCALPHA)
    
    # Vẽ biểu tượng thông tin
    pygame.draw.circle(info_img, colors["DARK_GREEN"], (30, 30), 30)
    pygame.draw.circle(info_img, colors["WHITE"], (30, 30), 26, 2)
    info_text = font.render("i", True, colors["WHITE"])
    info_img.blit(info_text, (26, 16))
    
    # Phiên bản hover
    pygame.draw.circle(info_img_hover, colors["GREEN"], (30, 30), 30)
    pygame.draw.circle(info_img_hover, colors["YELLOW"], (30, 30), 26, 2)
    info_text_hover = font.render("i", True, colors["YELLOW"])
    info_img_hover.blit(info_text_hover, (26, 16))
    
    info_btn = ImageButton(
        width - 80, 100, 60, 60,
        "", font, (0, 0, 0),
        info_img, info_img_hover
    )
    
    # Tạo các phần tử nổi (mây, chim, lá) cho hiệu ứng động
    for _ in range(8):
        x = random.randint(0, width)
        y = random.randint(0, height // 2)
        size = random.randint(30, 80)
        speed = random.uniform(0.2, 0.8)
        amplitude = random.randint(10, 30)
        phase = random.uniform(0, 2 * math.pi)
        element_type = random.choice(["cloud", "bird", "leaf"])
        floating_elements.append({
            "x": x, "y": y, "size": size, "speed": speed,
            "amplitude": amplitude, "phase": phase, "type": element_type,
            "original_y": y
        })
    
    # Biến để kiểm soát hoạt ảnh
    animation_done = False
    
    while True:
        current_time = pygame.time.get_ticks()
        delta_time = clock.get_time() / 1000.0  # Chuyển đổi sang giây
        mouse_pos = pygame.mouse.get_pos()
        
        # Hiệu ứng tiêu đề di chuyển vào (ease out)
        if title_y_offset < 0:
            elapsed = (current_time - start_time) / 1000.0  # giây
            progress = min(1.0, elapsed / 1.2)  # 1.2 giây cho hoạt ảnh
            # Ease out cubic: progress = 1 - (1 - progress)^3
            eased_progress = 1 - (1 - progress)**3
            title_y_offset = -200 * (1 - eased_progress)
        
        # Hiệu ứng làm mờ dần nút (sau khi hiệu ứng tiêu đề)
        if title_y_offset > -20 and button_alpha < 255:
            button_alpha = min(255, button_alpha + int(510 * delta_time))
            
        # Kiểm tra hoàn thành hoạt ảnh
        if title_y_offset >= 0 and button_alpha >= 255 and not animation_done:
            animation_done = True
            # Tạo các hạt một lần khi hoạt ảnh hoàn thành
            for _ in range(30):
                particles.append({
                    "x": width // 2,
                    "y": height // 3 + title_img.get_height() // 2,
                    "vx": random.uniform(-2, 2),
                    "vy": random.uniform(-3, -1),
                    "size": random.randint(3, 8),
                    "color": random.choice([colors["YELLOW"], colors["LIGHT_GREEN"], (255, 255, 255)]),
                    "life": random.uniform(1.0, 3.0)
                })
        
        # Hiệu ứng thay đổi kích thước nút
        if animation_done:
            button_scale += button_scale_direction
            if button_scale > 1.05:
                button_scale = 1.05
                button_scale_direction = -0.0005
            elif button_scale < 0.95:
                button_scale = 0.95
                button_scale_direction = 0.0005
        
        # Vẽ nền
        screen.blit(background_img, (0, 0))
        screen.blit(overlay, (0, 0))
        
        # Vẽ các phần tử trang trí
        for element in decorative_elements:
            screen.blit(element["surface"], element["pos"])
            
        # Cập nhật và vẽ các phần tử nổi
        for element in floating_elements:
            # Cập nhật vị trí với chuyển động hình sin
            element["phase"] += element["speed"] * delta_time
            element["y"] = element["original_y"] + math.sin(element["phase"]) * element["amplitude"]
            element["x"] -= element["speed"] * 15 * delta_time
            
            # Quay lại khi ra khỏi màn hình
            if element["x"] + element["size"] < 0:
                element["x"] = width + element["size"]
                element["original_y"] = random.randint(0, height // 2)
                
            # Vẽ phần tử dựa trên loại
            if element["type"] == "cloud":
                draw_cloud(screen, element["x"], element["y"], element["size"])
            elif element["type"] == "bird":
                draw_bird(screen, element["x"], element["y"], element["size"] // 2)
            elif element["type"] == "leaf":
                draw_leaf(screen, element["x"], element["y"], element["size"] // 3)
                
        # Hiển thị FPS nếu được bật trong cài đặt
        if game_settings.get("display", "show_fps"):
            fps = clock.get_fps()
            fps_font = pygame.font.SysFont('Arial', 20)
            fps_text = fps_font.render(f"FPS: {int(fps)}", True, (255, 255, 255))
            screen.blit(fps_text, (10, 10))
        
        # Cập nhật và vẽ các hạt
        for particle in particles[:]:
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]
            particle["vy"] += 0.1  # trọng lực
            particle["life"] -= delta_time
            
            if particle["life"] <= 0:
                particles.remove(particle)
            else:
                alpha = min(255, int(255 * particle["life"]))
                color = particle["color"][:3] + (alpha,)
                pygame.draw.circle(
                    screen, 
                    color, 
                    (int(particle["x"]), int(particle["y"])), 
                    int(particle["size"])
                )
        
        # Vẽ tiêu đề với vị trí hiện tại
        title_rect = title_img.get_rect(center=(width // 2, title_target_y + title_y_offset))
        title_shadow = title_img.copy()
        title_shadow.fill((0, 0, 0, 100), None, pygame.BLEND_RGBA_MULT)
        shadow_rect = title_shadow.get_rect(center=(width // 2 + 5, title_target_y + title_y_offset + 5))
        screen.blit(title_shadow, shadow_rect)  # Bóng đổ
        screen.blit(title_img, title_rect)
        
        # Vẽ nút chơi với hiệu ứng độ trong suốt
        if button_alpha < 255:
            button_surface = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
            temp_button = play_img.copy()
            temp_button.set_alpha(button_alpha)
            button_surface.blit(temp_button, (0, 0))
            screen.blit(button_surface, (play_btn.rect.x, play_btn.rect.y))
        else:
            # Vẽ nút với hiệu ứng thu phóng nhẹ
            scaled_width = int(button_width * button_scale)
            scaled_height = int(button_height * button_scale)
            x_offset = (scaled_width - button_width) // 2
            y_offset = (scaled_height - button_height) // 2
            
            # Vẽ hiệu ứng phát sáng cho nút
            glow_surface = pygame.Surface((scaled_width + 20, scaled_height + 20), pygame.SRCALPHA)
            pygame.draw.rect(
                glow_surface, 
                (*colors["YELLOW"], 40),  # Màu vàng bán trong suốt
                (0, 0, scaled_width + 20, scaled_height + 20),
                border_radius=20
            )
            screen.blit(
                glow_surface, 
                (play_btn.rect.x - x_offset - 10, play_btn.rect.y - y_offset - 10)
            )
            
            # Sau đó vẽ nút với hiệu ứng hover
            play_btn.draw(screen, mouse_pos)
        
        # Vẽ các nút phụ
        settings_btn.draw(screen, mouse_pos)
        info_btn.draw(screen, mouse_pos)
        
        # Vẽ văn bản chân trang
        current_year = time.strftime("%Y")
        footer_text = font.render(f"© {current_year} Nông Trại Vui Vẻ", True, (255, 255, 255))
        screen.blit(footer_text, (width - footer_text.get_width() - 20, height - footer_text.get_height() - 10))
        
        # Xử lý hiệu ứng chuyển tiếp
        if transition_active and transition:
            transition.update()
            transition.draw()
            
            if transition.is_done():
                transition_active = False
                # Nếu có màn hình đích, chuyển đến đó
                if transition_target == "play":
                    # Trả về True để bắt đầu game
                    return True
                elif transition_target == "exit":
                    # Thoát game
                    pygame.quit()
                    sys.exit()
                elif transition_target == "settings":
                    # Chuyển đến màn hình cài đặt và lấy kết quả trả về
                    saved, updated_settings = settings_screen(screen, width, height, font, big_font, colors, clock, game_settings)
                    if saved:
                        game_settings = updated_settings
        
        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and info_panel_visible:
                    info_panel_visible = False
            
            if animation_done and not transition_active:
                if play_btn.is_clicked(event):
                    # Bắt đầu hiệu ứng chuyển tiếp
                    transition = FadeTransition(0.7)
                    transition.start(screen)
                    transition_active = True
                    transition_target = "play"
                
                # if settings_btn.is_clicked(event):
                #     # Hiển thị màn hình cài đặt
                #     transition = SlideTransition(0.7, "left")
                    
                #     # Tạo một hàm để vẽ màn hình cài đặt cho hiệu ứng chuyển tiếp
                #     def draw_settings_screen(surface):
                #         settings_screen(surface, width, height, font, big_font, colors, clock, game_settings)
                    
                #     transition.start(screen, draw_settings_screen)
                #     transition_active = True
                #     transition_target = "settings"
                
                if info_btn.is_clicked(event):
                    # Hiển thị/ẩn màn hình thông tin
                    info_panel_visible = not info_panel_visible

        pygame.display.flip()
        clock.tick(60)

def create_decorative_elements(width, height):
    """Tạo các phần tử trang trí cho menu"""
    elements = []
    
    # Tạo surface cho các trang trí
    # 1. Trang trí lúa ở góc
    wheat_surf = pygame.Surface((150, 200), pygame.SRCALPHA)
    draw_wheat(wheat_surf, 75, 180, 150)
    elements.append({"surface": wheat_surf, "pos": (20, height - 200)})
    
    # 2. Lúa bên phải
    wheat_surf2 = pygame.Surface((150, 200), pygame.SRCALPHA)
    draw_wheat(wheat_surf2, 75, 180, 150)
    # Lật ngang
    wheat_surf2 = pygame.transform.flip(wheat_surf2, True, False)
    elements.append({"surface": wheat_surf2, "pos": (width - 170, height - 200)})
    
    # 3. Công cụ nông trại trang trí
    tools_surf = pygame.Surface((300, 100), pygame.SRCALPHA)
    draw_farm_tools(tools_surf, 150, 50)
    elements.append({"surface": tools_surf, "pos": (width - 320, 20)})
    
    # 4. Tạo hàng rào ở dưới
    fence_surf = pygame.Surface((width, 80), pygame.SRCALPHA)
    draw_fence(fence_surf, width, 40)
    elements.append({"surface": fence_surf, "pos": (0, height - 80)})
    
    return elements

def draw_wheat(surface, x, y, height):
    """Vẽ cọng lúa trang trí"""
    # Thân chính
    stem_color = (207, 176, 49)  # Màu vàng lúa mì
    pygame.draw.line(surface, stem_color, (x, y), (x, y - height), 3)
    
    # Hạt lúa
    grain_color = (235, 199, 64)  # Màu vàng sáng hơn
    grain_length = 25
    num_grains = 12
    
    for i in range(num_grains):
        y_pos = y - 40 - i * (height - 40) / num_grains
        angle = math.sin(i * 0.5) * 30 + 15  # Xen kẽ góc
        end_x = x + math.cos(math.radians(angle)) * grain_length
        end_y = y_pos + math.sin(math.radians(angle)) * grain_length
        
        # Vẽ hạt lúa như đường thẳng
        pygame.draw.line(surface, grain_color, (x, y_pos), (end_x, end_y), 2)
        
        # Vẽ ở phía bên kia
        end_x = x - math.cos(math.radians(angle)) * grain_length
        pygame.draw.line(surface, grain_color, (x, y_pos), (end_x, end_y), 2)

def draw_farm_tools(surface, x, y):
    """Vẽ công cụ nông trại trang trí"""
    # Vẽ cái xẻng
    fork_color = (139, 69, 19)  # Nâu
    # Cán
    pygame.draw.line(surface, fork_color, (x - 50, y + 40), (x - 50, y - 30), 4)
    # Răng
    for i in range(3):
        offset = (i - 1) * 15
        pygame.draw.line(surface, fork_color, (x - 50, y - 30), (x - 50 + offset, y - 50), 3)
    
    # Vẽ cái cuốc
    # Cán
    pygame.draw.line(surface, fork_color, (x + 50, y + 40), (x + 50, y - 20), 4)
    # Lưỡi
    pygame.draw.line(surface, (100, 100, 100), (x + 50, y - 20), (x + 80, y - 10), 5)

def draw_cloud(surface, x, y, size):
    """Vẽ đám mây trang trí"""
    cloud_color = (255, 255, 255, 100)  # Trắng bán trong suốt
    pygame.draw.ellipse(surface, cloud_color, (x, y, size, size // 2))
    pygame.draw.ellipse(surface, cloud_color, (x + size // 4, y - size // 4, size // 2, size // 2))
    pygame.draw.ellipse(surface, cloud_color, (x + size // 2, y, size // 2, size // 3))

def draw_bird(surface, x, y, size):
    """Vẽ hình bóng chim đơn giản"""
    bird_color = (60, 60, 60, 150)  # Xám đậm bán trong suốt
    # Vẽ cánh như cung
    pygame.draw.arc(surface, bird_color, (x, y, size, size), 0, math.pi, 2)
    pygame.draw.arc(surface, bird_color, (x + size//2, y, size, size), 0, math.pi, 2)

def draw_leaf(surface, x, y, size):
    """Vẽ chiếc lá đơn giản"""
    leaf_color = (50, 180, 50, 150)  # Xanh lá bán trong suốt
    points = [
        (x, y),
        (x + size//2, y - size),
        (x + size, y),
        (x + size//2, y + size//3)
    ]
    pygame.draw.polygon(surface, leaf_color, points)
    # Vẽ thân lá
    pygame.draw.line(surface, (100, 80, 0, 150), (x + size//2, y), (x + size//2, y + size//2), 2)

def draw_fence(surface, width, height):
    """Vẽ hàng rào trang trí ở dưới cùng"""
    fence_color = (120, 80, 40, 180)  # Nâu gỗ bán trong suốt
    post_width = 15
    post_spacing = 40
    post_height = height
    
    # Vẽ các cột hàng rào
    for x in range(0, width, post_spacing):
        pygame.draw.rect(surface, fence_color, (x, 0, post_width, post_height))
    
    # Vẽ thanh ngang
    pygame.draw.rect(surface, fence_color, (0, 10, width, 8))
    pygame.draw.rect(surface, fence_color, (0, 30, width, 8))
