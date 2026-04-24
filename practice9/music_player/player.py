import pygame
import time
import os

class MusicPlayer:
    def __init__(self, playlist):
        self.playlist = playlist
        self.current = 0
        self.start_time = 0
        self.is_playing = False

    def play(self):
        pygame.mixer.music.load(self.playlist[self.current])
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play()
        self.start_time = time.time()
        self.is_playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next(self):
        self.current = (self.current + 1) % len(self.playlist)
        self.play()

    def previous(self):
        self.current = (self.current - 1) % len(self.playlist)
        self.play()

    # ✅ Track name
    def get_current_track(self):
        return os.path.basename(self.playlist[self.current])

    # ✅ Playback position (seconds)
    def get_position(self):
        pos = pygame.mixer.music.get_pos()  # milliseconds
        if pos == -1:
            return 0
        return pos // 1000  # seconds


    def get_length(self):
        return 180  # temporary safe fallback

    # ✅ Progress percentage
    def get_progress(self):
        length = self.get_length()
        if length == 0:
            return 0
        return self.get_position() / length