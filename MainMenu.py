import pygame
from pygame.locals import *
from miscellanea import multilineText

class MainMenu:
    def __init__(self, font, active, passive):
        self._highScores = None
        self._gameplay = None
        self._position = "new_game"
        self._nextState = self
        self._newGameActive = multilineText(font, "NEW\nGAME", False, active)
        self._hallOfFameActive = multilineText(font, "HALL\nOF FAME", False, active)
        self._exitTextActive = multilineText(font, "EXIT", False, active)
        self._newGamePassive = multilineText(font, "NEW\nGAME", False, passive)
        self._hallOfFamePassive = multilineText(font, "HALL\nOF FAME", False, passive)
        self._exitTextPassive = multilineText(font, "EXIT", False, passive)
       
    def reset(self):
        self._position = "new_game"
        self._nextState = self

    def handle(self, event):
        if event.type == KEYDOWN:
            if event.key == K_a or event.key == K_LEFT:
                self._position = "new_game"
            elif event.key == K_d or event.key == K_RIGHT:
                self._position = "high_scores"
            elif event.key == K_s or event.key == K_DOWN:
                self._position = "exit"
            elif event.key == K_ESCAPE:
                if self._position == "exit":
                    self._nextState = None
                else:
                    self._position = "exit"
            elif event.key == K_RETURN:
                if self._position == "new_game":
                    self._nextState = self._levelScreen
                    self._gameplay.reset(True)
                elif self._position == "high_scores":
                    self._nextState = self._highScores
                elif self._position == "exit":
                    self._nextState = None

    def update(self, delta, current):
        return self._nextState
    
    def render(self, surface):
        OFFSET = 128
        x = OFFSET - (self._newGameActive.get_size()[0] // 2)
        y = OFFSET - (self._newGameActive.get_size()[1] // 2)
        if self._position == "new_game": 
            surface.blit(self._newGameActive, (x, y))
        else:
            surface.blit(self._newGamePassive, (x, y))

        x = surface.get_size()[0] - OFFSET - (self._hallOfFameActive.get_size()[0] // 2)
        y = OFFSET - (self._hallOfFameActive.get_size()[1] // 2)
        if self._position == "high_scores": 
            surface.blit(self._hallOfFameActive, (x, y))
        else:
            surface.blit(self._hallOfFamePassive, (x, y))

        x = (surface.get_size()[0] - self._exitTextActive.get_size()[0]) // 2
        y = surface.get_size()[1] - OFFSET - (self._exitTextActive.get_size()[1] // 2)
        if self._position == "exit": 
            surface.blit(self._exitTextActive, (x, y))
        else:
            surface.blit(self._exitTextPassive, (x, y))
