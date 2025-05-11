import random
from animal import Animal
from items import Item

# from food import Food

class Merchant:
    def __init__(self):
        self.items = self.generate_items()

    def generate_items(self):
        items = []
        for _ in range(3):  # Hiển thị 3 món mỗi lần
            if random.random() < 0.3:
                # Tạo động vật với vị trí ngẫu nhiên
                animal = random.choice([
                    Animal(name="Bò", cost=25, index = 0, x=random.randint(100, 600), y=random.randint(400, 500)),
                    Animal(name="Gà", cost=15, index = 0, x=random.randint(100, 600), y=random.randint(400, 500)),
                    Animal(name="Heo", cost=20, index = 0, x=random.randint(100, 600), y=random.randint(400, 500)),
                    Animal(name="Cừu", cost=22, index = 0, x=random.randint(100, 600), y=random.randint(400, 500)),
                    Animal(name="Dê", cost=22, index = 0, x=random.randint(100, 600), y=random.randint(400, 500)),
                ])
            else:
                # Bán hạt giống
                seed = random.choice([
                    Item(name="Carrot", index=2, x=0, y=0),
                    Item(name="Corn", index=7, x=0, y=0),
                    Item(name="Straw_berry", index=4, x=0, y=0),
                    Item(name="Carbage", index=28, x=0, y=0),
                    Item(name="Rice", index=3, x=0, y=0),
                ])
                seed.cost = 10  # thêm thuộc tính cost để mua
                items.append(seed)
        return items
