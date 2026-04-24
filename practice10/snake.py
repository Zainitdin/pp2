import pygame
import sys
import random

# -----------------------------
# Initialize pygame
# -----------------------------
pygame.init()

# -----------------------------
# Screen settings
# -----------------------------
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
CELL_SIZE = 20

# Number of cells in the grid
GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // CELL_SIZE

# Create game window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake Game")

# -----------------------------
# Colors
# -----------------------------
BLACK = (255, 255, 255)
WHITE = (0, 0, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 120, 0)
RED = (220, 0, 0)
GRAY = (100, 100, 100)
BLUE = (50, 150, 255)

# -----------------------------
# Fonts
# -----------------------------
font = pygame.font.SysFont("Verdana", 20)
big_font = pygame.font.SysFont("Verdana", 40)

# -----------------------------
# Clock and game speed
# -----------------------------
clock = pygame.time.Clock()
BASE_SPEED = 7   # starting speed

# -----------------------------
# Walls
# We create several wall blocks
# Each wall is stored as a (x, y) tuple in grid coordinates
# -----------------------------
walls = {
    (10, 10), (11, 10), (12, 10), (13, 10),
    (20, 15), (20, 16), (20, 17), (20, 18),
    (5, 22), (6, 22), (7, 22), (8, 22),
    (24, 5), (24, 6), (24, 7), (24, 8)
}

# -----------------------------
# Function: draw text on screen
# -----------------------------
def draw_text(text, font_obj, color, x, y):
    img = font_obj.render(text, True, color)
    screen.blit(img, (x, y))

# -----------------------------
# Function: draw one grid cell
# -----------------------------
def draw_cell(color, position):
    x, y = position
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect)

# -----------------------------
# Function: generate food
# Food must NOT appear:
# - on snake body
# - on wall
# -----------------------------
def generate_food(snake, walls):
    while True:
        food_position = (
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1)
        )

        if food_position not in snake and food_position not in walls:
            return food_position

# -----------------------------
# Function: show game over screen
# -----------------------------
def game_over_screen(score, level):
    screen.fill(BLACK)

    game_over_text = big_font.render("Game Over", True, RED)
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    exit_text = font.render("Press any key to exit", True, WHITE)

    screen.blit(game_over_text, (WINDOW_WIDTH // 2 - 120, WINDOW_HEIGHT // 2 - 80))
    screen.blit(score_text, (WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2))
    screen.blit(level_text, (WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2 + 30))
    screen.blit(exit_text, (WINDOW_WIDTH // 2 - 110, WINDOW_HEIGHT // 2 + 80))

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                pygame.quit()
                sys.exit()

# -----------------------------
# Main game function
# -----------------------------
def main():
    # Snake starts with 3 blocks
    snake = [(5, 5), (4, 5), (3, 5)]

    # Initial direction of snake movement
    direction = (1, 0)  # moving right

    # Create first food
    food = generate_food(snake, walls)

    # Score and level
    score = 0
    level = 1

    # Snake speed
    speed = BASE_SPEED

    # Number of foods needed to move to next level
    foods_per_level = 4

    # Game loop
    while True:
        # -----------------------------
        # Handle events
        # -----------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # Change direction with arrow keys
                # We also prevent the snake from going directly backwards
                if event.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)

        # -----------------------------
        # Move snake
        # -----------------------------
        head_x, head_y = snake[0]
        dx, dy = direction
        new_head = (head_x + dx, head_y + dy)

        # -----------------------------
        # Check border collision
        # Snake dies if it leaves playing area
        # -----------------------------
        if (
            new_head[0] < 0 or
            new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or
            new_head[1] >= GRID_HEIGHT
        ):
            game_over_screen(score, level)

        # -----------------------------
        # Check collision with itself
        # -----------------------------
        if new_head in snake:
            game_over_screen(score, level)

        # -----------------------------
        # Check collision with walls
        # -----------------------------
        if new_head in walls:
            game_over_screen(score, level)

        # Add new head to snake
        snake.insert(0, new_head)

        # -----------------------------
        # Check if snake eats food
        # -----------------------------
        if new_head == food:
            score += 1

            # Generate new food in valid position
            food = generate_food(snake, walls)

            # Level system:
            # every 4 foods -> next level
            if score % foods_per_level == 0:
                level += 1
                speed += 2   # increase speed when next level starts

        else:
            # If food is not eaten, remove tail
            snake.pop()

        # -----------------------------
        # Draw everything
        # -----------------------------
        screen.fill(BLACK)

        # Draw walls
        for wall in walls:
            draw_cell(GRAY, wall)

        # Draw snake head
        draw_cell(DARK_GREEN, snake[0])

        # Draw snake body
        for part in snake[1:]:
            draw_cell(GREEN, part)

        # Draw food
        draw_cell(RED, food)

        # Draw score and level
        draw_text(f"Score: {score}", font, WHITE, 10, 10)
        draw_text(f"Level: {level}", font, WHITE, 500, 10)
        draw_text(f"Speed: {speed}", font, BLUE, 250, 10)

        # Update screen
        pygame.display.update()

        # Control game speed
        clock.tick(speed)

# -----------------------------
# Run the game
# -----------------------------
main()