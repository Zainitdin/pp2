import pygame
from persistence import load_leaderboard, save_settings


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
DARK_GRAY = (70, 70, 70)


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, screen, font):
        pygame.draw.rect(screen, GRAY, self.rect, border_radius=8)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=8)

        text = font.render(self.text, True, BLACK)
        screen.blit(
            text,
            (
                self.rect.centerx - text.get_width() // 2,
                self.rect.centery - text.get_height() // 2
            )
        )

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)


def get_username(screen, clock):
    font = pygame.font.SysFont("Verdana", 28)
    small_font = pygame.font.SysFont("Verdana", 20)

    name = ""

    while True:
        screen.fill(WHITE)

        title = font.render("Enter your name:", True, BLACK)
        screen.blit(title, (70, 180))

        box = pygame.Rect(70, 230, 260, 45)
        pygame.draw.rect(screen, WHITE, box)
        pygame.draw.rect(screen, BLACK, box, 2)

        name_text = small_font.render(name, True, BLACK)
        screen.blit(name_text, (80, 240))

        hint = small_font.render("Press ENTER to start", True, DARK_GRAY)
        screen.blit(hint, (90, 300))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip():
                    return name

                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]

                else:
                    if len(name) < 12:
                        name += event.unicode

        pygame.display.update()
        clock.tick(60)


def main_menu(screen, clock):
    font = pygame.font.SysFont("Verdana", 28)

    buttons = {
        "play": Button(100, 180, 200, 50, "Play"),
        "leaderboard": Button(100, 250, 200, 50, "Leaderboard"),
        "settings": Button(100, 320, 200, 50, "Settings"),
        "quit": Button(100, 390, 200, 50, "Quit")
    }

    while True:
        screen.fill(WHITE)

        title = font.render("TSIS 3 Racer", True, BLACK)
        screen.blit(title, (90, 90))

        for button in buttons.values():
            button.draw(screen, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            for key, button in buttons.items():
                if button.clicked(event):
                    return key

        pygame.display.update()
        clock.tick(60)


def leaderboard_screen(screen, clock):
    font = pygame.font.SysFont("Verdana", 24)
    small_font = pygame.font.SysFont("Verdana", 18)

    back = Button(120, 520, 160, 45, "Back")

    while True:
        screen.fill(WHITE)

        title = font.render("Top 10 Scores", True, BLACK)
        screen.blit(title, (105, 40))

        scores = load_leaderboard()

        y = 100
        for i, entry in enumerate(scores):
            text = f"{i + 1}. {entry['name']} | Score: {entry['score']} | Dist: {entry['distance']}m"
            line = small_font.render(text, True, BLACK)
            screen.blit(line, (25, y))
            y += 35

        back.draw(screen, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if back.clicked(event):
                return "menu"

        pygame.display.update()
        clock.tick(60)


def settings_screen(screen, clock, settings):
    font = pygame.font.SysFont("Verdana", 22)

    sound_button = Button(80, 150, 240, 45, "")
    color_button = Button(80, 230, 240, 45, "")
    difficulty_button = Button(80, 310, 240, 45, "")
    back_button = Button(120, 500, 160, 45, "Back")

    colors = ["blue", "red", "green", "yellow"]
    difficulties = ["Easy", "Normal", "Hard"]

    while True:
        screen.fill(WHITE)

        title = font.render("Settings", True, BLACK)
        screen.blit(title, (140, 70))

        sound_button.text = f"Sound: {'ON' if settings['sound'] else 'OFF'}"
        color_button.text = f"Car: {settings['car_color']}"
        difficulty_button.text = f"Difficulty: {settings['difficulty']}"

        sound_button.draw(screen, font)
        color_button.draw(screen, font)
        difficulty_button.draw(screen, font)
        back_button.draw(screen, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if sound_button.clicked(event):
                settings["sound"] = not settings["sound"]
                save_settings(settings)

            if color_button.clicked(event):
                current = colors.index(settings["car_color"])
                settings["car_color"] = colors[(current + 1) % len(colors)]
                save_settings(settings)

            if difficulty_button.clicked(event):
                current = difficulties.index(settings["difficulty"])
                settings["difficulty"] = difficulties[(current + 1) % len(difficulties)]
                save_settings(settings)

            if back_button.clicked(event):
                return "menu"

        pygame.display.update()
        clock.tick(60)


def game_over_screen(screen, clock, score, distance, coins):
    font = pygame.font.SysFont("Verdana", 26)
    small_font = pygame.font.SysFont("Verdana", 20)

    retry = Button(100, 350, 200, 50, "Retry")
    menu = Button(100, 420, 200, 50, "Main Menu")

    while True:
        screen.fill(WHITE)

        title = font.render("Game Over", True, BLACK)
        screen.blit(title, (120, 120))

        info1 = small_font.render(f"Score: {score}", True, BLACK)
        info2 = small_font.render(f"Distance: {distance}m", True, BLACK)
        info3 = small_font.render(f"Coins: {coins}", True, BLACK)

        screen.blit(info1, (120, 190))
        screen.blit(info2, (120, 220))
        screen.blit(info3, (120, 250))

        retry.draw(screen, font)
        menu.draw(screen, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if retry.clicked(event):
                return "retry"

            if menu.clicked(event):
                return "menu"

        pygame.display.update()
        clock.tick(60)