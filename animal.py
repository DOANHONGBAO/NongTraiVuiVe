class Animal:
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost
        self.hungry = True

    def __str__(self):
        return f"{self.name} - giá: {self.cost}"

    def feed(self):
        self.hungry = False

    def produce_gold(self):
        return 5 if not self.hungry else 0  # Nếu được cho ăn thì tạo ra vàng
