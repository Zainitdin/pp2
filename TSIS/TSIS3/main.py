import pygame

from persistence import load_settings
from ui import (
    main_menu,
    get_username,
    leaderboard_screen,
    settings_screen,
    game_over_screen
)
from racer import run_game


pygame.init()

WIDTH = 400
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 3 Racer Game")

clock = pygame.time.Clock()

settings = load_settings()


while True:
    choice = main_menu(screen, clock)

    if choice == "play":
        username = get_username(screen, clock)

        while True:
            result, score, distance, coins = run_game(
                screen,
                clock,
                username,
                settings
            )

            if result == "quit":
                pygame.quit()
                exit()

            action = game_over_screen(
                screen,
                clock,
                score,
                distance,
                coins
            )

            if action == "retry":
                continue

            elif action == "menu":
                break

            elif action == "quit":
                pygame.quit()
                exit()

    elif choice == "leaderboard":
        result = leaderboard_screen(screen, clock)

        if result == "quit":
            pygame.quit()
            exit()

    elif choice == "settings":
        result = settings_screen(screen, clock, settings)

        if result == "quit":
            pygame.quit()
            exit()

    elif choice == "quit":
        pygame.quit()
        exit()