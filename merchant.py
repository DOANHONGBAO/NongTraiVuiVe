import random
from animal import Animal
from food import Food

class Merchant:
    def __init__(self):
        self.items = self.generate_items()

    def generate_items(self):
        items = []
        for _ in range(3):  # Mỗi lần hiển thị 3 món
            if random.random() < 0.5:
                animal = random.choice([
                    Animal("Bò", 25),
                    Animal("Gà", 15),
                    Animal("Heo", 20),
                    Animal("Cừu", 22),
                    Animal("Ngựa", 30),
                    Animal("Vịt", 12),
                    Animal("Thỏ", 10),
                    Animal("Chó", 18),
                ])
                items.append(animal)
            else:
                food = random.choice([
                    Food("Thức ăn gia súc", 10),
                    Food("Cỏ khô", 5),
                    Food("Ngũ cốc", 8),
                    Food("Thức ăn hỗn hợp", 12),
                    Food("Bắp", 7),
                    Food("Rơm", 6),
                    Food("Thức ăn cao cấp", 15),
                    Food("Cá khô", 10),
                    Food("Hoa quả tươi", 18),
                    Food("Bánh mì", 9),
                    Food("Sữa tươi", 12),
                    Food("Khoai tây", 5),
                    Food("Hạt giống", 4),
                ])
                items.append(food)
        return items
