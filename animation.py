import pygame
import os
from enum import Enum

class AnimationState(Enum):
    """Trạng thái animation của động vật"""
    IDLE = 0       # Đứng yên
    WALKING = 1    # Đi bộ
    RUNNING = 2    # Chạy
    EATING = 3     # Ăn
    SLEEPING = 4   # Ngủ
    ATTACKING = 5  # Tấn công

class Animation:
    def __init__(self, sprite_sheet_path, frame_width, frame_height, scale=1.0):
        """
        Khởi tạo hệ thống animation từ sprite sheet
        
        Tham số:
            sprite_sheet_path (str): Đường dẫn tới file sprite sheet
            frame_width (int): Chiều rộng của mỗi frame (pixel)
            frame_height (int): Chiều cao của mỗi frame (pixel)
            scale (float): Tỷ lệ phóng to/thu nhỏ animation (mặc định 1.0)
        """
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.scale = scale
        
        # Tính toán số lượng frame trong sprite sheet
        self.sheet_width = self.sprite_sheet.get_width()
        self.sheet_height = self.sprite_sheet.get_height()
        self.frames_per_row = self.sheet_width // frame_width
        self.rows = self.sheet_height // frame_height
        
        # Các trạng thái animation và frame tương ứng
        self.animations = {
            AnimationState.IDLE: {"frames": [], "speed": 0.2},
            AnimationState.WALKING: {"frames": [], "speed": 0.15},
            AnimationState.RUNNING: {"frames": [], "speed": 0.1},
            # Thêm các trạng thái khác nếu cần
        }
        
        # Trạng thái animation hiện tại
        self.current_state = AnimationState.IDLE
        self.current_frame = 0
        self.animation_time = 0
        self.facing_right = True  # Hướng nhìn sang phải
        
        # Trích xuất các frame từ sprite sheet
        self._extract_frames()
    
    def _extract_frames(self):
        """Trích xuất tất cả frame từ sprite sheet và phân loại theo trạng thái"""
        all_frames = []
        for row in range(self.rows):
            for col in range(self.frames_per_row):
                frame_rect = pygame.Rect(col * self.frame_width, 
                                        row * self.frame_height, 
                                        self.frame_width, 
                                        self.frame_height)
                frame_image = self.sprite_sheet.subsurface(frame_rect)
                
                # Thay đổi kích thước nếu cần
                if self.scale != 1.0:
                    new_size = (int(self.frame_width * self.scale), 
                               int(self.frame_height * self.scale))
                    frame_image = pygame.transform.scale(frame_image, new_size)
                
                all_frames.append(frame_image)
        
        # Phân phối frame cho các trạng thái animation
        frames_per_state = len(all_frames) // len(self.animations)
        for i, state in enumerate(self.animations.keys()):
            start = i * frames_per_state
            end = start + frames_per_state
            self.animations[state]["frames"] = all_frames[start:end]
    
    def set_state(self, new_state):
        """
        Thay đổi trạng thái animation hiện tại
        
        Tham số:
            new_state (AnimationState): Trạng thái mới
        """
        if new_state != self.current_state:
            self.current_state = new_state
            self.current_frame = 0
            self.animation_time = 0
    
    def set_direction(self, facing_right):
        """
        Thiết lập hướng nhìn của nhân vật
        
        Tham số:
            facing_right (bool): True nếu nhìn sang phải, False nếu nhìn sang trái
        """
        self.facing_right = facing_right
    
    def update(self, dt):
        """
        Cập nhật animation dựa trên thời gian
        
        Tham số:
            dt (float): Thời gian trôi qua kể từ frame trước (giây)
        """
        if not self.animations[self.current_state]["frames"]:
            return
            
        self.animation_time += dt
        frame_duration = self.animations[self.current_state]["speed"]
        
        if self.animation_time >= frame_duration:
            self.animation_time = 0
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.current_state]["frames"])
    
    def get_current_frame(self):
        """
        Lấy frame hiện tại của animation, lật hướng nếu cần
        
        Trả về:
            pygame.Surface: Frame hình ảnh hiện tại
        """
        if not self.animations[self.current_state]["frames"]:
            return None
            
        frame = self.animations[self.current_state]["frames"][self.current_frame]
        
        # Lật hình nếu hướng nhìn sang trái
        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)
        
        return frame
    
    def draw(self, surface, position):
        """
        Vẽ frame hiện tại lên surface tại vị trí chỉ định
        
        Tham số:
            surface (pygame.Surface): Bề mặt để vẽ lên
            position (tuple): Vị trí (x, y) để vẽ
        """
        frame = self.get_current_frame()
        if frame:
            surface.blit(frame, position)

# Ví dụ sử dụng (gọi từ file gameplay của bạn)
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    
    # Khởi tạo animation cho gà
    chicken_animation = Animation("assets/animals/chicken.png", 64, 64, 0.8)
    chicken_animation.set_state(AnimationState.WALKING)
    
    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # Thời gian delta tính bằng giây
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Cập nhật animation
        chicken_animation.update(dt)
        
        # Vẽ
        screen.fill((255, 255, 255))
        chicken_animation.draw(screen, (400, 300))
        
        pygame.display.flip()
    
    pygame.quit()