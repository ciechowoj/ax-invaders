import pygame
import pickle
from pygame.locals import *
from miscellanea import multilineText

TABLE_WIDTH = 0.7

class HighScores:
    def __init__(self, font):
        self.font = font
        file = None
        try:
            file = open("data/player.dat", "rb")
        except IOError:
            file = None
        if file != None:
            self.score_list = pickle.load(file)
        else:
            self.score_list = [("Unknown", 0)] * 10
        self.score_cache = None
        self.head = font.render("HALL OF FAME", False, (255, 255, 0))
        self.back = False

    def addScore(self, name, score):
        self.score_list.append((name, score))
        self.score_list.sort(key = lambda x: -x[1])
        if len(self.score_list) > 10:
            self.score_list = self.score_list[0:10]
        file = open("data/player.dat", "wb+")
        pickle.dump(self.score_list, file)
        self.score_cache = None
        
    def renderCache(self, width):
        names = [self.font.render(self.score_list[x][0], False, (255, 255, 0)) for x in range(len(self.score_list))]
        scores = [self.font.render(str(self.score_list[x][1]), False, (255, 255, 0)) for x in range(len(self.score_list))]
        height = names[0].get_size()[1]
        self.score_cache = pygame.Surface((width * TABLE_WIDTH, height * len(scores)))
        for i in range(len(scores)):
            self.score_cache.blit(names[i], (0, height * i))
            self.score_cache.blit(scores[i], (width * TABLE_WIDTH - scores[i].get_size()[0], height * i))

    def handle(self, event):
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            self._mainMenu.reset()
            self.back = True

    def update(self, delta, current):
        if self.back:
            self.back = False
            return self._mainMenu
        else:
            return self
    
    def render(self, surface):
        if self.score_cache == None:
            self.renderCache(surface.get_size()[0])
        cache_size = self.score_cache.get_size()
        head_size = self.head.get_size()
        surface_size = surface.get_size()
        surface.blit(self.head, ((surface_size[0] - head_size[0]) // 2, (surface_size[1] - head_size[1] - cache_size[1]) // 2))
        surface.blit(self.score_cache, ((surface_size[0] - cache_size[0]) // 2, (surface_size[1] - head_size[1] - cache_size[1]) // 2 + head_size[1]))

