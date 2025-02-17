import pygame
import time
import random
import threading
import os

# List of 10 audio file paths (update with actual file paths)
AUDIO_DIR = "./assets/"
AUDIO_FILES = [os.path.join(AUDIO_DIR, f"audio{i}.wav") for i in range(5)]

# Dictionary to store audio playback state
players = {}
playing = {}
playing_lock = threading.Lock()

def play_audio(file_path):
    """Plays an audio file in a loop."""
    pygame.mixer.init()
    channel = pygame.mixer.Channel(AUDIO_FILES.index(file_path))
    sound = pygame.mixer.Sound(file_path)
    while True:
        with playing_lock:
            is_playing = playing.get(file_path, False)
        if is_playing:
            if not channel.get_busy():
                channel.play(sound, -1)  # -1 means loop forever
            players[file_path] = channel
            while playing.get(file_path, False) and channel.get_busy():
                time.sleep(0.1)  # Check periodically
            if not playing.get(file_path, False):
                channel.stop()

def toggle_audio():
    """Toggles a random audio file between playing and paused."""
    file_to_toggle = random.choice(AUDIO_FILES)
    with playing_lock:
        playing[file_to_toggle] = not playing.get(file_to_toggle, False)
    state = "Playing" if playing[file_to_toggle] else "Paused"
    print(f"Toggled: {file_to_toggle} -> {state}")

def main():
    # Initialize pygame mixer
    pygame.mixer.init()
    pygame.mixer.set_num_channels(len(AUDIO_FILES))
    
    # Initialize playback states
    for file in AUDIO_FILES:
        with playing_lock:
            playing[file] = False
        thread = threading.Thread(target=play_audio, args=(file,))
        thread.daemon = True
        thread.start()

    # Loop to toggle a random track every 5 seconds
    while True:
        time.sleep(random.randint(1, 5))
        toggle_audio()

if __name__ == "__main__":
    main()
