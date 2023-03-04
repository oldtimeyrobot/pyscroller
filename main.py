###############################Init and Setup BEGIN########################################
# Import and Intialize the pygame library
import pygame
import pygame.freetype  # for UI Sprites

# import pygame locals
from pygame.sprite import Sprite
from pygame.rect import Rect

from pygame.locals import (
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

# UI
BLUE = (106, 159, 181)
WHITE = (255, 255, 255)

#Constants for movement
ACC = 0.5
FRIC = -0.12

def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    """ Returns surface with text written on """
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()
# END UI

#Texture Loading#
#playerTexture = pygame.image.load("Sprites\knight.png")
#End Texture Loading#
###############################Init and Setup END########################################

###############################Instantiate Objects BEGIN#################################
player = Player()
platform = Platform()
################################Instantiate Objects END####################################
################################Sprite Groups Begin########################################
sprites = pygame.sprite.Group()
sprites.add(player)
sprites.add(platform)

platforms = pygame.sprite.Group()
platforms.add(platform)
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



