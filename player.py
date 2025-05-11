import random
from card import Card
from items import Slot, Inventory, Item
from animal import Animal  # Assuming animal.py exists

class Player:
    def __init__(self):
        self.gold = 5000
        self.animals = []
        self.food = []
        self.hand = self.draw_cards()
        self.score_multiplier = 1
        self.score_exponent = 1
        self.animals_on_field = []
        
        # Initialize toolbar and inventory
        self.toolbar_width = 800
        self.toolbar_height = 126
        self.toolbar_x = (1900 - self.toolbar_width) // 2
        self.toolbar_y = 1000 - self.toolbar_height
        self.inventory_x = self.toolbar_x
        self.inventory_y = self.toolbar_y - 460
        
        raw_positions = [
            ((578, 903), (645, 966)), ((655, 904), (719, 966)), ((729, 906), (792, 968)),
            ((804, 905), (868, 966)), ((880, 903), (941, 966)), ((955, 903), (1019, 965)),
            ((1031, 904), (1094, 963)), ((1105, 905), (1171, 969)), ((1178, 901), (1246, 970)),
            ((1259, 906), (1322, 970))
        ]
        
        raw_inventory_position = [
            ((578, 444), (652, 516)), ((652, 444), (726, 516)), ((726, 444), (800, 516)),
            ((800, 444), (874, 516)), ((874, 444), (948, 516)), ((948, 444), (1022, 516)),
            ((1022, 444), (1096, 516)), ((1096, 444), (1170, 516)), ((1170, 444), (1244, 516)),
            ((1244, 444), (1318, 516)), ((578, 516), (652, 588)), ((652, 516), (726, 588)),
            ((726, 516), (800, 588)), ((800, 516), (874, 588)), ((874, 516), (948, 588)),
            ((948, 516), (1022, 588)), ((1022, 516), (1096, 588)), ((1096, 516), (1170, 588)),
            ((1170, 516), (1244, 588)), ((1244, 516), (1318, 588)), ((578, 588), (652, 660)),
            ((652, 588), (726, 660)), ((726, 588), (800, 660)), ((800, 588), (874, 660)),
            ((874, 588), (948, 660)), ((948, 588), (1022, 660)), ((1022, 588), (1096, 660)),
            ((1096, 588), (1170, 660)), ((1170, 588), (1244, 660)), ((1244, 588), (1318, 660)),
            ((578, 660), (652, 734)), ((652, 660), (726, 734)), ((726, 660), (800, 734)),
            ((800, 660), (874, 734)), ((874, 660), (948, 734)), ((948, 660), (1022, 734)),
            ((1022, 660), (1096, 734)), ((1096, 660), (1170, 734)), ((1170, 660), (1244, 734)),
            ((1244, 660), (1318, 734)), ((578, 734), (652, 808)), ((652, 734), (726, 808)),
            ((726, 734), (800, 808)), ((800, 734), (874, 808)), ((874, 734), (948, 808)),
            ((948, 734), (1022, 808)), ((1022, 734), (1096, 808)), ((1096, 734), (1170, 808)),
            ((1170, 734), (1244, 808)), ((1244, 734), (1318, 808))
        ]
        self.slot_positions = [Slot(topleft, bottomright) for topleft, bottomright in raw_positions]
        self.inventory_position = [Slot(topleft, bottomright) for topleft, bottomright in raw_inventory_position]
        self.toolbar = Inventory(self.slot_positions)
        self.inventory = Inventory(self.inventory_position)

    def draw_cards(self):
        cards = [
            Card("Thu hoạch mùa", 7), Card("Lễ hội làng", 5), Card("Bán rau củ", 4),
            Card("Lao động", 6), Card("Bạn bè tặng quà", 3), Card("Mưa lớn", -5),
            Card("Mùa màng bội thu", 10), Card("Kinh doanh thành công", 8),
            Card("Chuyến đi du lịch", 2), Card("Thêm bạn bớt thù", 5),
            Card("Tình cờ gặp khách quý", 15), Card("Hỗ trợ cộng đồng", -3),
            Card("Giảm giá đặc biệt", 4), Card("Lễ kỷ niệm lớn", 12),
            Card("Nâng cấp cơ sở hạ tầng", 10), Card("Khó khăn tài chính", -10),
            Card("Gặp may mắn", 5), Card("Khôi phục sản xuất", 6),
            Card("Bốc thêm lá", 0), Card("Nhân đôi điểm", 0),
            Card("Nhân ba điểm", 0), Card("Lũy thừa điểm x2", 0),
            Card("Lũy thừa điểm x3", 0)
        ]
        return random.sample(cards, 5)

    def apply_card_effect(self, card):
        if card.name == "Nhân đôi điểm":
            self.score_multiplier = random.uniform(1.5, 2.5)
            self.score_exponent = 1
        elif card.name == "Nhân ba điểm":
            self.score_multiplier = random.uniform(2.5, 3.5)
            self.score_exponent = 1
        elif card.name == "Lũy thừa điểm x2":
            self.score_exponent = random.uniform(1.5, 2.5)
            self.score_multiplier = 1
        elif card.name == "Lũy thừa điểm x3":
            self.score_exponent = random.uniform(2.5, 3.5)
            self.score_multiplier = 1
        elif card.name == "Bốc thêm lá":
            self.hand.append(self.draw_cards()[0])
        else:
            self.score_multiplier = 1
            self.score_exponent = 1

    def calculate_final_score(self, base_score):
        if self.score_exponent > 1:
            return base_score ** self.score_exponent
        else:
            return base_score * self.score_multiplier

    def to_dict(self):
        def serialize_item(item):
            if item is None:
                return None
            # Serialize Item object, excluding pygame.Surface (image) and pygame.Rect (rect)
            return {
                'name': item.name,
                'index': item.index,
                'base_x': item.base_x,
                'base_y': item.base_y,
                'angle': item.angle,
                'angle_direction': item.angle_direction,
                'float_offset': item.float_offset,
                'float_timer': item.float_timer,
                'bouncing': item.bouncing,
                'bounce_velocity': item.bounce_velocity,
                'gravity': item.gravity,
                'offset_y': item.offset_y
            }

        def serialize_animal(animal):
            if animal is None:
                return None
            # Serialize Animal object, excluding pygame.Surface (image)
            return {
                'name': animal.name,
                'cost': animal.cost,
                'x': animal.x,
                'y': animal.y,
                'index': animal.index
                # Add other attributes as needed, excluding image
            }

        return {
            'gold': self.gold,
            'animals': self.animals,
            'food': self.food,
            'hand': [card.__dict__ for card in self.hand],
            'score_multiplier': self.score_multiplier,
            'score_exponent': self.score_exponent,
            'animals_on_field': [serialize_animal(animal) for animal in self.animals_on_field],
            'toolbar': [
                {'item': serialize_item(slot.item), 'quantity': slot.quantity}
                for slot in self.toolbar.slots
            ],
            'inventory': [
                {'item': serialize_item(slot.item), 'quantity': slot.quantity}
                for slot in self.inventory.slots
            ]
        }

    @classmethod
    def from_dict(cls, data):
        player = cls()
        player.gold = data.get('gold', 5000)
        player.animals = data.get('animals', [])
        player.food = data.get('food', [])
        player.hand = [Card(d['name'], d['value']) for d in data.get('hand', [])]
        player.score_multiplier = data.get('score_multiplier', 1)
        player.score_exponent = data.get('score_exponent', 1)
        
        # Load animals_on_field
        animals_on_field_data = data.get('animals_on_field', [])
        player.animals_on_field = [
            Animal(
                name=animal_data['name'],
                cost=animal_data['cost'],
                x=animal_data['x'],
                y=animal_data['y'],
                index=animal_data['index']
            ) for animal_data in animals_on_field_data if animal_data
        ]
        
        # Load toolbar
        toolbar_data = data.get('toolbar', [])
        for i, slot_data in enumerate(toolbar_data):
            if i < len(player.toolbar.slots) and slot_data and slot_data['item']:
                item_data = slot_data['item']
                item = Item(
                    name=item_data['name'],
                    index=item_data['index'],
                    x=item_data['base_x'],
                    y=item_data['base_y']
                )
                item.angle = item_data['angle']
                item.angle_direction = item_data['angle_direction']
                item.float_offset = item_data['float_offset']
                item.float_timer = item_data['float_timer']
                item.bouncing = item_data['bouncing']
                item.bounce_velocity = item_data['bounce_velocity']
                item.gravity = item_data['gravity']
                item.offset_y = item_data['offset_y']
                player.toolbar.slots[i].item = item
                player.toolbar.slots[i].quantity = slot_data['quantity']
        
        # Load inventory
        inventory_data = data.get('inventory', [])
        for i, slot_data in enumerate(inventory_data):
            if i < len(player.inventory.slots) and slot_data and slot_data['item']:
                item_data = slot_data['item']
                item = Item(
                    name=item_data['name'],
                    index=item_data['index'],
                    x=item_data['base_x'],
                    y=item_data['base_y']
                )
                item.angle = item_data['angle']
                item.angle_direction = item_data['angle_direction']
                item.float_offset = item_data['float_offset']
                item.float_timer = item_data['float_timer']
                item.bouncing = item_data['bouncing']
                item.bounce_velocity = item_data['bounce_velocity']
                item.gravity = item_data['gravity']
                item.offset_y = item_data['offset_y']
                player.inventory.slots[i].item = item
                player.inventory.slots[i].quantity = slot_data['quantity']
        
        return player