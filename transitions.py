import pygame
import math

class Transition:
    """
    Lớp cơ sở cho các hiệu ứng chuyển tiếp
    """
    def __init__(self, duration=1.0):
        self.duration = duration  # Thời gian chuyển tiếp (giây)
        self.start_time = 0
        self.progress = 0
        self.done = False
        self.screen = None
        self.width = 0
        self.height = 0
        self.initial_snapshot = None
        self.next_snapshot = None
    
    def start(self, screen, next_screen_func=None):
        """Bắt đầu hiệu ứng chuyển tiếp"""
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.start_time = pygame.time.get_ticks()
        self.done = False
        self.progress = 0
        
        # Lưu ảnh màn hình hiện tại
        self.initial_snapshot = screen.copy()
        
        # Gọi hàm tạo màn hình tiếp theo và lưu lại ảnh của nó
        if next_screen_func:
            # Tạo một bề mặt tạm thời để vẽ màn hình tiếp theo
            temp_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            next_screen_func(temp_surface)
            self.next_snapshot = temp_surface

    def update(self):
        """Cập nhật tiến trình hiệu ứng"""
        if self.done:
            return True
        
        current_time = pygame.time.get_ticks()
        elapsed = (current_time - self.start_time) / 1000.0
        
        # Tính toán tiến trình từ 0.0 đến 1.0
        self.progress = min(1.0, elapsed / self.duration)
        
        if self.progress >= 1.0:
            self.done = True
        
        return self.done

    def draw(self):
        """Vẽ frame hiệu ứng hiện tại - phương thức trừu tượng để lớp con triển khai"""
        pass

    def is_done(self):
        """Kiểm tra xem hiệu ứng đã hoàn thành chưa"""
        return self.done

    def ease_out_cubic(self, t):
        """Hàm easing làm chuyển động mượt hơn ở cuối"""
        return 1 - math.pow(1 - t, 3)
    
    def ease_in_out_cubic(self, t):
        """Hàm easing làm chuyển động mượt hơn ở đầu và cuối"""
        return 3 * t * t - 2 * t * t * t


class FadeTransition(Transition):
    """
    Hiệu ứng mờ dần từ màn hình này sang màn hình khác
    """
    def __init__(self, duration=1.0, color=(0, 0, 0)):
        super().__init__(duration)
        self.color = color
        
    def draw(self):
        if not self.initial_snapshot or not self.screen:
            return
        
        # Nếu không có ảnh của màn hình tiếp theo, chỉ làm mờ vào màu đen
        if not self.next_snapshot:
            # Vẽ ảnh màn hình hiện tại
            self.screen.blit(self.initial_snapshot, (0, 0))
            
            # Vẽ một lớp phủ dần dần tăng độ mờ
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            alpha = int(self.progress * 255)
            overlay.fill((*self.color, alpha))
            self.screen.blit(overlay, (0, 0))
        else:
            # Chuyển tiếp giữa hai ảnh màn hình
            if self.progress < 0.5:
                # Hiển thị màn hình đầu tiên và làm mờ dần
                self.screen.blit(self.initial_snapshot, (0, 0))
                overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                alpha = int((self.progress / 0.5) * 255)
                overlay.fill((*self.color, alpha))
                self.screen.blit(overlay, (0, 0))
            else:
                # Hiển thị màn hình thứ hai và làm rõ dần
                self.screen.blit(self.next_snapshot, (0, 0))
                overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                alpha = int(255 - ((self.progress - 0.5) / 0.5) * 255)
                overlay.fill((*self.color, alpha))
                self.screen.blit(overlay, (0, 0))


class SlideTransition(Transition):
    """
    Hiệu ứng trượt từ màn hình này sang màn hình khác
    Hướng: 'left', 'right', 'up', 'down'
    """
    def __init__(self, duration=1.0, direction='left'):
        super().__init__(duration)
        self.direction = direction
        
    def draw(self):
        if not self.initial_snapshot or not self.next_snapshot or not self.screen:
            return
        
        # Tính toán vị trí dựa trên hướng và tiến trình
        progress = self.ease_out_cubic(self.progress)  # Áp dụng hàm easing
        
        if self.direction == 'left':
            x1 = int(-self.width * progress)
            x2 = int(self.width + x1)
            self.screen.blit(self.initial_snapshot, (x2, 0))
            self.screen.blit(self.next_snapshot, (x1, 0))
        elif self.direction == 'right':
            x1 = int(self.width * progress)
            x2 = int(-self.width + x1)
            self.screen.blit(self.initial_snapshot, (x2, 0))
            self.screen.blit(self.next_snapshot, (x1, 0))
        elif self.direction == 'up':
            y1 = int(-self.height * progress)
            y2 = int(self.height + y1)
            self.screen.blit(self.initial_snapshot, (0, y2))
            self.screen.blit(self.next_snapshot, (0, y1))
        elif self.direction == 'down':
            y1 = int(self.height * progress)
            y2 = int(-self.height + y1)
            self.screen.blit(self.initial_snapshot, (0, y2))
            self.screen.blit(self.next_snapshot, (0, y1))


class ZoomTransition(Transition):
    """
    Hiệu ứng phóng to/thu nhỏ giữa các màn hình
    mode: 'in' (thu nhỏ màn hình hiện tại, hiển thị màn hình mới)
          'out' (phóng to màn hình hiện tại, sau đó hiển thị màn hình mới)
    """
    def __init__(self, duration=1.0, mode='in'):
        super().__init__(duration)
        self.mode = mode
        
    def draw(self):
        if not self.initial_snapshot or not self.next_snapshot or not self.screen:
            return
        
        progress = self.ease_in_out_cubic(self.progress)
        
        if self.mode == 'in':
            if progress < 0.5:
                # Thu nhỏ màn hình hiện tại
                scale = 1 - progress * 2
                scaled_width = int(self.width * scale)
                scaled_height = int(self.height * scale)
                
                # Vị trí để giữ hình ảnh ở giữa
                x = (self.width - scaled_width) // 2
                y = (self.height - scaled_height) // 2
                
                # Thu nhỏ và vẽ
                scaled_surface = pygame.transform.smoothscale(
                    self.initial_snapshot, (scaled_width, scaled_height))
                
                # Vẽ màu nền (đen)
                self.screen.fill((0, 0, 0))
                
                # Vẽ hình ảnh đã thu nhỏ
                self.screen.blit(scaled_surface, (x, y))
            else:
                # Phóng to màn hình mới
                adjusted_progress = (progress - 0.5) * 2
                scale = adjusted_progress
                scaled_width = int(self.width * scale)
                scaled_height = int(self.height * scale)
                
                # Vị trí để giữ hình ảnh ở giữa
                x = (self.width - scaled_width) // 2
                y = (self.height - scaled_height) // 2
                
                # Phóng to và vẽ
                scaled_surface = pygame.transform.smoothscale(
                    self.next_snapshot, (scaled_width, scaled_height))
                
                # Vẽ màu nền (đen)
                self.screen.fill((0, 0, 0))
                
                # Vẽ hình ảnh đã phóng to
                self.screen.blit(scaled_surface, (x, y))
        
        elif self.mode == 'out':
            # Ngược lại với 'in'
            if progress < 0.5:
                # Phóng to màn hình hiện tại
                adjusted_progress = progress * 2
                scale = 1 + adjusted_progress * 0.5  # Phóng to 150%
                scaled_width = int(self.width * scale)
                scaled_height = int(self.height * scale)
                
                # Vị trí để giữ hình ảnh ở giữa
                x = (self.width - scaled_width) // 2
                y = (self.height - scaled_height) // 2
                
                # Phóng to và vẽ
                scaled_surface = pygame.transform.smoothscale(
                    self.initial_snapshot, (scaled_width, scaled_height))
                
                # Vẽ hình ảnh đã phóng to (chỉ hiển thị phần vừa với màn hình)
                self.screen.blit(scaled_surface, (x, y))
            else:
                # Thu nhỏ màn hình mới từ ngoài vào
                adjusted_progress = (progress - 0.5) * 2
                scale = 2 - adjusted_progress  # Từ 1.5 đến 1.0
                scaled_width = int(self.width * scale)
                scaled_height = int(self.height * scale)
                
                # Vị trí để giữ hình ảnh ở giữa
                x = (self.width - scaled_width) // 2
                y = (self.height - scaled_height) // 2
                
                # Thu nhỏ và vẽ
                scaled_surface = pygame.transform.smoothscale(
                    self.next_snapshot, (scaled_width, scaled_height))
                
                # Vẽ hình ảnh đã thu nhỏ
                self.screen.blit(scaled_surface, (x, y))


class PixelateTransition(Transition):
    """
    Hiệu ứng chuyển tiếp pixel hóa
    """
    def __init__(self, duration=1.0):
        super().__init__(duration)
        
    def draw(self):
        if not self.initial_snapshot or not self.next_snapshot or not self.screen:
            return
        
        progress = self.progress
        
        if progress < 0.5:
            # Pixel hóa màn hình hiện tại
            pixel_size = int(1 + (progress * 2) * 20)  # Tăng dần kích thước pixel từ 1 đến 21
            
            if pixel_size > 1:
                # Thu nhỏ hình ảnh
                small_width = max(1, self.width // pixel_size)
                small_height = max(1, self.height // pixel_size)
                small_surface = pygame.transform.scale(
                    self.initial_snapshot, (small_width, small_height))
                
                # Phóng to lại để tạo hiệu ứng pixel
                pixelated_surface = pygame.transform.scale(
                    small_surface, (self.width, self.height))
                
                self.screen.blit(pixelated_surface, (0, 0))
            else:
                self.screen.blit(self.initial_snapshot, (0, 0))
                
        else:
            # Giảm dần độ pixel hóa cho màn hình mới
            adjusted_progress = (progress - 0.5) * 2
            pixel_size = int(20 - adjusted_progress * 19)  # Giảm dần kích thước pixel từ 20 về 1
            
            if pixel_size > 1:
                # Thu nhỏ hình ảnh
                small_width = max(1, self.width // pixel_size)
                small_height = max(1, self.height // pixel_size)
                small_surface = pygame.transform.scale(
                    self.next_snapshot, (small_width, small_height))
                
                # Phóng to lại để tạo hiệu ứng pixel
                pixelated_surface = pygame.transform.scale(
                    small_surface, (self.width, self.height))
                
                self.screen.blit(pixelated_surface, (0, 0))
            else:
                self.screen.blit(self.next_snapshot, (0, 0))