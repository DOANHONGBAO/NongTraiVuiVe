import random
from animal import Animal
from food import Food

class Merchant:
    def __init__(self):
        self.items = self.generate_items()

    def generate_items(self):
        items = []
        # 50% cơ hội là động vật, 50% là thức ăn
        for _ in range(1):
            if random.random() < 0.5:
                animal = random.choice([
                    Animal("Bò", 25),
                    Animal("Gà", 15),
                    Animal("Heo", 20),
                ])
                items.append(animal)
            else:
                food = random.choice([
                    Food("Thức ăn gia súc", 10),
                    Food("Cỏ khô", 5),
                ])
                items.append(food)
        return items
