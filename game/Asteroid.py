import pygame
import random
import math
from settings import *

class Asteroid:
    def __init__(self, screen, position, direction, size, speed, radius):
        self.screen = screen
        self.position = position
        self.direction = direction
        self.size = size
        self.radius = radius
        self.speed = speed
        self.oneMoreLife = 0
        self.generateRandomPolygon()

        proba = random.randint(0, 100)
        if proba < 5:
            self.oneMoreLife = 1
        
    def generateRandomPolygon(self):
        num_vertices = random.randint(5, 12)
        angle_increment = 360 / num_vertices

        self.vertices = []
        for i in range(num_vertices):
            angle = math.radians(i * angle_increment + random.uniform(-10, 10))
            radius = random.uniform(self.radius / 2, self.radius)
            x = self.position.x + radius * math.cos(angle)
            y = self.position.y + radius * math.sin(angle)
            self.vertices.append(pygame.math.Vector2(x, y))
        
    def update(self):
        self.position += self.direction * self.speed
        
        if self.position.x < 0:
            self.position.x = WIDTH
        elif self.position.x > WIDTH:
            self.position.x = 0
        
        if self.position.y < 0:
            self.position.y = HEIGHT
        elif self.position.y > HEIGHT:
            self.position.y = 0
        
        self.generateRandomPolygon()

    def breakApart(self):
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
        if self.oneMoreLife == 0:
            pygame.draw.polygon(self.screen, WHITE, [vertex.xy for vertex in self.vertices], 1)
        else:
            pygame.draw.polygon(self.screen, RED, [vertex.xy for vertex in self.vertices], 1)