import pygame
import sys
from clock import get_time

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Clock")

clock = pygame.time.Clock()

# Load SAME image but we will treat them as left/right hands
hand_img = pygame.image.load("/Users/zainitdinspv/work/practice9/mickeyes_clocks/images/mickeyclock.jpeg")

center = (WIDTH // 2, HEIGHT // 2)

font = pygame.font.SysFont(None, 40)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((255, 255, 255))

    minutes, seconds = get_time()

    # ✅ Correct angles
    sec_angle = -seconds * 6
    min_angle = -minutes * 6

    # ✅ Rotate hands
    sec_hand = pygame.transform.rotate(hand_img, sec_angle)
    min_hand = pygame.transform.rotate(hand_img, min_angle)

    # ✅ Position LEFT (seconds) and RIGHT (minutes)
    sec_rect = sec_hand.get_rect(center=(center[0] - 20, center[1]))
    min_rect = min_hand.get_rect(center=(center[0] + 20, center[1]))

    # Draw hands
    screen.blit(sec_hand, sec_rect)   # LEFT = seconds
    screen.blit(min_hand, min_rect)   # RIGHT = minutes

    # ✅ Display digital time (helps teacher verify)
    time_text = font.render(f"{minutes:02}:{seconds:02}", True, (0, 0, 0))
    screen.blit(time_text, (250, 50))

    pygame.display.flip()

    # ✅ Update every second (IMPORTANT)
    pygame.time.delay(1000)