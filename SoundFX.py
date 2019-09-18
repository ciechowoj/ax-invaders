import pygame

shoot = pygame.mixer.Sound("data/sfx/shoot.wav")
explosion = pygame.mixer.Sound("data/sfx/explosion.wav")
fastinvader = [pygame.mixer.Sound("data/sfx/fastinvader" + str(x) + ".wav") for x in range(1, 4)]
invaderkilled = pygame.mixer.Sound("data/sfx/invaderkilled.wav")




