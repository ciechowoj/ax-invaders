import pygame
from pygame.locals import *
from miscellanea import multilineText

SHOW_TIME = 1.0

class LevelScreen:
    def __init__(self, font):
        self.time = 0
        self.font = font

    def reset(self):
        self.time = 0

    def handle(self, event):
        pass

    def update(self, delta, current):
        self.time += delta
        if self.time > SHOW_TIME:
            self.time = 0
            self._gameplay.reset(False)
            return self._gameplay
        else:
            return self

    def render(self, surface):
        label = self.font.render("ROUND " + str(self._gameplay._level), False, (255, 255, 0))
        dst_size = surface.get_size()
        src_size = label.get_size()
        surface.blit(label, ((dst_size[0] - src_size[0]) // 2, (dst_size[1] - src_size[1]) // 2))

