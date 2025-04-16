import pygame
import os
import random

from animation import Animation  # Giả sử file animation.py chứa class Animation



class Animal:
    ANIMAL_ASSET_CONFIG = {
        "chicken": {
            "path": "assets/animals/chicken",
            "left_frames": list(range(0,5)),     # 1–5
            "right_frames": list(range(5, 9))    # 6–10
        },
        "pig": {
            "path": "assets/animals/pig",
            "left_frames": list(range(0,5)),
            "right_frames": list(range(5, 9))
        },
        "cow": {
            "path": "assets/animals/cow",
            "left_frames": list(range(0,5)),
            "right_frames": list(range(5, 9))
        },
        "goat": {
            "path": "assets/animals/goat",
            "left_frames": list(range(0,5)),
            "right_frames": list(range(5, 9))
        },
        # Thêm các con khác vào đây
    }
    def __init__(self, name, cost, x=0, y=0):
        self.name = name
        self.cost = cost
        self.hungry = True

        TRANSLATE_NAMES = {
            "Gà": "chicken",
            "Heo": "pig",
            "Bò": "cow",
            "Dê": "goat"
        }

        self.asset_key = TRANSLATE_NAMES.get(self.name, self.name.lower())

        self.x = x
        self.y = y
        self.direction = random.choice(["left", "right"])
        self.speed = 1 + random.random() * 1.5

        # Load frames trước
        self.left_frames = self.load_frames("left")
        self.right_frames = self.load_frames("right")

        # Gán hình ban đầu
        if self.direction == "right" and self.right_frames:
            self.image = self.right_frames[0]
        elif self.left_frames:
            self.image = self.left_frames[0]
        else:
            self.image = None
            print(f"[ERROR] No animation frames loaded for {self.name}")

        # Animation controller
        self.animation = Animation(self, self.right_frames, self.left_frames)

        # Thời gian đứng im
        self.is_idle = False
        self.idle_start_time = 0
        self.idle_duration = 0

    def load_frames(self, direction):
        frames = []

        config = Animal.ANIMAL_ASSET_CONFIG.get(self.asset_key)
        if not config:
            print(f"[WARNING] No animation config found for {self.name}")
            return frames

        base_path = config["path"]
        indices = config["left_frames"] if direction == "left" else config["right_frames"]

        for i in indices:
            filename = base_path + "/" + f"{self.asset_key}_{i}.png"
            if os.path.exists(filename):
                print(f"[INFO] Loading frame: {filename}")
                frames.append(pygame.image.load(filename).convert_alpha())
            else:
                print(f"[WARNING] Missing frame: {filename}")

        return frames




    def feed(self):
        self.hungry = False

    def produce_gold(self):
        return 5 if not self.hungry else 0

    def update(self, screen_width):
        now = pygame.time.get_ticks()

        # Nếu đang đứng im
        if self.is_idle:
            if now - self.idle_start_time >= self.idle_duration:
                self.is_idle = False  # Hết thời gian đứng im
            else:
                self.animation.update()
                return

        # Di chuyển
        if self.direction == "right":
            self.x += self.speed
            if self.x > screen_width - 64:
                self.direction = "left"
        else:
            self.x -= self.speed
            if self.x < 0:
                self.direction = "right"

        # Update animation
        self.animation.update()

        # Cơ hội đứng im 30%
        if random.random() < 0.3:
            self.is_idle = True
            self.idle_start_time = now
            self.idle_duration = 10000  # 10 giây

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.x, self.y))
