import pygame
import os
import random
from animation import Animation

class Animal:
    ANIMAL_ASSET_CONFIG = {
        "chicken": {
            "path": "assets/animals/chicken",
            "left_frames": list(range(0, 5)),
            "right_frames": list(range(5, 9))
        },
        "pig": {
            "path": "assets/animals/pig",
            "left_frames": list(range(0, 5)),
            "right_frames": list(range(5, 9))
        },
        "cow": {
            "path": "assets/animals/cow",
            "left_frames": list(range(0, 5)),
            "right_frames": list(range(5, 9))
        },
        "goat": {
            "path": "assets/animals/goat",
            "left_frames": list(range(0, 5)),
            "right_frames": list(range(5, 9))
        },
        "sheep": {
            "path": "assets/animals/sheep",
            "left_frames": list(range(0, 5)),
            "right_frames": list(range(5, 9))
        },
    }

    def __init__(self, name, cost, index, x=0, y=0, screen_width=1900, screen_height=1000):
        self.name = name
        self.cost = cost
        self.hungry = True

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.index = index

        TRANSLATE_NAMES = {
            "Gà": "chicken",
            "Heo": "pig",
            "Bò": "cow",
            "Dê": "goat",
            "Cừu": "sheep"
        }

        self.asset_key = TRANSLATE_NAMES.get(self.name, self.name.lower())

        self.x = x
        self.y = y
        self.speed = 1 

        self.left_frames = self.load_frames("left")
        self.right_frames = self.load_frames("right")

        self.image = self.right_frames[0] if self.right_frames else None

        self.animation = Animation(self, self.right_frames, self.left_frames)

        # Idle control
        self.is_idle = False
        self.idle_start_time = 0
        self.idle_duration = 2000  # 2 seconds

        self.set_new_target()

    def set_new_target(self):
        # Giới hạn phạm vi 500px từ giữa màn hình
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2

        # Chọn target x trong phạm vi từ (center_x - 250) đến (center_x + 250)
        # Chọn target y trong phạm vi toàn màn hình
        self.target_x = random.randint(center_x - 500, center_x + 500)
        self.target_y = random.randint(center_y - 200, center_y + 200)


    def move(self):
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance < 2:
            # Đến nơi rồi, bắt đầu idle
            self.is_idle = True
            self.idle_start_time = pygame.time.get_ticks()
            return

        # Tính hướng di chuyển
        move_x = self.speed * dx / distance
        move_y = self.speed * dy / distance

        self.x += move_x
        self.y += move_y

        self.direction = "right" if move_x >= 0 else "left"

    def load_frames(self, direction):
        frames = []

        config = Animal.ANIMAL_ASSET_CONFIG.get(self.asset_key)
        if not config:
            print(f"[WARNING] No animation config found for {self.name}")
            return frames

        base_path = config["path"]
        indices = config["left_frames"] if direction == "left" else config["right_frames"]

        for i in indices:
            filename = os.path.join(base_path, f"{self.asset_key}_{i}.png")
            if os.path.exists(filename):
                frames.append(pygame.image.load(filename).convert_alpha())
            else:
                print(f"[WARNING] Missing frame: {filename}")

        return frames

    def feed(self):
        self.hungry = False

    def produce_gold(self):
        return 5 if not self.hungry else 0

    def update(self):
        now = pygame.time.get_ticks()

        if self.is_idle:
            if now - self.idle_start_time >= self.idle_duration:
                self.is_idle = False
                self.set_new_target()
            else:
                self.animation.update()
                return

        self.move()
        self.animation.update()

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.x, self.y))
