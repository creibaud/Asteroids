import pygame;
import math;
from settings import *
from game.Game import Game

# Initialize Pygame
pygame.init()

# Set up game window
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids")

# Create Game object
game = Game(screen)

# Initialize variables
angle = math.radians(0)
isAcceleration = False
shoot = False
lastShootTime = pygame.time.get_ticks()
asteroidTime = pygame.time.get_ticks()
asteroidAnimation = pygame.time.get_ticks()
canBeHitTime = pygame.time.get_ticks()
CAN_RESTART = False
GAME_OVER = False
START_GAME = False

# Main game loop
run = True
while run:
    # Event handling loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            # Rotate spaceship left
            if event.key == pygame.K_q and START_GAME:
                angle = math.radians(-SPACESHIP_ROTATION_SPEED)
            # Rotate spaceship right
            if event.key == pygame.K_d and START_GAME:
                angle = math.radians(SPACESHIP_ROTATION_SPEED)
            # Accelerate spaceship
            if event.key == pygame.K_z and START_GAME:
                isAcceleration = True
            # Restart the game
            if event.key == pygame.K_r and CAN_RESTART:
                game.restartGame()

                # Reset variables
                angle = math.radians(0)
                isAcceleration = False
                shoot = False
                lastShootTime = pygame.time.get_ticks()
                asteroidTime = pygame.time.get_ticks()
                asteroidAnimation = pygame.time.get_ticks()
                canBeHitTime = pygame.time.get_ticks()
                CAN_RESTART = False
                GAME_OVER = False

            # Start the game
            if event.key == pygame.K_SPACE and not START_GAME:
                START_GAME = True
                game.introduction = True

        if event.type == pygame.KEYUP:
            # Stop spaceship rotation and acceleration
            if event.key == pygame.K_q or event.key == pygame.K_d:
                angle = math.radians(0)
            if event.key == pygame.K_z:
                isAcceleration = False

        if event.type == pygame.MOUSEBUTTONDOWN and START_GAME:
            # Shoot when the left mouse button is pressed
            if event.button == 1:
                shoot = True
        
        if event.type == pygame.MOUSEBUTTONUP:
            # Stop shooting when the left mouse button is released
            if event.button == 1:
                shoot = False
    
    # Game logic and rendering
    screen.fill(BLACK)

    if START_GAME:
        # Update spaceship rotation and acceleration
        game.rotateSpaceShip(angle)
        game.spaceShipAccelerate(isAcceleration)

        # Shoot if the shooting condition is met
        if shoot and (pygame.time.get_ticks() - lastShootTime) > SHOOT_INTERVAL:
            lastShootTime = pygame.time.get_ticks()
            game.shootSpaceShip()

        # Create asteroids at regular intervals
        if pygame.time.get_ticks() - asteroidTime > game.asteroidInterval:
            asteroidTime = pygame.time.get_ticks()
            game.createRandomAsteroid()

        # Check for collision with asteroids
        if game.shipCollisionWithAsteroid() and game.canBeHit:
            game.life -= 1
            game.canBeHit = False
            canBeHitTime = pygame.time.get_ticks()
        
        # Set a cooldown period for the spaceship to be hit again
        if pygame.time.get_ticks() - canBeHitTime > CAN_BE_HIT_INTERVAL and not game.canBeHit:
            game.canBeHit = True

        # Check if the player has run out of lives
        if game.life <= 0:
            GAME_OVER = True

        # Update and draw game elements
        game.update()
        game.draw()
    else:
        # Display introductory text and prompt to start the game
        canBeHitTime = pygame.time.get_ticks()
        screen.fill(BLACK)

        # Draw asteroids for introduction
        if game.introduction:
            game.startIntroduction()

        game.update()
        game.draw()

        # Display game title and start prompt
        fontStartGame = pygame.font.Font(None, 50)
        fontTitle = pygame.font.Font(None, 100)
        startGameText = fontStartGame.render("Press Space to start", True, WHITE)
        titleText = fontTitle.render("Asteroids", True, WHITE)
        screen.blit(titleText, (WIDTH / 2 - titleText.get_width() / 2, 200))
        screen.blit(startGameText, (WIDTH / 2 - startGameText.get_width() / 2, HEIGHT / 2 - startGameText.get_height() / 2))

    # Display game over screen if the game is over
    if GAME_OVER:
        screen.fill(BLACK)
        fontGameOver = pygame.font.Font(None, 70)
        fontRestart = pygame.font.Font(None, 50)

        gameOverText = fontGameOver.render("Game Over", True, RED)
        restartText = fontRestart.render("Press R to restart", True, WHITE)

        screen.blit(gameOverText, (WIDTH / 2 - gameOverText.get_width() / 2, HEIGHT / 2 - gameOverText.get_height() / 2))
        screen.blit(restartText, (WIDTH / 2 - restartText.get_width() / 2, HEIGHT / 2 - restartText.get_height() / 2 - 150))

        CAN_RESTART = True

    # Update the display and control the frame rate
    pygame.display.update()
    clock.tick(FPS)

# Quit Pygame when the game loop exits
pygame.quit()