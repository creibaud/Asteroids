import pygame
import math
from settings import *
from game.Bullet import Bullet

class SpaceShip:
    def __init__(self, screen):
        """
        Initializes a spaceship object.

        Args:
        - screen: Pygame screen surface
        """

        self.screen = screen
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, 0)
        self.thrusting = False
        self.P = pygame.math.Vector2(self.x, self.y)
        self.alpha = math.radians(120)
        self.axe = pygame.math.Vector2(1, 0)
        self.A = self.P + SPACESHIP_LENGTH * self.axe
        self.B = self.P + SPACESHIP_WIDTH * self.axe.rotate(-math.degrees(self.alpha))
        self.C = self.P + SPACESHIP_WIDTH * self.axe.rotate(math.degrees(self.alpha))
        self.maxSpeed = MAX_SPEED
        self.bullets = []
        self.framesHitAnimation = 0

    def update(self):
        """
        Updates the spaceship's position, velocity, and bullets.
        """

        if self.thrusting:
            self.accelerate()
        else:
            self.decelerate()

        self.velocity += self.acceleration

        if self.velocity.length() != 0:
            self.velocity.scale_to_length(min(self.velocity.length(), self.maxSpeed))

        # Wrap around the screen if the spaceship goes off the edges
        if self.P.x < 0:
            self.P.x = WIDTH
        elif self.P.x > WIDTH:
            self.P.x = 0

        if self.P.y < 0:
            self.P.y = HEIGHT
        elif self.P.y > HEIGHT:
            self.P.y = 0

        self.P += self.velocity
        self.A = self.P + SPACESHIP_LENGTH * self.axe
        self.B = self.P + SPACESHIP_WIDTH * self.axe.rotate(-math.degrees(self.alpha))
        self.C = self.P + SPACESHIP_WIDTH * self.axe.rotate(math.degrees(self.alpha))

        # Update bullets and remove those that are off-screen
        for bullet in self.bullets:
            bullet.update()

        self.bullets = [bullet for bullet in self.bullets if bullet.position.x <= WIDTH and bullet.position.x >= 0 and bullet.position.y <= HEIGHT and bullet.position.y >= 0]

    def accelerate(self):
        """
        Accelerates the spaceship in the direction it is facing.
        """

        thrustVector= self.axe * THRUST_POWER
        self.acceleration += thrustVector

    def decelerate(self):
        """
        Decelerates the spaceship to simulate friction.
        """

        self.acceleration *= SPACESHIP_DECELERATION

    def shoot(self):
        """
        Creates a new bullet and adds it to the list of bullets.
        """

        direction = self.axe.copy()
        newBullet = Bullet(self.screen, self.A, direction)
        self.bullets.append(newBullet)

    def rotate(self, angle):
        """
        Rotates the spaceship by a given angle.

        Args:
        - angle: Angle in radians
        """

        self.axe.rotate_ip(math.degrees(angle))

    def hitAnimation(self):
        """
        Displays a hit animation for the spaceship.
        """

        if self.framesHitAnimation < 15:
            self.draw(BLACK)
        else:
            self.draw(WHITE)

        self.framesHitAnimation += 1
        if self.framesHitAnimation > 30:
            self.framesHitAnimation = 0

    def draw(self, color):
        """
        Draws the spaceship on the screen.

        Args:
        - color: Color of the spaceship
        """

        pygame.draw.polygon(self.screen, color, [self.P, self.B, self.A, self.C], 1)
        for bullet in self.bullets:
            bullet.draw()