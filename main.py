###############################Init and Setup BEGIN########################################
# Import and Intialize the pygame library
import pygame
from pygame.sprite import Sprite
from pygame.rect import Rect
import pygame.freetype  # for UI Sprites

from pytmx.util_pygame import load_pygame

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

# Import the random library for RNG
import random

pygame.init()
v = pygame.math.Vector2

# Define constants for pygame window
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 640

# create screen object # set up window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

running = True
output = 0

# Define Constants for Game State
TITLE_SCREEN = 1
MAIN_SCREEN = 2
GAMEOVER_SCREEN = 3

# Mouse Left Button
LEFT = 1

#Constants for movement
ACC = 0.5
FRIC = -0.12
#Vector Shortcut
v = pygame.math.Vector2

# UI
BLUE = (106, 159, 181)
WHITE = (255, 255, 255)

#Background
bg_texture = pygame.image.load('Sprites/oak_woods_v1.0/oak_woods_v1.0/background/background_layer_2.png')
bg_texture = pygame.transform.scale(bg_texture, (960,640))

def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    """ Returns surface with text written on """
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()
# END UI
###############################Init and Setup END########################################
#TILED FUNCTIONS#########################################################################
def blit_all_tiles(screen, tmxdata, world_offset):
    for layer in tmxdata:
        for tile in layer.tiles():
            #tile[0] -> x grid location
            #tile[1] -> y grid location
            #tile[2] -> image data for blitting
            #img = pygame.transform.scale(tile[2], (40,40))
            x_pixel = tile[0] * 32 + world_offset[0]
            y_pixel = tile[1] * 32 + world_offset[1]
            screen.blit(tile[2],(x_pixel, y_pixel))
def get_tile_properties(tmxdata, x, y, world_offset):
    #print("XX::: " + str(x))
    world_x = x - world_offset[0]
    world_y = y - world_offset[1]
    tile_x = world_x // 32
    tile_y = world_y // 32
    try:
        properties = tmxdata.get_tile_properties(tile_x,tile_y,0)
        #print("X:: " + str(tile_x) + " Y:: " + str(tile_y))
        #print("WX:: " + str(world_x) + " WY:: " + str(world_y))
        #print(properties)
    except ValueError:
        properties = {"ground": 0, "solid": 0}
    if properties is None:
        properties = {"ground": 0, "solid": 0}
    return properties
###############################Tiled Functions End#######################################
###############################CLASS DEFS BEGIN##########################################
###############################Player Class BEGIN########################################
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.filename = 'Sprites/knight.png'
        self.player_ss = SpriteSheet(self.filename)
        self.player_run_images = self.player_ss.load_strip((0,0,85,100),6,0)
        self.player_jump_images = self.player_ss.load_strip((0,160,85,100),2,0)
        self.player_shoot_images = self.player_ss.load_strip((-8, 327, 85, 100), 6,0)
        self.surf = pygame.Surface((85,100))
        self.surf = self.player_run_images[0]
        self.rect = self.surf.get_rect()
        self.pos = v((0,0))
        self.vel = v((0,0))
        self.acc = v((0,0))
        self.jumping = False
        self.frame = 0
        self.counter = 0
        self.direction = 'right'
        self.shooting = False
        self.player_old_y = 448
        self.shift = 0
        self.falling = False

    def move(self, tmxdata, world_offset):
        #get properties of tile we are standing on
        standing_on = get_tile_properties(tmxdata, self.pos[0], self.pos[1], world_offset)

        if self.vel == v((0,0)): #if we're still reset to standing frame
            self.frame = 0

        self.counter += 1 #move the frame counter for controlling animation of sprites

        #reset speed to zero so we can assess current inputs
        self.acc.x = 0
        self.vel.x = 0

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT]:
            self.direction = 'left'
            self.acc.x = -ACC #move to the left
            if self.counter > 7: #framerate control for animation
                self.frame += 1 #loop through animation frames on spritesheet
                self.counter = 0 #start counter over, each time it reaches 7 7/60th we loop to next frame
        if pressed_keys[K_RIGHT]:
            self.direction = 'right'
            self.acc.x = ACC #move to the right
            if self.counter > 7: #framerate control for animation
                self.frame += 1 #loop through animation frames on spritesheet
                self.counter = 0 #start counter over, each time it reaches 7 7/60th we loop to next frame

        if self.frame > 5: #when we reach the last fram ss[5] reset to ss[0]
            self.frame = 0

        # Animation for running only
        if not self.jumping and not self.shooting:
            if self.direction == 'left':
                self.surf = pygame.transform.flip(self.player_run_images[3], True, False)
            else:
                self.surf = self.player_run_images[3]
        # flip image if we go left, since the ss is right facing
        if pressed_keys[K_LEFT]:
            self.surf = pygame.transform.flip(self.player_run_images[self.frame], True, False)
            # draw normail image since ss is right facing
        if pressed_keys[K_RIGHT]:
            self.surf = self.player_run_images[self.frame]
        #animation for jumping
        if self.jumping:
            if self.direction == 'right':
                self.surf = self.player_jump_images[0]
            if self.direction == 'left':
                self.surf = pygame.transform.flip(self.player_jump_images[0], True, False)
        # animation for falling
            if self.falling:
                if self.direction == 'right':
                    self.surf = self.player_jump_images[0]
                if self.direction == 'left':
                    self.surf = pygame.transform.flip(self.player_jump_images[0], True, False)
        #animation for shooting
        if self.shooting:
            if self.direction == 'right':
                self.surf = self.player_shoot_images[self.frame]
            if self.direction == 'left':
                self.surf = pygame.transform.flip(self.player_shoot_images[self.frame], True, False)

        #move the player
        self.acc.x += self.vel.x * FRIC #Friction
        self.vel += self.acc #increase velocity by acceleration value

        if self.vel.y == 0:
            self.jumping = False
            if self.falling == False:
                self.falling = True
        self.pos += self.vel + 0.5 * self.acc #adjust position

        self.rect.midbottom = self.pos #adjust rect? for what

    def update(self, tmxdata, world_offset):
        standing_on = get_tile_properties(tmxdata, self.pos[0], self.pos[1], world_offset)
        if standing_on['ground'] == 1 and not self.jumping:
            self.acc = v((0, 0))  # if we're on the ground no acceleration downward
            self.vel[1] = 0
            self.falling = False

        if standing_on['ground'] == 0 and not self.jumping and not self.falling:
            self.acc = v((0, 0.5))  # if we're not on the ground we're falling
            self.falling = True

        if standing_on['ground'] == 0 and self.falling:
            self.acc = v((0, 0.5))

    def jump(self, tmxdata, world_offset):
        standing_on = get_tile_properties(tmxdata, self.pos[0], self.pos[1], world_offset)
        if standing_on['ground'] == 1 and not self.jumping:
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
###############################BULLET CLASS BEGIN########################################
class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        self.filename = 'Sprites/knight.png'
        self.ss = SpriteSheet(self.filename)
        self.image = self.ss.image_at((541, 374, 11, 11),0)
        self.surf = pygame.Surface((40,40))
        self.surf = self.image
        self.rect = self.surf.get_rect()
        self.pos = (player.pos[0], player.pos[1]-50)
        if player.direction == 'left':
            self.vel = v((-10, 0))
        else:
            self.vel = v((10, 0))

    def fire(self):
        self.pos += self.vel
###############################BULLET CLASS END##########################################
###############################SpriteSheet Class Begin###################################
class SpriteSheet:
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename)
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {filename}")

    def image_at(self, rectangle, colorkey = None):
        """Load a specific image from a specific rectangle."""
        # Loads image from x, y, x+offset, y+offset.
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def images_at(self, rects, colorkey = None):
        """Load a whole bunch of images and return them as a list."""
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_strip(self, rect, image_count, colorkey = None):
        """Load a whole strip of images, and return them as a list."""
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)
###############################SpriteSheet Class End#####################################
################################Class Def BEGIN##########################################
class UIElement():
    """ An user interface element that can be added to a surface """

    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb):
        self.mouse_over = False  # indicates if the mouse is over the element

        # create the default image
        default_image = create_surface_with_text(
            text=text, font_size=font_size, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        # create the image that shows when mouse is over the element
        highlighted_image = create_surface_with_text(
            text=text, font_size=font_size * 1.2, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        # add both images and their rects to lists
        self.images = [default_image, highlighted_image]
        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position),
        ]

    # properties that vary the image and its rect when the mouse is over the element
    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up):
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return 1
        else:
            self.mouse_over = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)

        # calls the init method of the parent sprite class
        super().__init__()
###############################CLASS DEFS END############################################
###############################Instantiate Objects BEGIN#################################
player = Player()
################################Instantiate Objects END####################################
################################Sprite Groups Begin########################################
sprites = pygame.sprite.Group()
sprites.add(player)
################################Sprite Groups END##########################################
################################Main BEGIN#################################################
def main():
    # inititialize pygame
    pygame.init()
    pygame.freetype.init()

    # State init
    GAMESTATE = TITLE_SCREEN

    # create a clock for frame rate
    clock = pygame.time.Clock()

    # create screen object, set up window
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    # Run until user quits
    running = True

    # bullet tracking
    bullets = []

    #world vars
    world_built = False
    world_offset = [0, 0]
    y_ground = screen.get_height()-170

    ################################Main Loop BEGIN##########################################
    while running == True:
        ###############################TitleScreen BEGIN#########################################
        if GAMESTATE == TITLE_SCREEN:
            # create a quit button
            quit_btn = UIElement(
                center_position=(400, 400),
                font_size=30,
                bg_rgb=BLUE,
                text_rgb=WHITE,
                text="Quit",
            )

            # create a play button
            play_btn = UIElement(
                center_position=(400, 300),
                font_size=30,
                bg_rgb=BLUE,
                text_rgb=WHITE,
                text="Play",
            )

            mouse_up = False
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_up = True
            screen.fill(BLUE)

            # quit button handling
            ui_action1 = quit_btn.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action1 == 1:
                # quit
                pygame.quit()

            # play button handling
            ui_action2 = play_btn.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action2 == 1:
                GAMESTATE = MAIN_SCREEN

            # draw UI elements
            quit_btn.draw(screen)
            play_btn.draw(screen)
            pygame.display.flip()
        ###############################TitleScreen END###########################################
        ##############################Main Screen BEGIN##########################################
        if GAMESTATE == MAIN_SCREEN:

            #build map, check if it's built, if not then we load the map
            if world_built == False:
                tmxdata = load_pygame("Maps/test.tmx")
                world_built = True

            # DEBUG
            playerpos = UIElement(
                center_position=(400, 10),
                font_size=30,
                bg_rgb=BLUE,
                text_rgb=WHITE,
                text=str(player.pos),
            )
            worldoffset = UIElement(
                center_position=(400, 40),
                font_size=30,
                bg_rgb=BLUE,
                text_rgb=WHITE,
                text=str(world_offset),
            )

            standing_on = get_tile_properties(tmxdata, player.pos[0], player.pos[1], world_offset)
            standingon = UIElement(
                center_position=(400, 70),
                font_size=25,
                bg_rgb=BLUE,
                text_rgb=WHITE,
                text=str(standing_on),
            )
            fallingtxt = UIElement(
                center_position=(400, 90),
                font_size=25,
                bg_rgb=BLUE,
                text_rgb=WHITE,
                text=str(player.falling),
            )
            jumpingtxt = UIElement(
                center_position=(400, 110),
                font_size=25,
                bg_rgb=BLUE,
                text_rgb=WHITE,
                text=str(player.jumping),
            )

            # DEBUG

            for event in pygame.event.get():
                # escape key to exit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: #quit
                        running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE: #jump
                        player.jump(tmxdata, world_offset)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE: #cancel jump
                        player.cancel_jump()
                if event.type == pygame.KEYDOWN:
                     if event.key == pygame.K_w:    #shoot
                        player.shoot()
                        bullets.append(Bullet())
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w: #cancel shoot
                        player.cancel_shooting()


            # draw------------------->
            # clear screen
            screen.fill((0, 0, 0))
            screen.blit(bg_texture, (0,0))
            playerpos.draw(screen)
            worldoffset.draw(screen)
            standingon.draw(screen)
            fallingtxt.draw(screen)
            jumpingtxt.draw(screen)
            #draw map from tiled
            blit_all_tiles(screen, tmxdata, world_offset)

            #update and draw
            player.update(tmxdata, world_offset)

            # bounding space for screen scrolling
            if player.pos[0] < SCREEN_WIDTH / 2:
                player.pos[0] = SCREEN_WIDTH / 2
                world_offset[0] += 10
            if player.pos[0] > SCREEN_WIDTH / 2:
                player.pos[0] = SCREEN_WIDTH / 2
                world_offset[0] -= 10
            if player.pos[1] < 200:
                player.pos[1] = 200
                world_offset[1] += 10
            if player.pos[1] > y_ground:
                player.pos[1] = y_ground
                world_offset[1] -= 10

            for entity in sprites:
                screen.blit(entity.surf, entity.rect)
                entity.move(tmxdata, world_offset)

            for b in bullets:
                if b.pos[0] > SCREEN_WIDTH or b.pos[0] < 0:
                    bullets.remove(b)
                b.fire()
                screen.blit(b.surf, b.pos)

            # flip the display
            pygame.display.flip()

            # clock------------------->

            # maintain 60FPS
            clock.tick(60)
        ###############################Main Screen END###########################################
        ###############################Game Over Screen BEGIN####################################
        if GAMESTATE == GAMEOVER_SCREEN:
            # update
            for event in pygame.event.get():
                # escape key to exit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
        ###############################Game Over Screen END######################################
    ###############################Main Loop END#############################################
################################Main END#################################################
# quit
pygame.quit()

# call main when the script is run
if __name__ == "__main__":
    main()



