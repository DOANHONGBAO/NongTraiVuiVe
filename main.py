import pygame
import sys
import json
import os
import tempfile
from menu import start_screen
from gameplay import gameplay_screen
from farming_screen import farming_screen
from audio import start_background_music, stop_music
from login import login_screen
from player import Player
from settings_manager import Settings, settings_screen
pygame.mixer.init()

pygame.init()
WIDTH, HEIGHT = 1915, 1020
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nông Trại Vui Vẻ")

COLORS = {
    "WHITE": (255, 255, 255),
    "GREEN": (150, 200, 150),
    "DARK_GREEN": (60, 130, 60),
    "BLACK": (0, 0, 0),
    "YELLOW": (255, 215, 0),
    "BROWN": (160, 100, 50),
    "LIGHT_GREEN": (180, 255, 180),
    "DARK_GRAY": (125, 125, 125),
    "LIGHT_BROWN": (3, 3, 3)
}

def find_font(font_path):
    potential_paths = [font_path, f"attached_assets/{font_path}"]
    for path in potential_paths:
        if os.path.exists(path):
            return path
    print(f"Warning: Could not find font {font_path}, using system default")
    return None

try:
    font_path = find_font("assets/fonts/arcade-among-1.otf")
    if font_path:
        FONT = pygame.font.Font(font_path, 24)
        BIG_FONT = pygame.font.Font(font_path, 36)
    else:
        FONT = pygame.font.SysFont("Arial", 24)
        BIG_FONT = pygame.font.SysFont("Arial", 36)
except Exception as e:
    print(f"Error loading font: {e}, using system default")
    FONT = pygame.font.SysFont("Arial", 24)
    BIG_FONT = pygame.font.SysFont("Arial", 36)

STATE_MENU = "menu"
STATE_LOGIN = "login"
STATE_GAMEPLAY = "gameplay"
STATE_FARMING = "farming"
current_state = STATE_MENU
current_user = None
player = None
current_day = 1

def save_player_data(player, current_day):
    if player and current_user:
        try:
            players_data = {}
            if os.path.exists('players.json'):
                with open('players.json', 'r') as f:
                    if os.path.getsize('players.json') > 0:
                        players_data = json.load(f)
                    else:
                        print("Warning: players.json is empty, initializing as empty dict")
            players_data[current_user] = player.to_dict()
            players_data[current_user]['current_day'] = current_day
            players_data[current_user]['yard'] = []
            with tempfile.NamedTemporaryFile('w', delete=False, suffix='.json') as temp_file:
                json.dump(players_data, temp_file, indent=4)
                temp_file_name = temp_file.name
            os.replace(temp_file_name, 'players.json')
            print(f"Updated player data for {current_user} in players.json")
        except Exception as e:
            print(f"Error saving player data: {e}")

def main():
    global current_state, player, current_day, current_user
    clock = pygame.time.Clock()
    last_save_time = pygame.time.get_ticks()
    SAVE_INTERVAL = 60000
    start_background_music()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if current_user:
                    save_player_data(player, current_day)
                stop_music()
                pygame.quit()
                sys.exit()

        current_time = pygame.time.get_ticks()
        if current_time - last_save_time >= SAVE_INTERVAL and current_user:
            save_player_data(player, current_day)
            last_save_time = current_time

        if current_state == STATE_MENU:
            play_clicked = start_screen(SCREEN, WIDTH, HEIGHT, FONT, BIG_FONT, COLORS, clock)
            if play_clicked:
                current_state = STATE_LOGIN

        elif current_state == STATE_LOGIN:
            player = Player()
            status, player_data = login_screen(SCREEN, WIDTH, HEIGHT, FONT, BIG_FONT, COLORS, clock, current_user, player, current_day)
            if status == "success":
                current_user, player, current_day = player_data['current_user'], player_data['player'], player_data['current_day']
                current_state = STATE_GAMEPLAY

        elif current_state == STATE_GAMEPLAY:
            result = gameplay_screen(SCREEN, WIDTH, HEIGHT, FONT, BIG_FONT, COLORS, clock, player)
            if isinstance(result, tuple):
                action, player, current_day = result
                save_player_data(player, current_day)
                if action == "go_to_farming":
                    current_state = STATE_FARMING
                elif action == "back_to_menu":
                    current_state = STATE_MENU
            elif result == "back_to_menu":
                save_player_data(player, current_day)
                current_state = STATE_MENU

        elif current_state == STATE_FARMING:
            result = farming_screen(SCREEN, WIDTH, HEIGHT, FONT, BIG_FONT, COLORS, player, current_day, clock)
            if result == "back_to_gameplay":
                save_player_data(player, current_day)
                current_state = STATE_GAMEPLAY

        clock.tick(60)

if __name__ == "__main__":
    main()
