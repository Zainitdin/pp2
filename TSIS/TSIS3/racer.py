import pygame
import random
import time
from persistence import add_score


WIDTH = 400
HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ROAD = (45, 45, 45)
GREEN = (0, 180, 0)
RED = (220, 0, 0)
BLUE = (0, 100, 255)
YELLOW = (230, 230, 0)
ORANGE = (255, 150, 0)
PURPLE = (150, 0, 200)
GRAY = (120, 120, 120)

LANES = [70, 150, 230, 310]


class Player(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()

        # Load player car image
        self.image = pygame.image.load("/Users/zainitdinspv/work/TSIS/TSIS3/assets/Player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (45, 75))

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 90)

        self.speed = 6
        self.shield = False

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.left > 45:
            self.rect.x -= self.speed

        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH - 45:
            self.rect.x += self.speed

        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed

        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.left > 45:
            self.rect.x -= self.speed

        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH - 45:
            self.rect.x += self.speed

        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed

        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed


class TrafficCar(pygame.sprite.Sprite):
    def __init__(self, speed, player):
        super().__init__()

        self.image = pygame.image.load("/Users/zainitdinspv/work/TSIS/TSIS3/assets/Enemy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (45, 75))

        self.rect = self.image.get_rect()

        lane = random.choice(LANES)

        # Do not spawn directly above player
        while abs(lane - player.rect.centerx) < 50:
            lane = random.choice(LANES)

        self.rect.center = (lane, -80)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, speed, player):
        super().__init__()

        self.type = random.choice(["barrier", "oil", "pothole"])

        self.image = pygame.Surface((50, 35))

        if self.type == "barrier":
            self.image.fill(ORANGE)
        elif self.type == "oil":
            self.image.fill(BLACK)
        else:
            self.image.fill(GRAY)

        self.rect = self.image.get_rect()

        lane = random.choice(LANES)
        while abs(lane - player.rect.centerx) < 50:
            lane = random.choice(LANES)

        self.rect.center = (lane, -50)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()

        self.type = random.choice(["Nitro", "Shield", "Repair"])

        # Image paths
        image_map = {
            "Nitro": "/Users/zainitdinspv/work/TSIS/TSIS3/assets/nitro.png",
            "Shield": "/Users/zainitdinspv/work/TSIS/TSIS3/assets/shield.png",
            "Repair": "/Users/zainitdinspv/work/TSIS/TSIS3/assets/repair.png"
        }

        # Sizes
        size_map = {
            "Nitro": (40, 40),
            "Shield": (45, 45),
            "Repair": (35, 35)
        }

        base_image = pygame.image.load(image_map[self.type]).convert_alpha()
        self.image = pygame.transform.scale(base_image, size_map[self.type])

        self.rect = self.image.get_rect()
        self.rect.center = (random.choice(LANES), -40)

        self.speed = speed
        self.spawn_time = time.time()
        self.timeout = 6

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()

        if time.time() - self.spawn_time > self.timeout:
            self.kill()

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()

        if time.time() - self.spawn_time > self.timeout:
            self.kill()


class Coin(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()

        # Value (weight)
        self.value = random.choice([1, 2, 3])

        # Load image
        base_image = pygame.image.load("/Users/zainitdinspv/work/TSIS/TSIS3/assets/Coin.png").convert_alpha()

        # Dynamic size
        size_map = {
            1: 25,
            2: 35,
            3: 45
        }

        size = size_map[self.value]

        self.image = pygame.transform.scale(base_image, (size, size))

        self.rect = self.image.get_rect()
        self.rect.center = (random.choice(LANES), -30)

        self.speed = speed

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()


class RoadEvent(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()

        self.type = random.choice(["speed_bump", "nitro_strip", "moving_barrier"])

        self.image = pygame.Surface((90, 25))

        if self.type == "speed_bump":
            self.image.fill(ORANGE)
        elif self.type == "nitro_strip":
            self.image.fill(YELLOW)
        else:
            self.image.fill(GRAY)

        self.rect = self.image.get_rect()
        self.rect.center = (random.choice(LANES), -30)

        self.speed = speed
        self.direction = random.choice([-2, 2])

    def update(self):
        self.rect.y += self.speed

        if self.type == "moving_barrier":
            self.rect.x += self.direction

            if self.rect.left < 40 or self.rect.right > WIDTH - 40:
                self.direction *= -1

        if self.rect.top > HEIGHT:
            self.kill()


def run_game(screen, clock, username, settings):

    
    font = pygame.font.SysFont("Verdana", 18)

        # ---------- SOUND SETUP ----------
    pygame.mixer.init()

    if settings["sound"]:
        pygame.mixer.music.load("/Users/zainitdinspv/work/TSIS/TSIS3/assets/background.wav")
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)

    crash_sound = pygame.mixer.Sound("/Users/zainitdinspv/work/TSIS/TSIS3/assets/crash.wav")
    # --------------------------------

    def end_game():
        if settings["sound"]:
            crash_sound.play()
            pygame.time.delay(500)

        pygame.mixer.music.stop()
        add_score(username, score, distance)
        return "game_over", score, distance, coins

    player = Player(settings["car_color"])

    all_sprites = pygame.sprite.Group()
    traffic = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    coins_group = pygame.sprite.Group()
    road_events = pygame.sprite.Group()

    all_sprites.add(player)

    base_speed = {
        "Easy": 4,
        "Normal": 6,
        "Hard": 8
    }[settings["difficulty"]]

    traffic_speed = base_speed
    road_speed = base_speed

    score = 0
    coins = 0
    distance = 0
    finish_distance = 3000

    active_power = None
    power_start = 0
    power_duration = 0

    spawn_timer = 0
    running = True

    while running:
        screen.fill(GREEN)

        # Draw road
        pygame.draw.rect(screen, ROAD, (40, 0, 320, HEIGHT))

        # Lane lines
        for x in [120, 200, 280]:
            pygame.draw.line(screen, WHITE, (x, 0), (x, HEIGHT), 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", score, distance, coins

        # Distance and difficulty scaling
        distance += 1
        score = coins * 10 + distance

        if distance % 500 == 0:
            traffic_speed += 1
            road_speed += 1

        spawn_timer += 1

        # Dynamic spawning
        if spawn_timer % max(35, 90 - distance // 80) == 0:
            car = TrafficCar(traffic_speed, player)
            traffic.add(car)
            all_sprites.add(car)

        if spawn_timer % max(45, 120 - distance // 70) == 0:
            obstacle = Obstacle(road_speed, player)
            obstacles.add(obstacle)
            all_sprites.add(obstacle)

        if spawn_timer % 100 == 0:
            coin = Coin(road_speed)
            coins_group.add(coin)
            all_sprites.add(coin)

        if spawn_timer % 320 == 0:
            power = PowerUp(road_speed)
            powerups.add(power)
            all_sprites.add(power)

        if spawn_timer % 250 == 0:
            road_event = RoadEvent(road_speed)
            road_events.add(road_event)
            all_sprites.add(road_event)

        all_sprites.update()

        # Coin collision
        collected_coins = pygame.sprite.spritecollide(player, coins_group, True)

        for coin in collected_coins:
            coins += coin.value
            score += coin.value * 10

        # Power-up collision
        collected_powerups = pygame.sprite.spritecollide(player, powerups, True)

        for power in collected_powerups:
            # Only one active power-up at a time
            active_power = power.type
            power_start = time.time()

            if active_power == "Nitro":
                power_duration = 4
                player.speed = 10

            elif active_power == "Shield":
                player.shield = True
                power_duration = 999

            elif active_power == "Repair":
                power_duration = 0

                # Repair clears one obstacle instantly
                for obstacle in obstacles:
                    obstacle.kill()
                    score += 25
                    break

                active_power = None

        # Nitro timer
        if active_power == "Nitro":
            remaining = power_duration - (time.time() - power_start)

            if remaining <= 0:
                active_power = None
                player.speed = 6

        # Traffic collision
        if pygame.sprite.spritecollide(player, traffic, True):
            if player.shield:
                player.shield = False
                active_power = None
            else:
                return end_game()
        # Obstacle collision
        hit_obstacles = pygame.sprite.spritecollide(player, obstacles, True)

        for obstacle in hit_obstacles:
            if player.shield:
                player.shield = False
                active_power = None
            else:
                if obstacle.type == "oil":
                    player.speed = 3
                else:
                    return end_game()

        # Road event collision
        hit_events = pygame.sprite.spritecollide(player, road_events, True)

        for road_event in hit_events:
            if road_event.type == "speed_bump":
                player.speed = 3

            elif road_event.type == "nitro_strip":
                player.speed = 10
                active_power = "Nitro"
                power_start = time.time()
                power_duration = 3

            elif road_event.type == "moving_barrier":
                if player.shield:
                    player.shield = False
                    active_power = None
                else:
                    return end_game()

        # Restore normal speed if no nitro and not slowed
        if active_power != "Nitro" and player.speed < 6:
            if spawn_timer % 120 == 0:
                player.speed = 6

        all_sprites.draw(screen)

        # HUD
        score_text = font.render(f"Score: {score}", True, WHITE)
        coins_text = font.render(f"Coins: {coins}", True, WHITE)
        distance_text = font.render(
            f"Distance: {distance}m / {finish_distance}m",
            True,
            WHITE
        )

        screen.blit(score_text, (10, 10))
        screen.blit(coins_text, (10, 35))
        screen.blit(distance_text, (10, 60))

        if active_power:
            if active_power == "Shield":
                power_text = font.render("Power: Shield", True, WHITE)
            else:
                remaining = max(0, int(power_duration - (time.time() - power_start)))
                power_text = font.render(
                    f"Power: {active_power} {remaining}s",
                    True,
                    WHITE
                )

            screen.blit(power_text, (10, 85))

        if distance >= finish_distance:
            pygame.mixer.music.stop()
            add_score(username, score + 500, distance)
            return "game_over", score + 500, distance, coins
        
        pygame.display.update()
        clock.tick(60)