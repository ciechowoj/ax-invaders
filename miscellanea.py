import pygame
from vector import *

def multilineText(font, text, antialias, color, background = None):
    L = [font.render(x, antialias, color) for x in text.split('\n')]
    width = max(L, key = lambda x: x.get_size()[0]).get_size()[0]
    height = max(L, key = lambda x: x.get_size()[1]).get_size()[1]
    result = pygame.Surface((width, height * len(L)))
    for i in range(len(L)):
        result.blit(L[i], ((width - L[i].get_size()[0]) // 2, i * height))
    return result

def loadMeshes(dsc, img):
    def spatialSprite(surface, transparent):
        def check(surface, position, transparent):
            if position.x < 0 or position.y < 0 or position.x >= surface.get_size()[0] or position.y >= surface.get_size()[1]:
                return transparent
            else:
                c = surface.get_at(position)
                return vec3(c[0], c[1], c[2])

        V = []
        C = []
        N = []
        count = 0
        size = vec2(surface.get_size()[0], surface.get_size()[1])
        offset = vec3(-size.x / 2, -size.y / 2, 0) - vec3(0.5, 0.5, 0.5)
        for y in range(size.y):
            for x in range(size.x):
                color = check(surface, vec2(x, y), transparent)
                if color != transparent:
                    t0 = vec3(x, 1, y) + offset
                    t1 = vec3(x, 1, y + 1) + offset
                    t2 = vec3(x + 1, 1, y + 1) + offset
                    t3 = vec3(x + 1, 1, y) + offset
                    b0 = vec3(x, 0, y) + offset
                    b1 = vec3(x, 0, y + 1) + offset
                    b2 = vec3(x + 1, 0, y + 1) + offset
                    b3 = vec3(x + 1, 0, y) + offset
                    V.append(t0); V.append(t1); V.append(t2); V.append(t3); C.append(color); N.append(vec3(0.0, +1.0, 0.0));
                    V.append(b2); V.append(b1); V.append(b0); V.append(b3); C.append(color); N.append(vec3(0.0, -1.0, 0.0));
                    if check(surface, vec2(x, y - 1), transparent) == transparent:
                        V.append(b0); V.append(t0); V.append(t3); V.append(b3); C.append(color); N.append(vec3(0.0, 0.0, -1.0))
                    if check(surface, vec2(x, y + 1), transparent) == transparent:
                        V.append(t2); V.append(t1); V.append(b1); V.append(b2); C.append(color); N.append(vec3(0.0, 0.0, +1.0))
                    if check(surface, vec2(x - 1, y), transparent) == transparent:
                        V.append(t0); V.append(b0); V.append(b1); V.append(t1); C.append(color); N.append(vec3(-1.0, 0.0, 0.0))
                    if check(surface, vec2(x + 1, y), transparent) == transparent:
                        V.append(b3); V.append(t3); V.append(t2); V.append(b2); C.append(color); N.append(vec3(+1.0, 0.0, 0.0))
        return (V, C, N, size)
    rects = []
    meshes = dict()
    sizes = dict()
    surface = pygame.image.load(img)
    for line in open(dsc, "r").readlines():
        split = line.split()
        if len(split) != 0:
            if split[0] == 'r':
                rects.append((int(split[1]), int(split[2]), int(split[3]), int(split[4])))
            elif split[0] == 's':
                M = []
                size = None
                for i in range(3, len(split)):
                    if split[i][0] == '#':
                        break
                    else:
                        M.append(spatialSprite(surface.subsurface(rects[int(split[i])]), vec3(255, 0, 255)))
                meshes[split[1]] = M
    return meshes

def drawStats(surface, spf, tri, font):
    FPS = font.render("MS: " + str(int(spf * 1000)) + " FPS: " + str(int(1.0 / spf)) + " QUADS: " + str(tri), False, (255, 0, 0))
    surface.blit(FPS, (0, 0))

def collide(a, b):
    x = abs(a.x - b.x) - (a.w + b.w)
    y = abs(a.y - b.y) - (a.h + b.h)
    return x < 0 and y < 0

