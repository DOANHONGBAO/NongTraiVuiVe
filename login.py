import pygame
import json
import os
from audio import stop_music
from player import Player
from items import Slot

def draw_gradient(screen, start_color, end_color, width, height):
    """Draw a vertical gradient background."""
    for y in range(height):
        ratio = y / height
        r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
        g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
        b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (width, y))

def draw_summer_decorations(screen, width, height):
    """Draw summer farming-themed decorations."""
    # Draw a semi-transparent sun in the top-left corner
    sun_color = (255, 200, 0, 100)  # Semi-transparent yellow
    pygame.draw.circle(screen, sun_color, (100, 100), 80)
    
    # Draw grass-like shapes at the bottom
    grass_color = (0, 150, 0, 80)  # Semi-transparent green
    for x in range(0, width, 20):
        pygame.draw.polygon(screen, grass_color, [
            (x, height - 20),
            (x + 10, height - 40),
            (x + 20, height - 20)
        ])
    
    # Add a semi-transparent overlay for depth
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 10))  # Very faint dark overlay
    screen.blit(overlay, (0, 0))

def login_screen(screen, width, height, font, big_font, colors, clock, current_user, player, current_day):
    username = ""
    input_active = True
    error_message = ""
    input_rect = pygame.Rect(width // 2 - 200, height // 2 - 50, 400, 50)
    fade_alpha = 0  # For fade-in animation
    shadow_offset = 5  # For input box shadow
    
    # Summer-themed gradient colors
    gradient_start = (255, 245, 150)  # Light yellow for summer sun
    gradient_end = (100, 200, 100)    # Green for fields
    shadow_color = (50, 50, 50, 100)  # Semi-transparent gray
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop_music()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN and username:
                    current_user = username
                    player_file = 'players.json'
                    try:
                        if os.path.exists(player_file):
                            with open(player_file, 'r') as f:
                                if os.path.getsize(player_file) > 0:
                                    players_data = json.load(f)
                                    if username in players_data:
                                        player = Player.from_dict(players_data[username])
                                        current_day = players_data[username].get('current_day', 1)
                                    else:
                                        player = Player()
                                else:
                                    print("Warning: players.json is empty, creating new player")
                                    player = Player()
                        else:
                            player = Player()
                        
                        return "success", {
                            'current_user': current_user,
                            'player': player,
                            'current_day': current_day
                        }
                    except json.JSONDecodeError as e:
                        print(f"Error decoding players.json: {e}. Creating new player")
                        player = Player()
                        return "success", {
                            'current_user': current_user,
                            'player': player,
                            'current_day': current_day
                        }
                    except Exception as e:
                        print(f"Error loading player data: {e}")
                        error_message = "Lỗi khi tải dữ liệu người chơi"
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    if len(username) < 20:
                        username += event.unicode
        
        # Draw gradient background and summer decorations
        draw_gradient(screen, gradient_start, gradient_end, width, height)
        draw_summer_decorations(screen, width, height)
        
        # Fade-in animation for title and input box
        if fade_alpha < 255:
            fade_alpha = min(fade_alpha + 5, 255)
        
        # Render title with fade-in
        title_text = big_font.render("ĐĂNG NHẬP", True, colors["BLACK"])
        title_surface = pygame.Surface((title_text.get_width(), title_text.get_height()), pygame.SRCALPHA)
        title_surface.blit(title_text, (0, 0))
        title_surface.set_alpha(fade_alpha)
        screen.blit(title_surface, (width // 2 - title_text.get_width() // 2, height // 2 - 150))
        
        # Draw input box shadow
        shadow_rect = input_rect.copy()
        shadow_rect.x += shadow_offset
        shadow_rect.y += shadow_offset
        pygame.draw.rect(screen, shadow_color, shadow_rect, border_radius=10)
        
        # Draw input box with rounded corners
        pygame.draw.rect(screen, colors["WHITE"], input_rect, border_radius=10)
        pygame.draw.rect(screen, colors["BLACK"], input_rect, 2, border_radius=10)
        
        # Render username text, centered vertically and adjusted horizontally
        username_text = font.render(username, True, colors["BLACK"])
        text_rect = username_text.get_rect()
        text_x = input_rect.x + 15
        text_y = input_rect.y + (input_rect.height - text_rect.height) // 2  # Center vertically
        screen.blit(username_text, (text_x, text_y))
        
        # Render prompt text with fade-in
        prompt_text = font.render("Nhập tên người chơi và nhấn Enter", True, colors["BLACK"])
        prompt_surface = pygame.Surface((prompt_text.get_width(), prompt_text.get_height()), pygame.SRCALPHA)
        prompt_surface.blit(prompt_text, (0, 0))
        prompt_surface.set_alpha(fade_alpha)
        screen.blit(prompt_surface, (width // 2 - prompt_text.get_width() // 2, height // 2 + 20))
        
        # Render error message if present
        if error_message:
            error_text = font.render(error_message, True, colors["BLACK"])
            screen.blit(error_text, (width // 2 - error_text.get_width() // 2, height // 2 + 60))
        
        pygame.display.flip()
        clock.tick(60)