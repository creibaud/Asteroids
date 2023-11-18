import pygame;
import math;
from settings import *
from game.Game import Game

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids")

game = Game(screen)

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

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q and START_GAME:
                angle = math.radians(-SPACESHIP_ROTATION_SPEED)
            if event.key == pygame.K_d and START_GAME:
                angle = math.radians(SPACESHIP_ROTATION_SPEED)
            if event.key == pygame.K_z and START_GAME:
                isAcceleration = True
            if event.key == pygame.K_r and CAN_RESTART:
                game.restartGame()

                angle = math.radians(0)
                isAcceleration = False
                shoot = False

                lastShootTime = pygame.time.get_ticks()
                asteroidTime = pygame.time.get_ticks()
                asteroidAnimation = pygame.time.get_ticks()
                canBeHitTime = pygame.time.get_ticks()

                CAN_RESTART = False
                GAME_OVER = False

            if event.key == pygame.K_SPACE and not START_GAME:
                START_GAME = True
                game.introduction = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_q or event.key == pygame.K_d:
                angle = math.radians(0)
            if event.key == pygame.K_z:
                isAcceleration = False

        if event.type == pygame.MOUSEBUTTONDOWN and START_GAME:
            if event.button == 1:
                shoot = True
        
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                shoot = False
    
    screen.fill(BLACK)

    if START_GAME:
        game.rotateSpaceShip(angle)
        game.spaceShipAccelerate(isAcceleration)

        if shoot and (pygame.time.get_ticks() - lastShootTime) > SHOOT_INTERVAL:
            lastShootTime = pygame.time.get_ticks()
            game.shootSpaceShip()

        if pygame.time.get_ticks() - asteroidTime > game.asteroidInterval:
            asteroidTime = pygame.time.get_ticks()
            game.createRandomAsteroid()

        if game.shipCollisionWithAsteroid() and game.canBeHit:
                game.life -= 1
                game.canBeHit = False
                canBeHitTime = pygame.time.get_ticks()
        
        if pygame.time.get_ticks() - canBeHitTime > CAN_BE_HIT_INTERVAL and not game.canBeHit:
            game.canBeHit = True

        if game.life <= 0:
            GAME_OVER = True

        game.update()
        game.draw()
    else:
        canBeHitTime = pygame.time.get_ticks()
        screen.fill(BLACK)

        if game.introduction:
            game.startIntroduction()

        game.update()
        game.draw()
        fontStartGame = pygame.font.Font(None, 50)
        fontTitle = pygame.font.Font(None, 100)
        startGameText = fontStartGame.render("Press Space to start", True, WHITE)
        titleText = fontTitle.render("Asteroids", True, WHITE)
        screen.blit(titleText, (WIDTH / 2 - titleText.get_width() / 2, 200))
        screen.blit(startGameText, (WIDTH / 2 - startGameText.get_width() / 2, HEIGHT / 2 - startGameText.get_height() / 2))

    if GAME_OVER:
        screen.fill(BLACK)
        fontGameOver = pygame.font.Font(None, 70)
        fontRestart = pygame.font.Font(None, 50)

        gameOverText = fontGameOver.render("Game Over", True, RED)
        restartText = fontRestart.render("Press R to restart", True, WHITE)

        screen.blit(gameOverText, (WIDTH / 2 - gameOverText.get_width() / 2, HEIGHT / 2 - gameOverText.get_height() / 2))
        screen.blit(restartText, (WIDTH / 2 - restartText.get_width() / 2, HEIGHT / 2 - restartText.get_height() / 2 - 150))

        CAN_RESTART = True

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()