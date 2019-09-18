import pygame
from pygame.locals import *
from miscellanea import multilineText

class GameOver:
    def __init__(self, font):
        self.font = font
        self.name = ""
        self.score = 0
        self.head = multilineText(font, "GAME OVER\nGIVE YOUR NAME:", False, (255, 255, 0))
        self.done = False

    def setScore(self, score):
        self.score = score

    def handle(self, event):
        if event.type == KEYDOWN:
            if event.key == K_BACKSPACE and len(self.name) != 0:
                self.name = self.name[0:-1]
            if ('a' <= event.unicode and event.unicode <= 'z') or ('A' <= event.unicode and event.unicode <= 'Z'):
                self.name += event.unicode
            if event.key == K_RETURN:
                self.done = True

    def update(self, delta, current):
        if self.done:
            if self.name != "":
                self._highScores.addScore(self.name, self.score)
                self.name = ""
            return self._highScores
        else:
            return self
    
    def render(self, surface):
        name = self.font.render(self.name, False, (255, 255, 0))
        name_size = name.get_size()
        head_size = self.head.get_size()
        surface_size = surface.get_size()
        surface.blit(self.head, ((surface_size[0] - head_size[0]) // 2, (surface_size[1] - head_size[1] - name_size[1]) // 2))
        surface.blit(name, ((surface_size[0] - name_size[0]) // 2, (surface_size[1] - head_size[1] - name_size[1]) // 2 + head_size[1]))


