import pygame
import random
import math
from settings import *
from game.Asteroid import Asteroid
from game.SpaceShip import SpaceShip

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.spaceShip = SpaceShip(self.screen)
        self.bullets = []
        self.asteroids = []
        self.life = 3
        self.score = 0
        self.level = 1
        self.scoreLimit = 1000
        self.asteroidInterval = 5000
        self.asteroidsCountInitial = 10
        self.canBeHit = False
        self.introduction = True

    def startIntroduction(self):
        for i in range(self.asteroidsCountInitial):
            self.createRandomAsteroid()
        self.introduction = False
    
    def restartGame(self):
        self.spaceShip = SpaceShip(self.screen)
        self.bullets = []
        self.asteroids = []
        self.life = 3
        self.score = 0
        self.level = 1
        self.scoreLimit = 1000
        self.asteroidInterval = 5000
        self.asteroidsCountInitial = 10
        self.canBeHit = False

        for i in range(self.asteroidsCountInitial):
            self.createRandomAsteroid()

    def createRandomAsteroid(self):
        side = random.choice(["top", "bottom", "left", "right"])
        position = pygame.math.Vector2(0, 0)
        radius = ASTEROID_RADIUS

        if side == "top":
            position = pygame.math.Vector2(random.randint(0, WIDTH), 0)
        elif side == "bottom":
            position = pygame.math.Vector2(random.randint(0, WIDTH), HEIGHT)
        elif side == "left":
            position = pygame.math.Vector2(0, random.randint(0, HEIGHT))
        elif side == "right":
            position = pygame.math.Vector2(WIDTH, random.randint(0, HEIGHT))

        direction = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))

        size = random.choice(ASTEROID_SIZE)
        if size == "small":
            radius = ASTEROID_RADIUS // 3
        elif size == "medium":
            radius = ASTEROID_RADIUS // 2
        else:
            radius = ASTEROID_RADIUS

        newAsteroid = Asteroid(self.screen, position, direction, size, random.uniform(1, ASTEROID_MAX_SPEED), radius)
        self.asteroids.append(newAsteroid)

    def bulletCollisionWithAsteroid(self):
        for bullet in self.bullets:
            for asteroid in self.asteroids:
                if bullet.position.distance_to(asteroid.position) < asteroid.radius + BULLET_RADIUS:
                    if asteroid.size != "small":
                        self.asteroids.extend(asteroid.breakApart())

                        if asteroid.size == "big":
                            self.score += 25
                        elif asteroid.size == "medium":
                            self.score += 50
                    else:
                        self.score += 100

                    if asteroid.oneMoreLife == 1:
                        self.life += 1

                    self.bullets.remove(bullet)
                    self.asteroids.remove(asteroid)
                    break

    def shipCollisionWithAsteroid(self):
        for asteroid in self.asteroids:
            self.shipPoints = [self.spaceShip.P, self.spaceShip.B, self.spaceShip.A, self.spaceShip.C]
            for shipPoint in self.shipPoints:
                if asteroid.position.distance_to(shipPoint) < asteroid.radius:
                    return True
        return False
        
    def update(self):
        if self.score >= self.scoreLimit:
            self.level += 1
            self.asteroidsCountInitial += 2
            self.scoreLimit += 1000
            self.asteroidInterval -= 500

            if self.asteroidInterval == 500:
                self.asteroidInterval = 500

            for i in range(self.asteroidsCountInitial):
                self.createRandomAsteroid()

        self.spaceShip.update()
        self.bullets = self.spaceShip.bullets

        for asteroid in self.asteroids:
            asteroid.update()

        self.bulletCollisionWithAsteroid()

    def rotateSpaceShip(self, angle):
        self.spaceShip.rotate(angle)

    def spaceShipAccelerate(self, isAcceleration):
        if isAcceleration:
            self.spaceShip.accelerate()
        else:
            self.spaceShip.decelerate()
    
    def shootSpaceShip(self):
        self.spaceShip.shoot()

    def displayScore(self):
        font = pygame.font.Font(None, 50)
        scoreText = font.render(str(self.score), True, WHITE)
        self.screen.blit(scoreText, (100, 100))

    def displayLevel(self):
        font = pygame.font.Font(None, 50)
        levelText = font.render("Level : " + str(self.level), True, WHITE)
        self.screen.blit(levelText, (WIDTH - 100 - levelText.get_width(), 100))

    def displayLife(self):
        alpha = math.radians(120)
        axe = pygame.math.Vector2(0, -1)

        for i in range(self.life):
            P = pygame.math.Vector2(109 + i * 30, 160)
            A = P + SPACESHIP_LENGTH * axe
            B = P + SPACESHIP_WIDTH * axe.rotate(-math.degrees(alpha))
            C = P + SPACESHIP_WIDTH * axe.rotate(math.degrees(alpha))
            pygame.draw.polygon(self.screen, RED, [P, B, A, C], 1)
    
    def draw(self):
        if not self.canBeHit:
            self.spaceShip.hitAnimation()
        else:
            self.spaceShip.draw(WHITE)
            self.spaceShip.framesHitAnimation = 0

        for asteroid in self.asteroids:
            asteroid.draw()

        self.displayScore()
        self.displayLife()
        self.displayLevel()
