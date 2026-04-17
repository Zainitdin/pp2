class Ball:
    def __init__(self, x, y, radius, speed, screen_size):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.width, self.height = screen_size

    def move(self, keys):
        if keys["left"] and self.x - self.speed - self.radius >= 0:
            self.x -= self.speed
        if keys["right"] and self.x + self.speed + self.radius <= self.width:
            self.x += self.speed
        if keys["up"] and self.y - self.speed - self.radius >= 0:
            self.y -= self.speed
        if keys["down"] and self.y + self.speed + self.radius <= self.height:
            self.y += self.speed