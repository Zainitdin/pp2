import pygame
import sys
from ball import Ball

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball")

clock = pygame.time.Clock()

ball = Ball(300, 300, 25, 20, (WIDTH, HEIGHT))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pressed = pygame.key.get_pressed()

    keys = {
        "left": pressed[pygame.K_LEFT],
        "right": pressed[pygame.K_RIGHT],
        "up": pressed[pygame.K_UP],
        "down": pressed[pygame.K_DOWN]
    }

    ball.move(keys)

    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (255, 0, 0), (ball.x, ball.y), ball.radius)

    pygame.display.flip()
    clock.tick(60)