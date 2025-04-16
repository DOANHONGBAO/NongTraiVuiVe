import pygame

class Animation:
    def __init__(self, entity, right_frames, left_frames, animation_speed=100):
        """
        Quản lý animation cho một thực thể (entity).
        
        entity: Đối tượng Animal (hoặc class con của Animal).
        right_frames: Danh sách frame khi di chuyển sang phải.
        left_frames: Danh sách frame khi di chuyển sang trái.
        animation_speed: Thời gian đổi frame (milliseconds).
        """
        self.entity = entity
        self.right_frames = right_frames
        self.left_frames = left_frames
        self.animation_speed = animation_speed

        self.current_frame = 0
        self.animation_timer = pygame.time.get_ticks()

    def update(self):
        """Cập nhật animation dựa trên hướng di chuyển."""
        now = pygame.time.get_ticks()
        if now - self.animation_timer > self.animation_speed:
            self.animation_timer = now
            self.current_frame = (self.current_frame + 1) % len(self.right_frames)

        # Chọn frame theo hướng
        if self.entity.direction == "right":
            self.entity.image = self.right_frames[self.current_frame]
        else:
            self.entity.image = self.left_frames[self.current_frame]
