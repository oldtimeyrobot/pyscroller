###############################Init and Setup BEGIN########################################
# Import and Intialize the pygame library
import pygame
from pygame.sprite import Sprite
from pygame.rect import Rect
import pygame.freetype  # for UI Sprites

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
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 632

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

#Texture Loading#
#playerTexture = pygame.image.load("Sprites\knight.png")
#End Texture Loading#
###############################Init and Setup END########################################
###############################CLASS DEFS BEGIN##########################################
###############################Platform Class Begin######################################
class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((SCREEN_WIDTH, 20))
        self.surf.fill((255,0,0))
        self.rect = self.surf.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT - 10))

    def move(self):
        pass
###############################Platform Class End########################################

###############################Platform Class Begin######################################
class Platform2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((500, 600))
        self.surf.fill((255,0,0))
        self.rect = self.surf.get_rect(center = (250, 300))

    def move(self):
        pass
###############################Platform Class End########################################

###############################Player Class BEGIN########################################
# for player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.filename = 'Sprites/knight.png'
        self.player_ss = SpriteSheet(self.filename)
        self.player_run_images = self.player_ss.load_strip((0,0,85,100),6)
        self.player_jump_images = self.player_ss.load_strip((0,160,85,100),2)
        self.player_shoot_images = self.player_ss.load_strip((-8, 327, 85, 100), 6)
        self.surf = pygame.Surface((85,100))
        self.surf = self.player_run_images[0]
        self.rect = self.surf.get_rect()
        self.pos = v((10,150))
        self.vel = v((0,0))
        self.acc = v((0,0))
        self.jumping = False
        self.frame = 0
        self.counter = 0
        self.direction = 'right'
        self.shooting = False

    def get_image(self):
        return self.player_image

    def move(self):
        self.acc = v((0,0.5))
        if self.vel == v((0,0)):
            self.frame = 0

        self.counter += 1

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.direction = 'left'
            self.acc.x = -ACC
            if self.counter > 7:
                self.frame += 1
                self.counter = 0
        if pressed_keys[K_RIGHT]:
            self.direction = 'right'
            self.acc.x = ACC
            if self.counter > 7:
                self.frame += 1
                self.counter = 0

        if self.frame > 5:
            self.frame = 0

        if pressed_keys[K_LEFT]:
            self.surf = pygame.transform.flip(self.player_run_images[self.frame],True, False)

        if pressed_keys[K_RIGHT]:
            self.surf = self.player_run_images[self.frame]

        if self.jumping == True:
            if self.direction == 'right':
                self.surf = self.player_jump_images[0]
            if self.direction == 'left':
                self.surf = pygame.transform.flip(self.player_jump_images[0], True, False)

        if self.shooting == True:
            if self.direction == 'right':
                self.surf = self.player_shoot_images[self.frame]
            if self.direction == 'left':
                self.surf = pygame.transform.flip(self.player_shoot_images[self.frame], True, False)


        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > SCREEN_WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = SCREEN_WIDTH

        self.rect.midbottom = self.pos

    def update(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if self.vel.y > 0:
            if hits:
                self.vel.y = 0
                self.pos.y = hits[0].rect.top + 1
                self.jumping = False

    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
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


###############################BULLET CLASS END##########################################
###############################SpriteSheet Class Begin###################################
class SpriteSheet:
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
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
# UI
BLUE = (106, 159, 181)
WHITE = (255, 255, 255)
def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    """ Returns surface with text written on """
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()
# END UI

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
platform = Platform()
#platform2 = Platform2()
################################Instantiate Objects END####################################
################################Sprite Groups Begin########################################
sprites = pygame.sprite.Group()
sprites.add(player)
sprites.add(platform)

platforms = pygame.sprite.Group()
platforms.add(platform)
#platforms.add(platform2)
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

            # update------------------->

            for event in pygame.event.get():
                # escape key to exit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player.jump()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        player.cancel_jump()
                if event.type == pygame.KEYDOWN:
                     if event.key == pygame.K_w:
                        player.shoot()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        player.cancel_shooting()


                        # draw------------------->

            # clear screen
            screen.fill((0, 0, 0))

            # draw all sprites
            #for entity in unit_sprites:
                #screen.blit(entity.surf, entity.rect)
            #collision

            player.update()

            for entity in sprites:
                screen.blit(entity.surf, entity.rect)
                entity.move()

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



