import pygame
import sys
import json
import os
import math
from GUI import ImageButton

# Các cài đặt mặc định
DEFAULT_SETTINGS = {
    "audio": {
        "music_volume": 0.7,
        "sound_volume": 0.8,
        "mute": False
    },
    "display": {
        "fullscreen": False,
        "show_fps": False,
        "animations": True,
        "particles": True
    }
}

# Tệp lưu cài đặt
SETTINGS_FILE = "game_settings.json"

class Settings:
    """
    Lớp quản lý cài đặt game
    """
    def __init__(self):
        self.settings = self.load_settings()
    
    def load_settings(self):
        """Tải cài đặt từ tệp JSON hoặc sử dụng mặc định nếu không tìm thấy"""
        try:
            if os.path.exists(SETTINGS_FILE):
                with open(SETTINGS_FILE, 'r') as f:
                    loaded_settings = json.load(f)
                    # Đảm bảo tất cả các khóa đều tồn tại
                    merged_settings = DEFAULT_SETTINGS.copy()
                    for category in loaded_settings:
                        if category in merged_settings:
                            merged_settings[category].update(loaded_settings[category])
                    return merged_settings
        except Exception as e:
            print(f"Lỗi khi tải cài đặt: {e}")
        
        # Trả về cài đặt mặc định nếu không tải được
        return DEFAULT_SETTINGS.copy()
    
    def save_settings(self):
        """Lưu cài đặt vào tệp JSON"""
        try:
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(self.settings, f, indent=4)
            print("Đã lưu cài đặt thành công")
            return True
        except Exception as e:
            print(f"Lỗi khi lưu cài đặt: {e}")
            return False
    
    def get(self, category, key):
        """Lấy giá trị cài đặt"""
        try:
            return self.settings[category][key]
        except KeyError:
            # Trả về giá trị mặc định nếu không tìm thấy
            return DEFAULT_SETTINGS[category].get(key)
    
    def set(self, category, key, value):
        """Đặt giá trị cài đặt"""
        if category in self.settings and key in self.settings[category]:
            self.settings[category][key] = value
            return True
        return False
    
    def apply_audio_settings(self):
        """Áp dụng cài đặt âm thanh"""
        music_volume = self.get("audio", "music_volume")
        sound_volume = self.get("audio", "sound_volume")
        mute = self.get("audio", "mute")
        
        # Áp dụng âm lượng nhạc
        if mute:
            pygame.mixer.music.set_volume(0)
        else:
            pygame.mixer.music.set_volume(music_volume)
        
        # Đối với âm thanh hiệu ứng, bạn có thể đặt âm lượng khi phát
        return True
    
    def apply_display_settings(self):
        """Áp dụng cài đặt hiển thị"""
        fullscreen = self.get("display", "fullscreen")
        
        if fullscreen:
            pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            # Lấy kích thước mặc định từ tệp cấu hình hoặc sử dụng giá trị cố định
            pygame.display.set_mode((1915, 1020))
        
        return True


class Slider:
    """
    Thanh trượt để điều chỉnh giá trị
    """
    def __init__(self, x, y, width, height, min_val, max_val, current_val, 
                 bg_color, slider_color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.current_val = current_val
        self.bg_color = bg_color
        self.slider_color = slider_color
        self.hover_color = hover_color
        self.handle_rect = pygame.Rect(0, 0, 15, height + 10)
        self.update_handle_position()
        self.dragging = False
    
    def update_handle_position(self):
        """Cập nhật vị trí của tay cầm dựa trên giá trị hiện tại"""
        val_range = self.max_val - self.min_val
        if val_range == 0:
            position = 0
        else:
            position = (self.current_val - self.min_val) / val_range
        handle_x = self.rect.x + int(position * self.rect.width) - self.handle_rect.width // 2
        self.handle_rect.x = handle_x
        self.handle_rect.y = self.rect.y - 5  # Để tay cầm cao hơn một chút
    
    def draw(self, screen, font=None, label=None):
        """Vẽ thanh trượt và nhãn nếu được cung cấp"""
        # Vẽ nền
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=5)
        
        # Vẽ phần đã chọn
        filled_width = int((self.current_val - self.min_val) / (self.max_val - self.min_val) * self.rect.width)
        filled_rect = pygame.Rect(self.rect.x, self.rect.y, filled_width, self.rect.height)
        pygame.draw.rect(screen, self.slider_color, filled_rect, border_radius=5)
        
        # Vẽ tay cầm
        color = self.hover_color if self.is_handle_hovered() or self.dragging else self.slider_color
        pygame.draw.rect(screen, color, self.handle_rect, border_radius=7)
        
        # Vẽ nhãn nếu có
        if font and label:
            label_text = font.render(label, True, (255, 255, 255))
            screen.blit(label_text, (self.rect.x, self.rect.y - 30))
            
            # Vẽ giá trị hiện tại
            value_text = font.render(f"{int(self.current_val * 100)}%", True, (255, 255, 255))
            screen.blit(value_text, (self.rect.right + 10, self.rect.y))
    
    def is_handle_hovered(self):
        """Kiểm tra xem chuột có đang di chuyển qua tay cầm không"""
        mouse_pos = pygame.mouse.get_pos()
        return self.handle_rect.collidepoint(mouse_pos)
    
    def handle_event(self, event):
        """Xử lý sự kiện chuột cho thanh trượt"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_handle_hovered() or self.rect.collidepoint(event.pos):
                self.dragging = True
                # Cập nhật giá trị dựa trên vị trí nhấp chuột
                self.update_value(event.pos[0])
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            # Cập nhật giá trị khi kéo
            self.update_value(event.pos[0])
    
    def update_value(self, x_pos):
        """Cập nhật giá trị dựa trên vị trí x của chuột"""
        rel_x = max(0, min(x_pos - self.rect.x, self.rect.width))
        self.current_val = self.min_val + (rel_x / self.rect.width) * (self.max_val - self.min_val)
        self.update_handle_position()


class Toggle:
    """
    Nút bật/tắt cho các cài đặt boolean
    """
    def __init__(self, x, y, width, height, is_on, inactive_color, active_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.is_on = is_on
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.handle_rect = pygame.Rect(0, 0, height - 4, height - 4)
        self.update_handle_position()
    
    def update_handle_position(self):
        """Cập nhật vị trí của tay cầm dựa trên trạng thái hiện tại"""
        if self.is_on:
            self.handle_rect.x = self.rect.x + self.rect.width - self.handle_rect.width - 2
        else:
            self.handle_rect.x = self.rect.x + 2
        self.handle_rect.y = self.rect.y + 2
    
    def draw(self, screen, font=None, label=None):
        """Vẽ nút bật/tắt và nhãn nếu được cung cấp"""
        # Vẽ nền
        color = self.active_color if self.is_on else self.inactive_color
        pygame.draw.rect(screen, color, self.rect, border_radius=self.rect.height // 2)
        
        # Vẽ tay cầm
        pygame.draw.ellipse(screen, (255, 255, 255), self.handle_rect)
        
        # Vẽ nhãn nếu có
        if font and label:
            label_text = font.render(label, True, (255, 255, 255))
            screen.blit(label_text, (self.rect.x - label_text.get_width() - 10, self.rect.y + 5))
            
            # Vẽ trạng thái
            state_text = font.render("BẬT" if self.is_on else "TẮT", True, (255, 255, 255))
            screen.blit(state_text, (self.rect.right + 10, self.rect.y + 5))
    
    def handle_event(self, event):
        """Xử lý sự kiện chuột cho nút bật/tắt"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_on = not self.is_on
                self.update_handle_position()
                return True
        return False


def settings_screen(screen, width, height, font, big_font, colors, clock, current_settings=None):
    """
    Hiển thị màn hình cài đặt
    """
    # Sử dụng cài đặt hiện tại hoặc tạo mới
    settings = current_settings if current_settings else Settings()
    
    # Tạo màu nền gradient
    background = pygame.Surface((width, height))
    for y in range(height):
        # Màu gradient từ xanh đậm đến xanh nhạt
        color = (0, 100 + (y * 50 // height), 50 + (y * 100 // height))
        pygame.draw.line(background, color, (0, y), (width, y))
    
    # Tạo các bề mặt bán trong suốt cho các phần
    panel_width = 800
    panel_height = 500
    panel_x = (width - panel_width) // 2
    panel_y = (height - panel_height) // 2
    
    panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
    panel.fill((0, 0, 0, 180))  # Bán trong suốt
    
    # Tạo các thanh trượt âm lượng
    music_slider = Slider(
        panel_x + 200, panel_y + 100, 300, 20, 
        0.0, 1.0, settings.get("audio", "music_volume"),
        (100, 100, 100), (0, 200, 100), (0, 255, 150)
    )
    
    sound_slider = Slider(
        panel_x + 200, panel_y + 160, 300, 20, 
        0.0, 1.0, settings.get("audio", "sound_volume"),
        (100, 100, 100), (0, 200, 100), (0, 255, 150)
    )
    
    # Tạo các nút bật/tắt
    mute_toggle = Toggle(
        panel_x + 400, panel_y + 220, 60, 30,
        settings.get("audio", "mute"),
        (100, 100, 100), (0, 200, 100)
    )
    
    fullscreen_toggle = Toggle(
        panel_x + 400, panel_y + 280, 60, 30,
        settings.get("display", "fullscreen"),
        (100, 100, 100), (0, 200, 100)
    )
    
    fps_toggle = Toggle(
        panel_x + 400, panel_y + 340, 60, 30,
        settings.get("display", "show_fps"),
        (100, 100, 100), (0, 200, 100)
    )
    
    animations_toggle = Toggle(
        panel_x + 400, panel_y + 400, 60, 30,
        settings.get("display", "animations"),
        (100, 100, 100), (0, 200, 100)
    )
    
    # Tạo các nút
    back_img = pygame.Surface((200, 60), pygame.SRCALPHA)
    pygame.draw.rect(back_img, colors["DARK_GREEN"], (0, 0, 200, 60), border_radius=15)
    back_text = font.render("QUAY LẠI", True, colors["WHITE"])
    back_img.blit(back_text, (back_img.get_width()//2 - back_text.get_width()//2, 
                           back_img.get_height()//2 - back_text.get_height()//2))
    
    back_img_hover = pygame.Surface((200, 60), pygame.SRCALPHA)
    pygame.draw.rect(back_img_hover, colors["GREEN"], (0, 0, 200, 60), border_radius=15)
    back_img_hover.blit(back_text, (back_img_hover.get_width()//2 - back_text.get_width()//2, 
                               back_img_hover.get_height()//2 - back_text.get_height()//2))
    
    back_btn = ImageButton(
        panel_x + 100, panel_y + panel_height - 80, 200, 60,
        "", font, (255, 255, 255),
        back_img, back_img_hover
    )
    
    save_img = pygame.Surface((200, 60), pygame.SRCALPHA)
    pygame.draw.rect(save_img, colors["DARK_GREEN"], (0, 0, 200, 60), border_radius=15)
    save_text = font.render("LƯU", True, colors["WHITE"])
    save_img.blit(save_text, (save_img.get_width()//2 - save_text.get_width()//2, 
                           save_img.get_height()//2 - save_text.get_height()//2))
    
    save_img_hover = pygame.Surface((200, 60), pygame.SRCALPHA)
    pygame.draw.rect(save_img_hover, colors["GREEN"], (0, 0, 200, 60), border_radius=15)
    save_img_hover.blit(save_text, (save_img_hover.get_width()//2 - save_text.get_width()//2, 
                               save_img_hover.get_height()//2 - save_text.get_height()//2))
    
    save_btn = ImageButton(
        panel_x + panel_width - 300, panel_y + panel_height - 80, 200, 60,
        "", font, (255, 255, 255),
        save_img, save_img_hover
    )
    
    # Thêm một số hiệu ứng đặc biệt cho màn hình
    particles = []
    for _ in range(50):
        particles.append({
            "x": pygame.time.get_ticks() % width,
            "y": pygame.time.get_ticks() % height,
            "size": pygame.time.get_ticks() % 3 + 1,
            "speed": pygame.time.get_ticks() % 2 + 1,
            "angle": pygame.time.get_ticks() % 360
        })
    
    # Hiệu ứng âm thanh khi thay đổi
    sound_change = False
    
    # Thông báo lưu
    save_message = ""
    save_time = 0
    
    while True:
        current_time = pygame.time.get_ticks()
        delta_time = clock.get_time() / 1000.0
        mouse_pos = pygame.mouse.get_pos()
        
        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Xử lý các thanh trượt
            music_slider.handle_event(event)
            sound_slider.handle_event(event)
            
            # Xử lý các nút bật/tắt
            mute_toggle.handle_event(event)
            fullscreen_toggle.handle_event(event)
            fps_toggle.handle_event(event)
            animations_toggle.handle_event(event)
            
            # Xử lý các nút
            if back_btn.is_clicked(event):
                return False, settings  # Không lưu
            
            if save_btn.is_clicked(event):
                # Cập nhật cài đặt
                settings.set("audio", "music_volume", music_slider.current_val)
                settings.set("audio", "sound_volume", sound_slider.current_val)
                settings.set("audio", "mute", mute_toggle.is_on)
                settings.set("display", "fullscreen", fullscreen_toggle.is_on)
                settings.set("display", "show_fps", fps_toggle.is_on)
                settings.set("display", "animations", animations_toggle.is_on)
                
                # Lưu cài đặt
                if settings.save_settings():
                    save_message = "Đã lưu cài đặt thành công!"
                else:
                    save_message = "Lỗi khi lưu cài đặt!"
                
                save_time = current_time
                
                # Áp dụng cài đặt
                settings.apply_audio_settings()
                settings.apply_display_settings()
                
                return True, settings  # Đã lưu
        
        # Cập nhật cài đặt trong thời gian thực cho âm lượng
        settings.set("audio", "music_volume", music_slider.current_val)
        settings.apply_audio_settings()
        
        # Vẽ nền
        screen.blit(background, (0, 0))
        
        # Vẽ các hạt
        for particle in particles:
            # Di chuyển hạt
            particle["x"] += particle["speed"] * 0.5 * math.cos(math.radians(particle["angle"]))
            particle["y"] += particle["speed"] * 0.5 * math.sin(math.radians(particle["angle"]))
            
            # Quay lại màn hình khi ra ngoài
            if particle["x"] < 0: particle["x"] = width
            if particle["x"] > width: particle["x"] = 0
            if particle["y"] < 0: particle["y"] = height
            if particle["y"] > height: particle["y"] = 0
            
            # Vẽ hạt
            pygame.draw.circle(
                screen, 
                (255, 255, 255, 100), 
                (int(particle["x"]), int(particle["y"])), 
                particle["size"]
            )
        
        # Vẽ bảng điều khiển
        screen.blit(panel, (panel_x, panel_y))
        
        # Vẽ tiêu đề
        title_text = big_font.render("CÀI ĐẶT", True, (255, 255, 255))
        screen.blit(title_text, (panel_x + panel_width // 2 - title_text.get_width() // 2, panel_y + 20))
        
        # Vẽ phần tiêu đề âm thanh
        audio_text = font.render("ÂM THANH", True, (255, 255, 255))
        screen.blit(audio_text, (panel_x + 40, panel_y + 70))
        
        # Vẽ các thanh trượt
        music_slider.draw(screen, font, "Nhạc nền:")
        sound_slider.draw(screen, font, "Âm thanh:")
        
        # Vẽ các nút bật/tắt
        mute_toggle.draw(screen, font, "Tắt tiếng:")
        
        # Vẽ phần tiêu đề hiển thị
        display_text = font.render("HIỂN THỊ", True, (255, 255, 255))
        screen.blit(display_text, (panel_x + 40, panel_y + 250))
        
        # Vẽ các nút bật/tắt hiển thị
        fullscreen_toggle.draw(screen, font, "Toàn màn hình:")
        fps_toggle.draw(screen, font, "Hiển thị FPS:")
        animations_toggle.draw(screen, font, "Hoạt ảnh:")
        
        # Vẽ các nút
        back_btn.draw(screen, mouse_pos)
        save_btn.draw(screen, mouse_pos)
        
        # Vẽ thông báo lưu nếu có
        if save_message and current_time - save_time < 3000:
            message_text = font.render(save_message, True, (255, 255, 255))
            screen.blit(message_text, (width // 2 - message_text.get_width() // 2, panel_y - 40))
        
        pygame.display.flip()
        clock.tick(60)