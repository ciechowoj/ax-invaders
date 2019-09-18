from miscellanea import loadMeshes
from miscellanea import drawStats
import pygame
from pygame.locals import *

# init pygame module
pygame.init()
pygame.font.init()
pygame.mixer.init()
if pygame.font.get_init() == False:
    input("Cannot initialize pygame.font module...")
if pygame.mixer.get_init() == False:
    input("Cannot initialize pygame.mixer module...")

from MainMenu import *
from Gameplay import *
from GameOver import *
from HighScores import *
from LevelScreen import *

# load game resources
big_font = pygame.font.Font("data/visitor.ttf", 64)
small_font = pygame.font.Font("data/visitor.ttf", 48)
mesh_list = loadMeshes("data/meshes.dsc", "data/sprites.png")

# create & init subsystems
screen = pygame.display.set_mode( (800, 600) )
mainMenu = MainMenu(big_font, (255, 0, 0), (0, 255, 0))
gameplay = Gameplay(mesh_list, big_font)
gameOver = GameOver(big_font)
highScores = HighScores(big_font)
levelScreen = LevelScreen(big_font)
mainMenu._gameplay = gameplay
mainMenu._highScores = highScores
gameplay._mainMenu = mainMenu
gameplay._gameOver = gameOver
gameOver._highScores = highScores
highScores._mainMenu = mainMenu
levelScreen._gameplay = gameplay
gameplay._levelScreen = levelScreen
mainMenu._levelScreen = levelScreen
quit = False

# game main loop
gameState = mainMenu
oldTime = pygame.time.get_ticks() * 0.001
newTime = pygame.time.get_ticks() * 0.001
deltaTime = 0
timeStep = 0.0333333
frame = 0
quads = 0
displayStats = True

while not quit:
    # compute time
    newTime = pygame.time.get_ticks() * 0.001
    deltaTime += newTime - oldTime
    frameTime = (newTime - oldTime) + 0.00001
    oldTime = newTime
    # handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            quit = True
        if event.type == KEYDOWN and event.key == K_F1:
            displayStats = not displayStats
        elif event.type == MOUSEMOTION:
            pass
        else:
            gameState.handle(event)
    # update state
    while deltaTime > timeStep:
        gameState = gameState.update(timeStep, newTime)
        if gameState == None:
            break
        deltaTime -= timeStep
    # render frame
    if gameState != None:
        screen.fill((0, 0, 0))
        if displayStats:
            drawStats(screen, frameTime, quads, small_font)
        quads = gameState.render(screen)
        pygame.display.update()
    else:
        quit = True
    frame += 1
