# Asteroids
This project is a revisit of the **Asteroids** game from the 1980s.

## Installation
Check that you have a python IDLE.
The version used for the project is **python3.11**

Install Pygame if you haven't done so already
```bash
pip install pygame
```

## How to start the game
If you're using Visual Studio Code, simply run **main.py**

Otherwise, go directly to the Asteroids file in cmd and run :
```bash
python main.py
```

## Structure
The **main.py** file manages the main game loop and the game logic, which includes startup, gameover and restart.

The **settings.py** file contains all the game's constants

The **game** folder contains all the files representing one of the game's main classes:
- **Asteroid.py**, which contains the class *Asteroid*
- **Bullet.py**, which contains the class *Bullet*
- **SpaceShip.py**, which contains the class *SpaceShip*
- **Game.py**, which contains the class *Game*