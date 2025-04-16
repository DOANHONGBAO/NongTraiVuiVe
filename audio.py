import pygame
import time
import threading

# Danh sách đường dẫn nhạc nền
MUSIC_TRACKS = [
    "assets/audios/music1.mp3",
    "assets/audios/music2.mp3",
    "assets/audios/music3.mp3"
]

MUSIC_INTERVAL = 300  # 5 phút = 300 giây
current_track_index = 0
running = True

def play_music_loop():
    global current_track_index
    pygame.mixer.init()
    
    while running:
        track_path = MUSIC_TRACKS[current_track_index]
        pygame.mixer.music.load(track_path)
        pygame.mixer.music.play()
        
        start_time = time.time()
        while time.time() - start_time < MUSIC_INTERVAL and running:
            time.sleep(1)
        
        current_track_index = (current_track_index + 1) % len(MUSIC_TRACKS)

def start_background_music():
    threading.Thread(target=play_music_loop, daemon=True).start()

def stop_music():
    global running
    running = False
    pygame.mixer.music.stop()
