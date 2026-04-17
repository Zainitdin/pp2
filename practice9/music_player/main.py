import pygame
import sys
from player import MusicPlayer

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption("Music Player")

playlist = [
    "/Users/zainitdinspv/work/practice9/music_player/music/Halestorm - Empire State Of Mind (Jay-Z).mp3",
    "/Users/zainitdinspv/work/practice9/music_player/music/The Weeknd feat. Playboi Carti - Timeless.mp3"
]

player = MusicPlayer(playlist)

font = pygame.font.SysFont(None, 30)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            elif event.key == pygame.K_s:
                player.stop()
            elif event.key == pygame.K_n:
                player.next()
            elif event.key == pygame.K_b:
                player.previous()
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

    screen.fill((255, 255, 255))

    text = font.render(f"Track: {player.current + 1}", True, (0, 0, 0))
    screen.blit(text, (100, 80))

    pygame.display.flip()