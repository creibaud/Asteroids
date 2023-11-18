import pygame
from settings import *

class Bullet:
    def __init__(self, screen, position, direction):
        self.screen = screen
        self.position = position
        self.direction = direction

    def update(self):
        self.position += self.direction * BULLET_SPEED

    def draw(self):
        pygame.draw.circle(self.screen, WHITE, (int(self.position.x), int(self.position.y)), BULLET_RADIUS)