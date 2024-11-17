from Game.Utils.imports import *
import pygame
from mapmanager import get_tile_properties
from spritesheet import SpriteSheet
from pygame.locals import (
    K_w,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    MOUSEMOTION,
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
)

###############################Player Class BEGIN########################################
class Player(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.filename = "../Sprites/knight.png"
        self.player_ss = SpriteSheet(self.filename, screen)
        self.player_run_images = self.player_ss.load_strip((0, 0, 85, 100), 6, 0)
        self.player_jump_images = self.player_ss.load_strip((0, 160, 85, 100), 2, 0)
        self.player_shoot_images = self.player_ss.load_strip((-8, 327, 85, 100), 6, 0)
        self.surf = pygame.Surface((85, 100))
        self.surf = self.player_run_images[0]
        self.rect = self.surf.get_rect()
        self.pos = pygame.math.Vector2((0, 0))
        self.vel = pygame.math.Vector2((0, 0))
        self.acc = pygame.math.Vector2((0, 0))
        self.frame = 0
        self.counter = 0
        self.direction = "right"
        self.shooting = False
        self.player_old_y = 448
        self.shift = 0
        self.falling = False

        # jumping
        self.gravity = 1
        self.jumping = False
        self.jump_power = 5

    def move(self, tmxdata, world_offset):
        # get properties of tile we are standing on
        standing_on = get_tile_properties(
            tmxdata, self.pos[0], self.pos[1], world_offset
        )

        if self.vel == pygame.math.Vector2((0, 0)):  # if we're not moving reset to standing frame
            self.frame = 0

        self.counter += 1  # move the frame counter for controlling animation of sprites

        # reset speed to zero so we can assess current inputs
        self.acc.x = 0
        self.vel.x = 0

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT]:
            self.direction = "left"
            self.acc.x = -ACC  # move to the left
            if self.counter > 7:  # framerate control for animation
                self.frame += 1  # loop through animation frames on spritesheet
                self.counter = 0  # start counter over, each time it reaches 7 7/60th we loop to next frame
        if pressed_keys[K_RIGHT]:
            self.direction = "right"
            self.acc.x = ACC  # move to the right
            if self.counter > 7:  # framerate control for animation
                self.frame += 1  # loop through animation frames on spritesheet
                self.counter = 0  # start counter over, each time it reaches 7 7/60th we loop to next frame

        if self.frame > 5:  # when we reach the last fram ss[5] reset to ss[0]
            self.frame = 0

##################################ANIMATION############################################

        # Animation for running only
        if not self.jumping and not self.shooting and not self.falling:
            if self.direction == "left":
                self.surf = pygame.transform.flip(
                    self.player_run_images[self.frame], True, False
                )  # flip image around
            if self.direction == "right":
                self.surf = self.player_run_images[self.frame]
        # animation for jumping
        if self.jumping:
            if self.direction == "right":
                self.surf = self.player_jump_images[0]
            if self.direction == "left":
                self.surf = pygame.transform.flip(
                    self.player_jump_images[0], True, False
                )  # flip image around
            # animation for falling
            if self.falling:
                if self.direction == "right":
                    self.surf = self.player_jump_images[0]
                if self.direction == "left":
                    self.surf = pygame.transform.flip(
                        self.player_jump_images[0], True, False
                    )  # flip image around
        # animation for shooting
        if self.shooting:
            if self.direction == "right":
                self.surf = self.player_shoot_images[self.frame]
            if self.direction == "left":
                self.surf = pygame.transform.flip(
                    self.player_shoot_images[self.frame], True, False
                )
##################################END ANIMATION############################################

        # move the player
        self.acc.x += self.vel.x * FRIC  # Friction
        self.vel += self.acc  # increase velocity by acceleration value

        if self.vel.y == 0: #if we stopped moving down
            self.jumping = False #we're done jumping
            if self.falling == False: #if we still thikn we are falling
                self.falling = True #tell us we are no longer falling

        #self.pos += self.vel #+ 0.5 * self.acc  # adjust position

        #self.rect.midbottom = self.pos  # adjust rect to center on screen rec must match object position

        # Apply gravity to the player's velocity
        #self.vel[1] += self.gravity

        # Move the player down by the vertical velocity
        self.pos[1] += self.vel[1]
        # horizontal
        self.pos[0] += self.vel[0]
        #print(self.rect)
        self.rect.midbottom = (self.pos.x, self.pos.y)
        #self.rect = self.pos
    def check_ground_collision(self, colliders):
        #self.rect = self.surf.get_rect()
        #print(self.rect)
        for tile in colliders:
            #print(tile)
            if self.surf.get_rect().colliderect(tile):
                #print("Collision")
                self.vel[1] = 0
                self.rect.bottom = tile.top  # Move player to stand on top of the tile
                self.jumping = False
                self.falling = False
                break

    def update(self, tmxdata, world_offset, colliders):
        self.check_ground_collision(colliders)

        standing_on = get_tile_properties(
             tmxdata, self.pos[0], self.pos[1], world_offset
        )
        if standing_on["ground"] == 1 and not self.jumping:
            self.acc = pygame.math.Vector2((0, 0))  # if we're on the ground no acceleration downward
            self.vel[1] = 0
            #print(world_offset)
            # self.pos[1] = world_offset[1]
            self.falling = False

        if standing_on["ground"] == 0 and not self.jumping and not self.falling:
            self.acc = pygame.math.Vector2((0, 0.5))  # if we're not on the ground we're falling
            self.falling = True

        if standing_on["ground"] == 0 and self.falling: #falling
            self.acc = pygame.math.Vector2((0, 0.5))

    def jump(self, tmxdata, world_offset):
         standing_on = get_tile_properties(
             tmxdata, self.pos[0], self.pos[1], world_offset
         )

         if standing_on["ground"] == 1 and not self.jumping:
             self.jumping = True
             self.vel.y = -15

    def cancel_jump(self):
         if self.jumping:
             if self.vel.y < -3:
                 self.vel.y = -3

    def shoot(self):
        if not self.shooting:
            self.shooting = True

    def cancel_shooting(self):
        self.shooting = False


###############################Player Class END##########################################
