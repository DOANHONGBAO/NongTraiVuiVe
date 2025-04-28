import pygame
from items import Item
import random
class Plant:
    def __init__(self, name, x, y, growth_stages, growth_time, images, index = None,indexob = None):
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
        self.index = index
        self.indexob = indexob



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


    def is_ready_to_harvest(self):
        """Kiểm tra xem cây đã ở giai đoạn cuối cùng chưa"""
        return self.current_stage == len(self.growth_stages) - 1
    def harvest(self):
        """Trả về item thu hoạch nếu cây sẵn sàng"""
        if self.is_ready_to_harvest():
            return Item(self.name,self.indexob, self.x + random.randint(-5, 5), self.y + random.randint(-5, 5))  # Item được định nghĩa bên ngoài
        return None
class Field:
    def __init__(self, x1, y1, x2, y2, num_columns, num_rows):
        self.x1 = x1
        self.y1 = y1
        self.rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
        self.num_columns = num_columns
        self.num_rows = num_rows
        self.plants = []
        self.harvested_items = []  # Danh sách vật phẩm sau khi thu hoạch
        self.harvested = True     # Cờ trạng thái: đã thu hoạch hay chưa

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.rect, 2)
        for plant in self.plants:
            plant.draw(screen)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def plant_crops(self, plant, plant_images):
        if self.plants or self.harvested is False:
            return  # Không trồng nếu đã có cây hoặc chưa thu hoạch
        plant_width, plant_height = 32, 32
        x_start = self.rect.x + 10
        y_start = self.rect.y + 10
        count = 0
        for row in range(self.num_rows):
            for col in range(self.num_columns):
                count += 1
                plant_x = x_start + col * (plant_width + 5)
                plant_y = y_start + row * (plant_height + 5)
                new_plant = Plant(name=plant.name, x=plant_x, y=plant_y,
                                  growth_stages=plant.growth_stages,
                                  growth_time=plant.growth_time,
                                  images=plant_images, index=count,indexob = plant.indexob)
                self.plants.append(new_plant)
        self.harvested = False  # Đặt lại trạng thái khi trồng
    def update(self, delta_time):
        for plant in self.plants:
            plant.update(delta_time)

    def try_harvest(self):
        dropped_items = []
        if all(p.is_ready_to_harvest() for p in self.plants):
            for p in self.plants:
                item = p.harvest()
                dropped_items.append(item)
            self.plants.clear()
            self.harvested = True
        return dropped_items
