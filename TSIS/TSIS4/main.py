# 🔹 Entry point of the program
# Starts the Snake game

from game import SnakeGame

if __name__ == "__main__":
    # Create game object
    game = SnakeGame()

    # Start main loop
    game.run()