from Game.Utils.imports import *
from spritesheet import SpriteSheet
import pygame

###############################BULLET CLASS BEGIN########################################
class Bullet(pygame.sprite.Sprite):
    def __init__(self, player, screen):
        self.filename = "../Sprites/knight.png"
        self.ss = SpriteSheet(self.filename, screen)
        self.image = self.ss.image_at((541, 374, 11, 11), 0)
        self.surf = pygame.Surface((40, 40))
        self.surf = self.image
        self.rect = self.surf.get_rect()
        self.pos = (player.pos[0], player.pos[1] - 50)
        if player.direction == "left":
            self.vel = pygame.math.Vector2((-10, 0))
        else:
            self.vel = pygame.math.Vector2((10, 0))

    def fire(self):
        self.pos += self.vel


###############################BULLET CLASS END##########################################
