import random
from animal import Animal
# from food import Food

class Merchant:
    def __init__(self):
        self.items = self.generate_items()

    def generate_items(self):
        items = []
        for _ in range(3):  # Hiển thị 3 món mỗi lần
            if random.random() < 1:
                # Tạo động vật với vị trí ngẫu nhiên
                animal = random.choice([
                    Animal(name="Bò", cost=25, x=random.randint(100, 600), y=random.randint(400, 500)),
                    Animal(name="Gà", cost=15, x=random.randint(100, 600), y=random.randint(400, 500)),
                    Animal(name="Heo", cost=20, x=random.randint(100, 600), y=random.randint(400, 500)),
                    Animal(name="Cừu", cost=22, x=random.randint(100, 600), y=random.randint(400, 500)),
                    Animal(name="Dê", cost=22, x=random.randint(100, 600), y=random.randint(400, 500)),
                    # Animal(name="Ngựa", cost=30, x=random.randint(100, 600), y=random.randint(400, 500)),
                    # Animal(name="Vịt", cost=12, x=random.randint(100, 600), y=random.randint(400, 500)),
                    # Animal(name="Thỏ", cost=10, x=random.randint(100, 600), y=random.randint(400, 500)),
                    # Animal(name="Chó", cost=18, x=random.randint(100, 600), y=random.randint(400, 500)),
                ])
                items.append(animal)
            # else:
                # # Tạo thực phẩm
                # food = random.choice([
                #     Food("Thức ăn gia súc", 10),
                #     Food("Cỏ khô", 5),
                #     # Food("Ngũ cốc", 8),
                #     # Food("Thức ăn hỗn hợp", 12),
                #     # Food("Bắp", 7),
                #     # Food("Rơm", 6),
                #     # Food("Thức ăn cao cấp", 15),
                #     # Food("Cá khô", 10),
                #     # Food("Hoa quả tươi", 18),
                #     # Food("Bánh mì", 9),
                #     # Food("Sữa tươi", 12),
                #     # Food("Khoai tây", 5),
                #     # Food("Hạt giống", 4),
                # ])
                # items.append(food)
        return items
