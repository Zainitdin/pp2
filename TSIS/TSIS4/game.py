import pygame
import random
import sys
import json
import os

# Import database functions from db.py
from db import save_game, get_top_10, get_personal_best


# Initialize all pygame modules
pygame.init()


# Window size
WIDTH = 600
HEIGHT = 600

# Grid cell size
CELL = 20

# Base game speed
FPS = 10


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (170, 170, 170)
DARK_GRAY = (80, 80, 80)
RED = (220, 0, 0)
DARK_RED = (120, 0, 0)
BLUE = (0, 120, 255)
YELLOW = (255, 220, 0)
PURPLE = (160, 50, 200)
ORANGE = (255, 150, 0)


class SnakeGame:
    def __init__(self):
        # Create the game window
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        # Set window title
        pygame.display.set_caption("TSIS4 Snake Game")

        # Clock controls FPS
        self.clock = pygame.time.Clock()

        # Fonts for normal and big text
        self.font = pygame.font.SysFont("Verdana", 22)
        self.big_font = pygame.font.SysFont("Verdana", 40)

        # Load settings from settings.json
        self.settings = self.load_settings()

        # Username entered on main menu
        self.username = ""

        # Current screen: menu, game, leaderboard, settings, game_over
        self.screen_state = "menu"

        # Prepare all game variables
        self.reset_game()

    def load_settings(self):
        # If settings file does not exist, create default settings
        if not os.path.exists("settings.json"):
            default = {
                "snake_color": [0, 200, 0],
                "grid": True,
                "sound": True
            }

            # Save default settings to file
            with open("settings.json", "w") as file:
                json.dump(default, file, indent=4)

            return default

        # Load settings from existing file
        with open("settings.json", "r") as file:
            return json.load(file)

    def save_settings(self):
        # Save current settings to settings.json
        with open("settings.json", "w") as file:
            json.dump(self.settings, file, indent=4)

    def reset_game(self):
        # Initial snake body.
        # First tuple is the head.
        self.snake = [
            (300, 300),
            (280, 300),
            (260, 300)
        ]

        # Current movement direction
        self.direction = (CELL, 0)

        # Next direction is used to avoid instant reverse bugs
        self.next_direction = (CELL, 0)

        # Score starts from 0
        self.score = 0

        # Counts how many foods were eaten
        self.food_count = 0

        # Initial level
        self.level = 1

        # Current snake speed
        self.speed = FPS

        # List of obstacle blocks
        self.obstacles = []

        # Shield is inactive at start
        self.shield = False

        # Active effect can be speed, slow, or None
        self.active_effect = None

        # Time when active effect should end
        self.effect_end_time = 0

        # Normal food position
        self.food = None

        # Food weight gives different score values
        self.food_weight = 1

        # Time when food appeared
        self.food_spawn_time = 0

        # Food disappears after 6 seconds
        self.food_lifetime = 6000

        # Poison food position
        self.poison = None

        # Power-up position
        self.powerup = None

        # Power-up type: speed, slow, shield
        self.powerup_type = None

        # Time when power-up appeared
        self.powerup_spawn_time = 0

        # Player personal best from database
        self.personal_best = 0

        # Spawn first food and poison
        self.spawn_food()
        self.spawn_poison()

    def draw_text(self, text, x, y, color=WHITE, big=False):
        # Choose big font or normal font
        font = self.big_font if big else self.font

        # Render text into image
        img = font.render(text, True, color)

        # Draw text on screen
        self.screen.blit(img, (x, y))

    def draw_button(self, text, x, y, w, h):
        # Get current mouse position
        mouse = pygame.mouse.get_pos()

        # Create rectangle for button
        rect = pygame.Rect(x, y, w, h)

        # If mouse is on button, make it lighter
        if rect.collidepoint(mouse):
            color = GRAY
        else:
            color = DARK_GRAY

        # Draw button rectangle
        pygame.draw.rect(self.screen, color, rect, border_radius=8)

        # Draw button text
        label = self.font.render(text, True, WHITE)
        self.screen.blit(label, (x + 20, y + 12))

        # Return rect so we can check clicks later
        return rect

    def random_empty_cell(self):
        # Keep generating random positions until valid empty cell is found
        while True:
            x = random.randrange(0, WIDTH, CELL)
            y = random.randrange(80, HEIGHT, CELL)

            pos = (x, y)

            # Position must not overlap snake, food, poison, powerup, obstacles
            if (
                pos not in self.snake
                and pos not in self.obstacles
                and pos != self.food
                and pos != self.poison
                and pos != self.powerup
            ):
                return pos

    def spawn_food(self):
        # Place normal food on empty cell
        self.food = self.random_empty_cell()

        # Food has random weight
        # Bigger weight means bigger score
        self.food_weight = random.choice([1, 2, 3])

        # Save time when food appeared
        self.food_spawn_time = pygame.time.get_ticks()

    def spawn_poison(self):
        # Poison food appears on empty cell
        self.poison = self.random_empty_cell()

    def spawn_powerup(self):
        # Only one power-up can exist on the field
        if self.powerup is None:
            # Small chance to spawn power-up each frame
            if random.randint(1, 100) <= 2:
                self.powerup = self.random_empty_cell()

                # Randomly select power-up type
                self.powerup_type = random.choice(["speed", "slow", "shield"])

                # Save spawn time
                self.powerup_spawn_time = pygame.time.get_ticks()

    def generate_obstacles(self):
        # Clear previous obstacles
        self.obstacles = []

        # Obstacles start only from level 3
        if self.level < 3:
            return

        # Number of obstacles depends on level
        count = self.level + 3

        for _ in range(count):
            pos = self.random_empty_cell()

            # Get snake head position
            head = self.snake[0]

            # Calculate Manhattan distance from obstacle to snake head
            distance = abs(pos[0] - head[0]) + abs(pos[1] - head[1])

            # Do not place obstacles too close to snake head
            # This helps avoid trapping player immediately
            if distance > CELL * 3:
                self.obstacles.append(pos)

    def update_level(self):
        # Every 5 eaten food items = next level
        new_level = self.food_count // 2+ 1

        # If player reached new level
        if new_level > self.level:
            self.level = new_level

            # Increase base speed
            self.speed += 1

            # Generate new obstacles for new level
            self.generate_obstacles()

    def handle_collision(self, new_head):
        # 🔹 Check if snake hits left/right/top/bottom borders
        hit_wall = (
            new_head[0] < 0                  # left wall
            or new_head[0] >= WIDTH         # right wall
            or new_head[1] < 80             # top (UI area border)
            or new_head[1] >= HEIGHT        # bottom wall
        )

        # 🔹 Check if snake collides with itself
        hit_self = new_head in self.snake

        # 🔹 Check if snake hits obstacle block
        hit_obstacle = new_head in self.obstacles

        # 🔹 If ANY type of collision happens
        if hit_wall or hit_self or hit_obstacle:

            # 🛡️ If shield is active → prevent death
            if self.shield:
                # Turn OFF shield after one use
                self.shield = False

                # 🔸 Special behavior for wall collision
                # Snake teleports to opposite side (wrap effect)
                if hit_wall:
                    # Wrap X coordinate
                    x = new_head[0] % WIDTH

                    # Y coordinate stays same
                    y = new_head[1]

                    # Fix vertical boundaries (because top area has UI)
                    if y < 80:
                        y = HEIGHT - CELL     # appear at bottom
                    elif y >= HEIGHT:
                        y = 80                # appear below UI

                    # Return:
                    # False → no game over
                    # (x, y) → corrected safe position
                    return False, (x, y)

                # 🔸 For self or obstacle collision
                # Ignore ONE collision and keep current head position
                return False, self.snake[0]

            # ❌ No shield → game over
            return True, new_head

        # ✅ No collision → continue game normally
        return False, new_head

    def apply_powerup(self):
        # Current time in milliseconds
        now = pygame.time.get_ticks()

        # Speed boost lasts 5 seconds
        if self.powerup_type == "speed":
            self.active_effect = "speed"
            self.effect_end_time = now + 5000

        # Slow motion lasts 5 seconds
        elif self.powerup_type == "slow":
            self.active_effect = "slow"
            self.effect_end_time = now + 5000

        # Shield lasts until next collision
        elif self.powerup_type == "shield":
            self.shield = True

        # Remove power-up from field after collecting
        self.powerup = None
        self.powerup_type = None

    def current_speed(self):
        # Current time
        now = pygame.time.get_ticks()

        # If temporary effect time finished, remove effect
        if self.active_effect and now > self.effect_end_time:
            self.active_effect = None

        # Speed boost
        if self.active_effect == "speed":
            return self.speed + 5

        # Slow motion
        if self.active_effect == "slow":
            return max(4, self.speed - 4)

        # Normal speed
        return self.speed

    def game_over(self):
        # Save result to database
        if self.username:
            save_game(self.username, self.score, self.level)

        # Switch to game over screen
        self.screen_state = "game_over"

    def update_game(self):
        # Update movement direction
        self.direction = self.next_direction

        # Get snake head position
        head_x, head_y = self.snake[0]

        # Get direction values
        dx, dy = self.direction

        # Calculate new head position
        new_head = (head_x + dx, head_y + dy)

        # Check collision before moving
        collision, new_head = self.handle_collision(new_head)

        if collision:
            self.game_over()
            return

        # Add new head to snake
        self.snake.insert(0, new_head)

        # Check if snake ate normal food
        ate_food = new_head == self.food

        # Check if snake ate poison
        ate_poison = new_head == self.poison

        # Check if snake ate power-up
        ate_powerup = new_head == self.powerup

        if ate_food:
            # Increase score by food weight
            self.score += self.food_weight

            # Increase eaten food counter
            self.food_count += 1

            # Spawn new food
            self.spawn_food()

            # Check level progress
            self.update_level()
        else:
            # If food not eaten, remove tail
            # This keeps snake same size
            self.snake.pop()

        if ate_poison:
            # Poison shortens snake by 2 segments
            for _ in range(2):
                if len(self.snake) > 1:
                    self.snake.pop()

            # If snake length becomes too small, game over
            if len(self.snake) <= 1:
                self.game_over()
                return

            # Spawn new poison
            self.spawn_poison()

        if ate_powerup:
            # Activate collected power-up
            self.apply_powerup()

        # Current time
        now = pygame.time.get_ticks()

        # Normal food disappears after timer
        if now - self.food_spawn_time > self.food_lifetime:
            self.spawn_food()

        # Power-up disappears after 8 seconds
        if self.powerup and now - self.powerup_spawn_time > 8000:
            self.powerup = None
            self.powerup_type = None

        # Try to spawn new power-up
        self.spawn_powerup()

    def draw_grid(self):
        # Draw grid only if setting is enabled
        if not self.settings["grid"]:
            return

        # Vertical grid lines
        for x in range(0, WIDTH, CELL):
            pygame.draw.line(self.screen, DARK_GRAY, (x, 80), (x, HEIGHT))

        # Horizontal grid lines
        for y in range(80, HEIGHT, CELL):
            pygame.draw.line(self.screen, DARK_GRAY, (0, y), (WIDTH, y))

    def draw_game(self):
        # Clear screen
        self.screen.fill(BLACK)

        # Draw top information panel
        self.draw_text(f"User: {self.username}", 10, 10)
        self.draw_text(f"Score: {self.score}", 10, 35)
        self.draw_text(f"Level: {self.level}", 180, 35)
        self.draw_text(f"Best: {self.personal_best}", 330, 35)

        # Show shield status
        if self.shield:
            self.draw_text("Shield ON", 450, 35, YELLOW)

        # Separate UI area from game arena
        pygame.draw.line(self.screen, WHITE, (0, 80), (WIDTH, 80), 2)

        # Draw grid
        self.draw_grid()

        # Draw obstacles
        for block in self.obstacles:
            pygame.draw.rect(self.screen, GRAY, (*block, CELL, CELL))

        # Convert JSON list to tuple for pygame color
        snake_color = tuple(self.settings["snake_color"])

        # Draw snake
        for segment in self.snake:
            pygame.draw.rect(self.screen, snake_color, (*segment, CELL, CELL))

        # Draw food with size depending on weight
        food_size = 8 + self.food_weight * 4

        food_rect = pygame.Rect(
            self.food[0] + (CELL - food_size) // 2,
            self.food[1] + (CELL - food_size) // 2,
            food_size,
            food_size
        )

        pygame.draw.rect(self.screen, RED, food_rect)

        # Draw poison food
        if self.poison:
            pygame.draw.rect(self.screen, DARK_RED, (*self.poison, CELL, CELL))

        # Draw power-up
        if self.powerup:
            if self.powerup_type == "speed":
                color = ORANGE
            elif self.powerup_type == "slow":
                color = BLUE
            else:
                color = PURPLE

            pygame.draw.rect(self.screen, color, (*self.powerup, CELL, CELL))

        # Update display
        pygame.display.update()

    def menu_screen(self):
        # Clear screen
        self.screen.fill(BLACK)

        # Game title
        self.draw_text("TSIS4 Snake Game", 120, 70, WHITE, big=True)

        # Username input
        self.draw_text("Enter username:", 180, 150)
        self.draw_text(self.username + "|", 210, 185, YELLOW)

        # Menu buttons
        play_btn = self.draw_button("Play", 220, 250, 160, 50)
        lb_btn = self.draw_button("Leaderboard", 220, 320, 160, 50)
        settings_btn = self.draw_button("Settings", 220, 390, 160, 50)
        quit_btn = self.draw_button("Quit", 220, 460, 160, 50)

        pygame.display.update()

        # Return buttons for click checking
        return play_btn, lb_btn, settings_btn, quit_btn

    def leaderboard_screen(self):
        # Clear screen
        self.screen.fill(BLACK)

        # Title
        self.draw_text("Leaderboard", 180, 40, WHITE, big=True)

        # Fetch top 10 scores from database
        rows = get_top_10()

        y = 120

        # Table header
        self.draw_text("Rank  User       Score  Level  Date", 40, 90, YELLOW)

        # Draw each row
        for i, row in enumerate(rows, start=1):
            username, score, level, date = row
            date_text = date.strftime("%Y-%m-%d")

            self.draw_text(
                f"{i:<5} {username:<10} {score:<6} {level:<5} {date_text}",
                40,
                y
            )

            y += 35

        # Back button
        back_btn = self.draw_button("Back", 220, 520, 160, 50)

        pygame.display.update()

        return back_btn

    def settings_screen(self):
        # Clear screen
        self.screen.fill(BLACK)

        # Title
        self.draw_text("Settings", 210, 60, WHITE, big=True)

        # Toggle grid button
        grid_btn = self.draw_button(
            f"Grid: {'ON' if self.settings['grid'] else 'OFF'}",
            180,
            160,
            250,
            50
        )

        # Toggle sound button
        sound_btn = self.draw_button(
            f"Sound: {'ON' if self.settings['sound'] else 'OFF'}",
            180,
            230,
            250,
            50
        )

        # Snake color buttons
        green_btn = self.draw_button("Green Snake", 180, 300, 250, 50)
        blue_btn = self.draw_button("Blue Snake", 180, 370, 250, 50)

        # Save button
        save_btn = self.draw_button("Save & Back", 180, 470, 250, 50)

        pygame.display.update()

        return grid_btn, sound_btn, green_btn, blue_btn, save_btn

    def game_over_screen(self):
        # Clear screen
        self.screen.fill(BLACK)

        # Game over title
        self.draw_text("Game Over", 180, 90, RED, big=True)

        # Final results
        self.draw_text(f"Final Score: {self.score}", 190, 180)
        self.draw_text(f"Level Reached: {self.level}", 190, 220)
        self.draw_text(f"Personal Best: {max(self.score, self.personal_best)}", 190, 260)

        # Buttons
        retry_btn = self.draw_button("Retry", 220, 350, 160, 50)
        menu_btn = self.draw_button("Main Menu", 220, 420, 160, 50)

        pygame.display.update()

        return retry_btn, menu_btn

    def handle_keydown(self, event):
        # Username typing only works in menu
        if self.screen_state == "menu":

            # Delete last character
            if event.key == pygame.K_BACKSPACE:
                self.username = self.username[:-1]

            # Add typed character
            elif len(self.username) < 12 and event.unicode.isprintable():
                self.username += event.unicode

        # Snake movement only works during game
        elif self.screen_state == "game":

            # Prevent moving directly opposite direction
            if event.key == pygame.K_UP and self.direction != (0, CELL):
                self.next_direction = (0, -CELL)

            elif event.key == pygame.K_DOWN and self.direction != (0, -CELL):
                self.next_direction = (0, CELL)

            elif event.key == pygame.K_LEFT and self.direction != (CELL, 0):
                self.next_direction = (-CELL, 0)

            elif event.key == pygame.K_RIGHT and self.direction != (-CELL, 0):
                self.next_direction = (CELL, 0)

    def run(self):
        # Main game loop
        while True:
            buttons = None

            # Draw current screen
            if self.screen_state == "menu":
                buttons = self.menu_screen()

            elif self.screen_state == "leaderboard":
                buttons = self.leaderboard_screen()

            elif self.screen_state == "settings":
                buttons = self.settings_screen()

            elif self.screen_state == "game_over":
                buttons = self.game_over_screen()

            elif self.screen_state == "game":
                self.update_game()
                self.draw_game()

            # Process all events
            for event in pygame.event.get():

                # Close window
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Keyboard events
                if event.type == pygame.KEYDOWN:
                    self.handle_keydown(event)

                # Mouse click events
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()

                    # Menu buttons
                    if self.screen_state == "menu":
                        play_btn, lb_btn, settings_btn, quit_btn = buttons

                        if play_btn.collidepoint(mouse) and self.username.strip():
                            self.reset_game()
                            self.personal_best = get_personal_best(self.username)
                            self.screen_state = "game"

                        elif lb_btn.collidepoint(mouse):
                            self.screen_state = "leaderboard"

                        elif settings_btn.collidepoint(mouse):
                            self.screen_state = "settings"

                        elif quit_btn.collidepoint(mouse):
                            pygame.quit()
                            sys.exit()

                    # Leaderboard back button
                    elif self.screen_state == "leaderboard":
                        back_btn = buttons

                        if back_btn.collidepoint(mouse):
                            self.screen_state = "menu"

                    # Settings buttons
                    elif self.screen_state == "settings":
                        grid_btn, sound_btn, green_btn, blue_btn, save_btn = buttons

                        if grid_btn.collidepoint(mouse):
                            self.settings["grid"] = not self.settings["grid"]

                        elif sound_btn.collidepoint(mouse):
                            self.settings["sound"] = not self.settings["sound"]

                        elif green_btn.collidepoint(mouse):
                            self.settings["snake_color"] = [0, 200, 0]

                        elif blue_btn.collidepoint(mouse):
                            self.settings["snake_color"] = [0, 120, 255]

                        elif save_btn.collidepoint(mouse):
                            self.save_settings()
                            self.screen_state = "menu"

                    # Game over buttons
                    elif self.screen_state == "game_over":
                        retry_btn, menu_btn = buttons

                        if retry_btn.collidepoint(mouse):
                            self.reset_game()
                            self.personal_best = get_personal_best(self.username)
                            self.screen_state = "game"

                        elif menu_btn.collidepoint(mouse):
                            self.screen_state = "menu"

            # Control game speed
            self.clock.tick(self.current_speed())