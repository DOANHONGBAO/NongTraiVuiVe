import pygame

class Plant:
    def __init__(self, name, x, y, growth_stages, growth_time, images):
        self.name = name  # Tên cây (ví dụ: carrot, tomato)
        self.x = x
        self.y = y

        # Các giai đoạn phát triển và hình ảnh cho từng giai đoạn
        self.growth_stages = growth_stages
        self.current_stage = 0  # Giai đoạn ban đầu (mới trồng)
        
        # Thời gian phát triển của cây (total time)
        self.growth_time = growth_time
        self.time_passed = 0
        
        # Danh sách hình ảnh cho từng giai đoạn phát triển
        self.images = images

    def update(self, delta_time):
        """Cập nhật trạng thái phát triển của cây"""
        if self.time_passed < self.growth_time:
            self.time_passed += delta_time
            # Cập nhật giai đoạn phát triển
            stage = int(self.time_passed / (self.growth_time / len(self.growth_stages)))
            self.current_stage = min(stage, len(self.growth_stages) - 1)

    def draw(self, screen):
        """Vẽ cây lên màn hình"""
        screen.blit(self.images[self.current_stage], (self.x, self.y))
class Field:
    def __init__(self, x1, y1, x2, y2, num_columns, num_rows):
        self.rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)  # Khu vực của thửa ruộng
        self.num_columns = num_columns  # Số cột cây
        self.num_rows = num_rows  # Số hàng cây
        self.plants = []  # Danh sách các cây trồng trong thửa này

    def draw(self, screen):
        # Vẽ thửa ruộng (có thể thay đổi màu sắc hoặc vẽ hình ảnh nền cho thửa)
        pygame.draw.rect(screen, (0, 255, 0), self.rect, 2)  # Vẽ viền thửa ruộng

    def is_clicked(self, mouse_pos):
        # Kiểm tra xem người chơi có click vào thửa ruộng không
        return self.rect.collidepoint(mouse_pos)

    def plant_crops(self, plant, plant_images):
        """Trồng cây trong thửa ruộng theo hàng và cột"""
        # Tính toán khoảng cách giữa các cây
        plant_width = 32  # Kích thước cây (32x32)
        plant_height = 32

        x_start = self.rect.x + 10  # Khoảng cách từ viền trái của thửa ruộng
        y_start = self.rect.y + 10  # Khoảng cách từ viền trên của thửa ruộng

        for row in range(self.num_rows):
            for col in range(self.num_columns):
                plant_x = x_start + col * (plant_width + 5)  # Khoảng cách giữa các cây theo chiều ngang
                plant_y = y_start + row * (plant_height + 5)  # Khoảng cách giữa các cây theo chiều dọc
                new_plant = Plant(name=plant.name, x=plant_x, y=plant_y,
                                  growth_stages=plant.growth_stages,
                                  growth_time=plant.growth_time,
                                  images=plant_images)
                self.plants.append(new_plant)  # Thêm cây vào thửa ruộng

