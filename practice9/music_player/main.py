import pygame
import sys
from player import MusicPlayer

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption("Music Player")

playlist = [
    "/Users/zainitdinspv/work/practice9/music_player/music/Chris Isaak - Wicked Game.mp3",
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

    title= font.render(player.get_current_track(), True, (0, 0, 0))
    screen.blit(title, (20,15))

    
    current_time =  player.get_position()
    total_time = player.get_length()
    time_text= font.render(f"{current_time}s / {total_time}s",True, ( 0, 0, 0))
    screen.blit(time_text, (20, 45))

    bar_x = 20

    bar_y = 80

    bar_width = 360

    bar_height = 10

    # current time in seconds

    current_time = player.get_position()

    total_time = player.get_length()

    # avoid division crash

    if total_time == 0:

        progress = 0

    else:

        progress = min(current_time / total_time, 1)

    # background bar

    pygame.draw.rect(screen, (200, 200, 200), (bar_x, bar_y, bar_width, bar_height))

    # filled bar

    pygame.draw.rect(

        screen,

        (30, 144, 255),

        (bar_x, bar_y, int(bar_width * progress), bar_height)

    )

    pygame.display.flip()