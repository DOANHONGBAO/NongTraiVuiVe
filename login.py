import pygame
import json
import os

DATA_FILE = 'players.json'

def load_players():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump({}, f)
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_players(players):
    with open(DATA_FILE, 'w') as f:
        json.dump(players, f, indent=4)

def login_screen(screen, width, height, font, big_font, colors, clock):
    players = load_players()
    
    username = ''
    password = ''
    active_input = 'username'
    error_message = ''
    
    input_box_username = pygame.Rect(width//2 - 150, height//2 - 60, 300, 50)
    input_box_password = pygame.Rect(width//2 - 150, height//2 + 20, 300, 50)
    
    while True:
        screen.fill(colors["WHITE"])
        
        pygame.draw.rect(screen, colors["DARK_GRAY"], input_box_username, 2)
        pygame.draw.rect(screen, colors["DARK_GRAY"], input_box_password, 2)

        username_surface = font.render(username, True, colors["BLACK"])
        password_hidden = '*' * len(password)
        password_surface = font.render(password_hidden, True, colors["BLACK"])
        
        screen.blit(username_surface, (input_box_username.x + 5, input_box_username.y + 10))
        screen.blit(password_surface, (input_box_password.x + 5, input_box_password.y + 10))
        
        label_user = font.render("Username:", True, colors["BLACK"])
        label_pass = font.render("Password:", True, colors["BLACK"])
        
        screen.blit(label_user, (input_box_username.x, input_box_username.y - 30))
        screen.blit(label_pass, (input_box_password.x, input_box_password.y - 30))
        
        if error_message:
            error_surface = font.render(error_message, True, (255, 0, 0))
            screen.blit(error_surface, (width//2 - error_surface.get_width()//2, height//2 + 90))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", None
            if event.type == pygame.KEYDOWN:
                if active_input == 'username':
                    if event.key == pygame.K_RETURN:
                        active_input = 'password'
                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode
                elif active_input == 'password':
                    if event.key == pygame.K_RETURN:
                        if username in players:
                            if players[username]['password'] == password:
                                # Login thành công → load data
                                return "login", players[username]
                            else:
                                error_message = "Sai mật khẩu!"
                                password = ''
                        else:
                            # Tạo user mới
                            players[username] = {
                                'password': password,
                                'current_day': 1,
                                'inventory': [],
                                'other_data': {}
                            }
                            save_players(players)
                            return "new_user", players[username]
                    elif event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    else:
                        password += event.unicode

        clock.tick(30)
