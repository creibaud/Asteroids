import pygame
import random
import math
from settings import *

class Asteroid:
    def __init__(self, screen, position, direction, size, speed, radius):
        """
        Initializes an asteroid object.

        Args:
        - screen: Pygame screen surface
        - position: Initial position of the asteroid as a pygame.math.Vector2
        - direction: Initial direction of the asteroid movement as a pygame.math.Vector2
        - size: Size of the asteroid ("big", "medium", "small")
        - speed: Speed of the asteroid movement
        - radius: Radius of the asteroid
        """
        
        self.screen = screen
        self.position = position
        self.direction = direction
        self.size = size
        self.radius = radius
        self.speed = speed
        self.oneMoreLife = 0 # Flag indicating if the asteroid can give a life for the space ship
        self.generateRandomPolygon() # Generate a random polygon shape for the asteroid

        # Randomly determine if the asteroid can give a life
        proba = random.randint(0, 100)
        if proba < 5:
            self.oneMoreLife = 1
        
    def generateRandomPolygon(self):
        """
        Generates a random polygon shape for the asteroid.
        """

        numVertices = random.randint(5, 12)
        angleIncrement = 360 / numVertices

        self.vertices = []
        for i in range(numVertices):
            angle = math.radians(i * angleIncrement + random.uniform(-10, 10))
            radius = random.uniform(self.radius / 2, self.radius)
            x = self.position.x + radius * math.cos(angle)
            y = self.position.y + radius * math.sin(angle)
            self.vertices.append(pygame.math.Vector2(x, y))
        
    def update(self):
        """
        Updates the position of the asteroid based on its movement.
        """

        self.position += self.direction * self.speed
        
        # Wrap around the screen if the asteroid goes off the edges
        if self.position.x < 0:
            self.position.x = WIDTH
        elif self.position.x > WIDTH:
            self.position.x = 0
        
        if self.position.y < 0:
            self.position.y = HEIGHT
        elif self.position.y > HEIGHT:
            self.position.y = 0
        
        # Regenerate a random polygon shape for the asteroid
        self.generateRandomPolygon()

    def breakApart(self):
        """
        Breaks apart the asteroid into smaller pieces when it's hit.

        Returns:
        - A list of smaller asteroid objects.
        """

        if self.size == "big":
            return [
                Asteroid(self.screen, self.position + pygame.math.Vector2(random.randint(0, 5), random.randint(0, 5)), pygame.Vector2(1, 0).rotate(random.uniform(0, 360)), "medium", self.speed, ASTEROID_RADIUS // 2),
                Asteroid(self.screen, self.position + pygame.math.Vector2(random.randint(0, 5), random.randint(0, 5)), pygame.Vector2(1, 0).rotate(random.uniform(0, 360)), "medium", self.speed, ASTEROID_RADIUS // 2)]
        elif self.size == "medium":
            return [
                Asteroid(self.screen, self.position + pygame.math.Vector2(random.randint(0, 5), random.randint(0, 5)), pygame.Vector2(1, 0).rotate(random.uniform(0, 360)), "small", self.speed, ASTEROID_RADIUS // 3),
                Asteroid(self.screen, self.position + pygame.math.Vector2(random.randint(0, 5), random.randint(0, 5)), pygame.Vector2(1, 0).rotate(random.uniform(0, 360)), "small", self.speed, ASTEROID_RADIUS // 3)
            ]
        else:
            return []

    def draw(self):
        """
        Draws the asteroid on the screen.
        """

        # Draw the asteroid with different colors based on whether it can give a life or not
        if self.oneMoreLife == 0:
            pygame.draw.polygon(self.screen, WHITE, [vertex.xy for vertex in self.vertices], 1)
        else:
            pygame.draw.polygon(self.screen, RED, [vertex.xy for vertex in self.vertices], 1)