import pygame
import sys
from menu import start_screen
from gameplay import gameplay_screen
from farming_screen import farming_screen 
from audio import start_background_music, stop_music
pygame.init()
WIDTH, HEIGHT = 1915, 1020 
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(" Nông Trại Vui Vẻ ")
# start_background_music() # Bắt đầu nhạc nền

# Màu sắc và font
COLORS = {
    "WHITE": (255, 255, 255),
    "GREEN": (150, 200, 150),
    "DARK_GREEN": (60, 130, 60),
    "BLACK": (0, 0, 0),
    "YELLOW": (255, 215, 0),
    "BROWN": (160, 100, 50),
    "LIGHT_GREEN": (180, 255, 180),  # Thêm dòng này để tránh lỗi
    "DARK_GRAY" : (125,125,125),
    "LIGHT_BROWN" : (3,3,3)
}

FONT = pygame.font.Font("assets/fonts/arcade-among-1.otf", 24)
BIG_FONT = pygame.font.Font("assets/fonts/arcade-among-1.otf", 36)

# Các trạng thái của game
STATE_MENU = "menu"
STATE_GAMEPLAY = "gameplay"
STATE_FARMING = "farming"
current_state = STATE_MENU
player = None
current_day = 1

toolbar_width = 800
toolbar_height = 126
# Vị trí để đặt ảnh thanh công cụ ở giữa dưới
toolbar_x = (1900 - toolbar_width) // 2
toolbar_y = 1000 - toolbar_height
inventory_x = toolbar_x
inventory_y = toolbar_y - 460
toolbar_slots = []
raw_positions = [
    ((578, 903), (645, 966)),
    ((655, 904), (719, 966)),
    ((729, 906), (792, 968)),
    ((804, 905), (868, 966)),
    ((880, 903), (941, 966)),
    ((955, 903), (1019, 965)),
    ((1031, 904), (1094, 963)),
    ((1105, 905), (1171, 969)),
    ((1178, 901), (1246, 970)),
    ((1259, 906), (1322, 970))
]

raw_inventory_position = [
    ((578, 444), (652, 516)), ((652, 444), (726, 516)), ((726, 444), (800, 516)), ((800, 444), (874, 516)), ((874, 444), (948, 516)),
    ((948, 444), (1022, 516)), ((1022, 444), (1096, 516)), ((1096, 444), (1170, 516)), ((1170, 444), (1244, 516)), ((1244, 444), (1318, 516)),

    ((578, 516), (652, 588)), ((652, 516), (726, 588)), ((726, 516), (800, 588)), ((800, 516), (874, 588)), ((874, 516), (948, 588)),
    ((948, 516), (1022, 588)), ((1022, 516), (1096, 588)), ((1096, 516), (1170, 588)), ((1170, 516), (1244, 588)), ((1244, 516), (1318, 588)),

    ((578, 588), (652, 660)), ((652, 588), (726, 660)), ((726, 588), (800, 660)), ((800, 588), (874, 660)), ((874, 588), (948, 660)),
    ((948, 588), (1022, 660)), ((1022, 588), (1096, 660)), ((1096, 588), (1170, 660)), ((1170, 588), (1244, 660)), ((1244, 588), (1318, 660)),

    ((578, 660), (652, 734)), ((652, 660), (726, 734)), ((726, 660), (800, 734)), ((800, 660), (874, 734)), ((874, 660), (948, 734)),
    ((948, 660), (1022, 734)), ((1022, 660), (1096, 734)), ((1096, 660), (1170, 734)), ((1170, 660), (1244, 734)), ((1244, 660), (1318, 734)),

    ((578, 734), (652, 808)), ((652, 734), (726, 808)), ((726, 734), (800, 808)), ((800, 734), (874, 808)), ((874, 734), (948, 808)),
    ((948, 734), (1022, 808)), ((1022, 734), (1096, 808)), ((1096, 734), (1170, 808)), ((1170, 734), (1244, 808)), ((1244, 734), (1318, 808)),
]


inventory_position = [Slot(topleft,bottomright) for topleft,bottomright in raw_inventory_position] 
inventory = Inventory(inventory_position)

slot_positions = [Slot(topleft, bottomright) for topleft, bottomright in raw_positions]
toolbar = Inventory(slot_positions)

# Hàm chính
def main():
    global current_state

    clock = pygame.time.Clock()

    while True:
        # Lấy sự kiện toàn cục
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop_music()
                pygame.quit()
                sys.exit()

        # Gọi hàm xử lý tương ứng với từng trạng thái
        if current_state == STATE_MENU:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            play_clicked = start_screen(SCREEN, WIDTH, HEIGHT, FONT, BIG_FONT, COLORS,clock)
            if play_clicked:
                current_state = STATE_GAMEPLAY

        elif current_state == STATE_GAMEPLAY:
            result = gameplay_screen(SCREEN, WIDTH, HEIGHT, FONT, BIG_FONT, COLORS,clock,toolbar,inventory)
            if isinstance(result, tuple):
                    action, player, current_day = result
                    if action == "go_to_farming":
                        current_state = STATE_FARMING
                    elif action == "back_to_menu":
                        current_state = STATE_MENU
            elif result == "back_to_menu":
                    current_state = STATE_MENU
        elif current_state == STATE_FARMING:
            result = farming_screen(SCREEN, WIDTH, HEIGHT, FONT, BIG_FONT, COLORS, player, current_day,clock,toolbar,inventory)
            if result == "back_to_gameplay":
                current_state = STATE_GAMEPLAY

        clock.tick(60)

# Chạy game
if __name__ == "__main__":
    main()