import pygame
from settings import *

class Bullet:
    def __init__(self, screen, position, direction):
        """
        Initializes a bullet object.

        Args:
        - screen: Pygame screen surface
        - position: Initial position of the bullet as a pygame.math.Vector2
        - direction: Direction of the bullet movement as a pygame.math.Vector2
        """

        self.screen = screen
        self.position = position
        self.direction = direction

    def update(self):
        """
        Updates the position of the bullet based on its movement speed.
        """

        self.position += self.direction * BULLET_SPEED

    def draw(self):
        """
        Draws the bullet on the screen as a circle.
        """
        
        pygame.draw.circle(self.screen, WHITE, (int(self.position.x), int(self.position.y)), BULLET_RADIUS)