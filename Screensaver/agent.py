from pygame.math import Vector2
from pygame.draw import circle, line, rect

class Agent:
    def __init__(self, position, radius, color):
        self.circle_color = color
        self.radius = radius
        self.position = position
        self.vel = Vector2(0,0)
        self.acc = Vector2(0,0)

    def update(self, delta_time_ms):
        self.vel = self.vel + self.acc
        self.position = self.position + self.vel
        self.acc = Vector2(0,0)

    def draw(self, screen):
        circle(screen, self.circle_color, 
               self.position, self.radius)