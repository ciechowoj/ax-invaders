from vector import look_at
from vector import perspective
from vector import identity4
from vector import translate4
from random import random
from SoundFX import *
from miscellanea import collide
import renderer
import pygame
from pygame.locals import *
from math import sqrt

HSPACING = 20
VSPACING = 10
HNUMBER = 11
NUM_BUNKER = 4
CYCLE_SIZE = 12
CYCLE_TIME = 0.1
PROJ = perspective(1.7 / 2, 1.25, 0.1, 1500)

PLAYER_YPOS = VSPACING * 14
BULLET_YPOS = PLAYER_YPOS + VSPACING
BUNKER_YPOS = VSPACING * 13
LIMIT_YPOS = VSPACING * 13
PLAYER_V = 30.0
BULLET_V = 60.0
BULLET_OFFSET = 5.0
THROUTPUT = 0.00005
ROOM_SIZE = 140
ALIEN_FACTOR = 10
PLAYER_LIVES = 4
CAMERA_HEIGHT = 100

aliens = HNUMBER * 5
canfire = True
score = 0
lives = PLAYER_LIVES

class SharedState:
    def __init__(self, meshes, objects):
        self.frame = 0
        self.time = 0.0
        self.phase = 0
        self.direction = 1
        self.side = False
        self.down = False
        self.bulletA = meshes["bulletA"][0][3]
        self.bulletB = meshes["bulletB"][0][3]
        self.laser = meshes["laser"][0][3]
        self.objects = objects

    def createBullet(self, x, y, type):
        if type == "bulletA":
            self.objects.append(Bullet(x, y, self.bulletA[0], self.bulletA[1], type))
        elif type == "bulletB":
            self.objects.append(Bullet(x, y, self.bulletB[0], self.bulletB[1], type))
        else:
            self.objects.append(Bullet(x, y, self.laser[0], self.laser[1], type))

class Explosion:
    def __init__(self, x, y):
        self.w = 0
        self.h = 0
        self.x = x
        self.y = y
        self.time = 0
        self.frame = 0
        self.dynamic = False
        self.type = "explosion"
        invaderkilled.play()

    def onUpdate(self, delta_time):
        self.time += delta_time
        if self.time > 0.3:
            self.frame += 1
            self.time = 0
        if self.frame == 2:
            return None
        else:
            return self
    
    def onCollision(self, obstacle):
        pass

class Wreck:
    def __init__(self, x, y):
        self.w = 0
        self.h = 0
        self.x = x
        self.y = y
        self.time = 0
        self.frame = 0
        self.dynamic = False
        self.type = "wreck"
        self.factor = 1

    def onUpdate(self, delta_time):
        global lives
        self.time += delta_time
        if self.time > 2:
            lives = -1
        return self
    
    def onCollision(self, obstacle):
        pass

class Alien:
    def __init__(self, x, y, w, h, type, master, state):
        self.w = w / 2.0
        self.h = h / 2.0
        self.x = x
        self.y = y - h
        self.type = type
        self.state = state
        self.master = master
        self.slave = None
        if master != None:
            master.slave = self
        self.factor = ALIEN_FACTOR
        self.dynamic = False
        self.destroy = False

    def onUpdate(self, delta_time):
        global score
        global aliens
        global lives
        if self.destroy:
            if self.type == "enemy10":
                score += 10
            elif self.type == "enemy20":
                score += 20
            elif self.type == "enemy30":
                score += 30
            aliens -= 1
            if self.slave != None:
                self.slave.master = self.master
            return Explosion(self.x, self.y)
        else:
            if self.state.side:
                self.x += self.state.direction * 4
            if self.state.down:
                self.y += VSPACING
                if self.y > LIMIT_YPOS and self.master == None:
                    lives = 0
            elif random() * delta_time < THROUTPUT and self.master == None:
                if self.type == "enemy30":
                    self.state.createBullet(self.x, self.y + self.h * 3, "bulletA")
                else:
                    self.state.createBullet(self.x, self.y + self.h * 3, "bulletB")
            return self

    def onCollision(self, obstacle):
        if obstacle == "laser":
            self.destroy = True

class Player:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w / 2.0
        self.h = h / 2.0
        self.type = "turret"
        self.vx = 0.0
        self.factor = 2
        self.dynamic = False

    def onUpdate(self, delta_time):
        self.x += self.vx * delta_time
        if self.x > ROOM_SIZE:
            self.x = ROOM_SIZE
        elif self.x < -ROOM_SIZE:
            self.x = -ROOM_SIZE
        if lives == 0:
            return Wreck(self.x, self.y)
        else:
            return self

    def onCollision(self, obstacle):
        global lives
        if obstacle[0:-2] == "enemy" or obstacle[0:-1] == "bullet":
            lives -= 1
            explosion.play()

class Bunker:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w / 2.0
        self.h = h / 2.0
        self.type = "bunker"
        self.damage = 4
        self.vx = 0.0
        self.dynamic = True
        
    def onUpdate(self, delta_time):
        if self.damage < 0:
            return None
        else:
            return self

    def onCollision(self, obstacle):
        self.damage -= 1
        explosion.play()

class Bullet:
    def __init__(self, x, y, w, h, type):
        self.x = x
        self.y = y
        self.w = w / 2.0
        self.h = h / 2.0
        self.type = type
        self.vy = BULLET_V
        if type == "laser":
            self.vy = -BULLET_V
        self.factor = 2
        self.destroy = False
        self.dynamic = True
        self.lost = False
        shoot.play()

    def onUpdate(self, delta_time):
        global canfire
        self.y += self.vy * delta_time
        if self.type == "laser" and self.y < VSPACING and not self.lost:
            canfire = True
            self.lost = True
        if self.y > BULLET_YPOS or self.y < - BULLET_YPOS:
            return None
        elif self.destroy:
            if self.type == "laser":
                canfire = True
            return None
        else:
            return self

    def onCollision(self, obstacle):
        self.destroy = True

class Gameplay:
    def __init__(self, meshes, font):
        global score
        global lives
        global canfire
        self._nextState = self
        self._objects = []
        self._meshes = meshes
        self._view = look_at((0, 100, 200), (0, 0, 80))
        self._level = 1
        self._font = font
        self._height = CAMERA_HEIGHT
        canfire = True
        self.reset(True)
        pass

    def handle(self, event):
        global canfire
        if self._height <= 0:
            keys = pygame.key.get_pressed()
            if keys[K_a] or keys[K_LEFT]:
                self._player.vx = -PLAYER_V
            elif keys[K_d] or keys[K_RIGHT]:
                self._player.vx = +PLAYER_V
            else:
                self._player.vx = 0
            if keys[K_SPACE] and canfire:
                self._state.createBullet(self._player.x, self._player.y - self._player.h - 2, "laser")
                canfire = False
            if keys[K_ESCAPE]:
                self._nextState = self._mainMenu
                self._mainMenu.reset()

    def update(self, delta, current):
        global lives
        if lives == -1:
            self._gameOver.setScore(score)
            return self._gameOver
        elif aliens == 0:
            self._level += 1
            lives += 1
            return self._levelScreen
        elif self._height > 0:
            self._height -= delta * 40
        else:
            for a in self._objects:
                if a.dynamic:
                    for b in self._objects:
                        if a != b and collide(a, b):
                            a.onCollision(b.type)
                            b.onCollision(a.type)
                            pass

            self._state.time += delta * sqrt(self._level)
            if self._state.time > CYCLE_TIME:
                self._state.phase += self._state.direction
                if self._state.phase % ALIEN_FACTOR == 0:
                    phase = self._state.phase // ALIEN_FACTOR
                    if phase == CYCLE_SIZE or phase == -CYCLE_SIZE:
                        self._state.direction *= -1
                        self._state.down = True
                    else:
                        self._state.side = True
                    fastinvader[phase % len(fastinvader)].play()
                self._state.frame += 1
                self._state.time -= CYCLE_TIME
            s = len(self._objects)
            i = 0
            while i < s:
                result = self._objects[i].onUpdate(delta)
                if result == None:
                    del self._objects[i]
                    i -= 1
                    s -= 1
                elif result != self._objects[i]:
                    self._objects[i] = result
                i += 1

            self._state.down = False
            self._state.side = False

        return self._nextState
    
    def render(self, surface):
        viewport = (0, 0) + surface.get_size()
        light = (1,  (75.0, 100.0, 50.0), (200, 200, 200))
        self._view = look_at((self._player.x, CAMERA_HEIGHT - self._height, 200), (self._player.x * 0.8, 0, 80))
        render_list = []
        for o in self._objects:
            mesh = self._meshes[o.type]
            if o.type == "explosion":
                render_list.append((mesh[o.frame], translate4(o.x, 0, o.y)))
            elif o.type != "bunker":
                render_list.append((mesh[self._state.frame // o.factor % len(mesh)], translate4(o.x, 0, o.y)))
            else:
                render_list.append((mesh[o.damage], translate4(o.x, 0, o.y)))
        quads = renderer.render(render_list, [light], (30, 30, 30), self._view, PROJ, viewport, surface, pygame.draw.polygon)
        self._drawHUD(surface)
        return quads
        
    def reset(self, all):
        global score
        global lives
        self._objects = []
        self._height = CAMERA_HEIGHT
        self._state = SharedState(self._meshes, self._objects)
        self._nextState = self
        self._initAliens()
        self._initPlayer()
        self._initBunkers()
        if all:
            score = 0
            lives = PLAYER_LIVES
            self._level = 1

    def _initAliens(self):
        global aliens
        aliens = HNUMBER * 5
        xoffset = - (HNUMBER - 1) * HSPACING / 2
        yoffset = 2 * VSPACING
        yoffset30 = yoffset
        yoffset20 = yoffset30 + VSPACING
        yoffset10 = yoffset20 + VSPACING * 2
        width30 = self._meshes["enemy30"][0][3][0]
        width20 = self._meshes["enemy20"][0][3][0]
        width10 = self._meshes["enemy10"][0][3][0]
        height = self._meshes["enemy10"][0][3][1]
        for x in range(HNUMBER):
            self._objects.append(Alien(x * HSPACING + xoffset, yoffset10 + VSPACING, width10, height, "enemy10", None, self._state))
        for x in range(HNUMBER):
            self._objects.append(Alien(x * HSPACING + xoffset, yoffset10, width10, height, "enemy10", self._objects[x], self._state))
        for x in range(HNUMBER):
            self._objects.append(Alien(x * HSPACING + xoffset, yoffset20 + VSPACING, width20, height, "enemy20", self._objects[HNUMBER + x], self._state))
        for x in range(HNUMBER):
            self._objects.append(Alien(x * HSPACING + xoffset, yoffset20, width20, height, "enemy20", self._objects[HNUMBER * 2 + x], self._state))
        for x in range(HNUMBER):
            self._objects.append(Alien(x * HSPACING + xoffset, yoffset30, width30, height, "enemy30", self._objects[HNUMBER * 3 + x], self._state))
        
    def _initPlayer(self):
        width = self._meshes["turret"][0][3][0]
        height = self._meshes["turret"][0][3][1]
        self._player = Player(0, PLAYER_YPOS, width, height)
        self._objects.append(self._player)

    def _initBunkers(self):
        width = self._meshes["bunker"][0][3][0]
        height = self._meshes["bunker"][0][3][1]
        spacing = HSPACING * 2
        for i in range(1, NUM_BUNKER + 1):
            self._objects.append(Bunker(-i * spacing + HSPACING - width, BUNKER_YPOS - height, width, height))
            self._objects.append(Bunker(-i * spacing + HSPACING, BUNKER_YPOS - height, width, height))
            self._objects.append(Bunker(-i * spacing + HSPACING + width, BUNKER_YPOS - height, width, height))
            self._objects.append(Bunker(-i * spacing + HSPACING - width, BUNKER_YPOS, width, height))
            self._objects.append(Bunker(-i * spacing + HSPACING, BUNKER_YPOS, width, height))
            self._objects.append(Bunker(-i * spacing + HSPACING + width, BUNKER_YPOS, width, height))
            self._objects.append(Bunker(i * spacing - HSPACING - width, BUNKER_YPOS - height, width, height))
            self._objects.append(Bunker(i * spacing - HSPACING, BUNKER_YPOS - height, width, height))
            self._objects.append(Bunker(i * spacing - HSPACING + width, BUNKER_YPOS - height, width, height))
            self._objects.append(Bunker(i * spacing - HSPACING - width, BUNKER_YPOS, width, height))
            self._objects.append(Bunker(i * spacing - HSPACING, BUNKER_YPOS, width, height))
            self._objects.append(Bunker(i * spacing - HSPACING + width, BUNKER_YPOS, width, height))

    def _drawHUD(self, surface):
        s = self._font.render("SCORE: " + str(score), False, (255, 255, 0))
        l = self._font.render("LIVES: " + str(max(0, lives)), False, (255, 255, 0))
        size = surface.get_size()
        surface.blit(s, (0, size[1] - s.get_size()[1]))
        surface.blit(l, (size[0] - l.get_size()[0], size[1] - l.get_size()[1]))
