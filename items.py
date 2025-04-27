import pygame
import math
pygame.init()

# Setup màn hình trước
screen = pygame.display.set_mode((1920, 1020))
item_images = {}
for i in range(1, 28):  # Từ 1 đến 42
    image = pygame.image.load(f"assets/items/object{i}.png").convert_alpha()
    item_images[i] = image

class Item:
    def __init__(self, name, index, x, y):
        self.name = name
        self.index = index
        self.base_x = x
        self.base_y = y
        self.image = item_images[index]
        self.rect = self.image.get_rect(center=(self.base_x, self.base_y))

        self.angle = 0  # Góc quay hiện tại
        self.angle_direction = 1  # Quay qua lại
        self.float_offset = 0  # Độ cao khi nhấp nhô
        self.float_timer = 0

    def update(self):
        # Lắc nhẹ: thay đổi góc qua lại trong khoảng [-5, 5] độ
        self.angle += 0.5 * self.angle_direction
        if abs(self.angle) > 5:
            self.angle_direction *= -1  # Đổi hướng quay

        # Nhấp nhô nhẹ: sin time
        self.float_timer += 0.05
        self.float_offset = math.sin(self.float_timer) * 5  # +-5 pixels

    def draw(self, screen):
        # Vẽ bóng dưới item
        shadow_rect = pygame.Rect(0, 0, self.rect.width * 0.6, self.rect.height * 0.2)
        shadow_rect.center = (self.base_x, self.base_y + 20)
        shadow_surface = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, (0, 0, 0, 100), shadow_surface.get_rect())
        screen.blit(shadow_surface, shadow_rect.topleft)

        # Xoay hình item
        rotated_image = pygame.transform.rotozoom(self.image, self.angle, 1)
        rotated_rect = rotated_image.get_rect(center=(self.base_x, self.base_y + self.float_offset))
        screen.blit(rotated_image, rotated_rect.topleft)
class Slot:
    def __init__(self, topleft, bottomright):
        x, y = topleft
        w = bottomright[0] - x
        h = bottomright[1] - y
        self.rect = pygame.Rect(x, y, w, h)
        self.item = None  # Item object
        self.quantity = 0  # Số lượng item trong ô

    def add_item(self, item):
        if self.item is None:
            self.item = item
            self.quantity = 1
        else:
            if self.item.name == item.name:
                self.quantity += 1
            else:
                print("Slot đã có item khác, không thể thêm.")  # Hoặc xử lý theo ý bạn

    def draw(self, screen, font):
        # Vẽ ô
        pygame.draw.rect(screen, (220, 220, 220), self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)

        # Vẽ item nếu có
        if self.item:
            # Center item trong slot
            item_rect = self.item.image.get_rect(center=self.rect.center)
            screen.blit(self.item.image, item_rect.topleft)

            # Vẽ số lượng
            quantity_text = font.render(str(self.quantity), True, (0, 0, 0))
            quantity_rect = quantity_text.get_rect(bottomright=self.rect.bottomright)
            screen.blit(quantity_text, quantity_rect.topleft)

class Inventory:
    def __init__(self, slots):
        self.slots = slots  # List các Slot

    def add_item(self, item):
        # item là object Item luôn nhé
        # Tìm slot đã có item cùng tên
        for slot in self.slots:
            if slot.item and slot.item.name == item.name:
                slot.add_item(item)
                return
        
        # Nếu chưa có thì tìm slot trống
        for slot in self.slots:
            if slot.item is None:
                slot.add_item(item)
                return