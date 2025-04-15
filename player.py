import random
from card import Card

class Player:
    def __init__(self):
        self.gold = 50
        self.animals = []
        self.food = []
        self.hand = self.draw_cards()
        self.score_multiplier = 1  # Hệ số nhân điểm mặc định là 1
        self.score_exponent = 1  # Hệ số lũy thừa mặc định là 1

    def draw_cards(self):
        # Các lá bài sự kiện (bao gồm cộng, trừ điểm và bốc thêm lá)
        cards = [
            Card("Thu hoạch mùa", 7),           # Cộng điểm
            Card("Lễ hội làng", 5),             # Cộng điểm
            Card("Bán rau củ", 4),             # Cộng điểm
            Card("Lao động", 6),               # Cộng điểm
            Card("Bạn bè tặng quà", 3),        # Cộng điểm
            Card("Mưa lớn", -5),               # Trừ điểm
            Card("Mùa màng bội thu", 10),      # Cộng điểm lớn
            Card("Kinh doanh thành công", 8),  # Cộng điểm
            Card("Chuyến đi du lịch", 2),      # Cộng điểm nhỏ
            Card("Thêm bạn bớt thù", 5),       # Cộng điểm
            Card("Tình cờ gặp khách quý", 15), # Cộng điểm lớn
            Card("Hỗ trợ cộng đồng", -3),      # Trừ điểm
            Card("Giảm giá đặc biệt", 4),      # Cộng điểm nhỏ
            Card("Lễ kỷ niệm lớn", 12),        # Cộng điểm lớn
            Card("Nâng cấp cơ sở hạ tầng", 10),# Cộng điểm
            Card("Khó khăn tài chính", -10),   # Trừ điểm lớn
            Card("Gặp may mắn", 5),            # Cộng điểm nhỏ
            Card("Khôi phục sản xuất", 6),     # Cộng điểm
            Card("Bốc thêm lá", 0),            # Bốc thêm lá bài
            Card("Nhân đôi điểm", 0),          # Nhân đôi điểm
            Card("Nhân ba điểm", 0),           # Nhân ba điểm
            Card("Lũy thừa điểm x2", 0),       # Lũy thừa điểm x2
            Card("Lũy thừa điểm x3", 0),       # Lũy thừa điểm x3
        ]
        return random.sample(cards, 5)  # Lấy ngẫu nhiên 3 lá bài từ bộ

    def apply_card_effect(self, card):
        # Áp dụng hiệu ứng của lá bài
        if card.name == "Nhân đôi điểm":
            self.score_multiplier = random.uniform(1.5, 2.5)  # Nhân đôi điểm với giá trị ngẫu nhiên từ 1.5 đến 2.5
            self.score_exponent = 1  # Đặt lại hệ số lũy thừa về 1
        elif card.name == "Nhân ba điểm":
            self.score_multiplier = random.uniform(2.5, 3.5)  # Nhân ba điểm với giá trị ngẫu nhiên từ 2.5 đến 3.5
            self.score_exponent = 1  # Đặt lại hệ số lũy thừa về 1
        elif card.name == "Lũy thừa điểm x2":
            self.score_exponent = random.uniform(1.5, 2.5)  # Lũy thừa điểm x2 với giá trị ngẫu nhiên
            self.score_multiplier = 1  # Đặt lại hệ số nhân điểm về 1
        elif card.name == "Lũy thừa điểm x3":
            self.score_exponent = random.uniform(2.5, 3.5)  # Lũy thừa điểm x3 với giá trị ngẫu nhiên
            self.score_multiplier = 1  # Đặt lại hệ số nhân điểm về 1
        elif card.name == "Bốc thêm lá":
            # Cơ chế bốc thêm lá bài
            self.hand.append(self.draw_cards()[0])  # Bốc một lá bài ngẫu nhiên từ bộ bài
        else:
            # Nếu là lá bài có điểm cộng hoặc trừ
            self.score_multiplier = 1
            self.score_exponent = 1

    def calculate_final_score(self, base_score):
        # Tính điểm cuối cùng, áp dụng hệ số nhân và hệ số lũy thừa
        if self.score_exponent > 1:
            return base_score ** self.score_exponent  # Tính điểm theo lũy thừa
        else:
            return base_score * self.score_multiplier  # Tính điểm theo hệ số nhân
