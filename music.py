import simpleaudio as sa
import time
import random
import threading
import os

# List of 10 audio file paths (update with actual file paths)
AUDIO_DIR = "./assets/"
AUDIO_FILES = [ os.path.join(AUDIO_DIR, f"audio{i}.wav") for i in range(5)]

# Dictionary to store audio playback state
players = {}
playing = {}

def play_audio(file_path):
    """Plays an audio file in a loop."""
    wave_obj = sa.WaveObject.from_wave_file(file_path)
    while True:
        if playing[file_path]:
            play_obj = wave_obj.play()
            players[file_path] = play_obj
            play_obj.wait_done()

def toggle_audio():
    """Toggles a random audio file between playing and paused."""
    file_to_toggle = random.choice(AUDIO_FILES)
    playing[file_to_toggle] = not playing[file_to_toggle]
    state = "Playing" if playing[file_to_toggle] else "Paused"
    print(f"Toggled: {file_to_toggle} -> {state}")

def main():
    # Initialize playback states
    for file in AUDIO_FILES:
        playing[file] = False
        thread = threading.Thread(target=play_audio, args=(file,), daemon=True)
        thread.start()

    # Loop to toggle a random track every 5 seconds
    while True:
        time.sleep(2)
        toggle_audio()

if __name__ == "__main__":
    main()
