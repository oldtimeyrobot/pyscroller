import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from uielement import *
import pygame
from player import *
from mapmanager import *
from bullet import *

################################Main BEGIN#################################################
def main():
    # initialize pygame
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

    # collider tracking
    colliders = []

    # world vars
    world_built = False
    world_offset = [0, 0]
    y_ground = screen.get_height() - 170

    # Background
    bg_texture = pygame.image.load(
        "../Sprites/oak_woods_v1.0/oak_woods_v1.0/background/background_layer_2.png"
    )
    bg_texture = pygame.transform.scale(bg_texture, (960, 640))

    ###############################Instantiate Objects BEGIN###################################
    player = Player(screen)
    ################################Instantiate Objects END####################################

    ################################Sprite Groups Begin########################################
    sprites = pygame.sprite.Group()
    sprites.add(player)  # add player sprite
    ################################Sprite Groups END##########################################

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

            # build map, check if it's built, if not then we load the map
            if world_built == False:
                tmxdata = load_pygame("../Maps/test.tmx")
                colliders = build_colliders(tmxdata)
                world_built = True

            # DEBUG
            playerpos = UIElement(
                center_position=(400, 10),
                font_size=30,
                bg_rgb=BLUE,
                text_rgb=WHITE,
                text=str(player.pos.y),
            )
            worldoffset = UIElement(
                center_position=(400, 40),
                font_size=30,
                bg_rgb=BLUE,
                text_rgb=WHITE,
                text=str(world_offset),
            )

            standing_on = get_tile_properties(
                tmxdata, player.pos[0], player.pos[1], world_offset
            )
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
            # keys_pressed = pygame.key.get_pressed() #dictionary of keys that are pressed

            for event in pygame.event.get():
                # escape key to exit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # quit
                        running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  # jump
                        player.jump(tmxdata, world_offset)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:  # cancel jump
                        player.cancel_jump()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:  # shoot
                        player.shoot()
                        bullets.append(Bullet(player, screen))
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:  # cancel shoot
                        player.cancel_shooting()

            # draw------------------->
            # clear screen
            screen.fill((0, 0, 0))
            screen.blit(bg_texture, (0, 0))
            # DEBUG
            # playerpos.draw(screen)
            # worldoffset.draw(screen)
            # standingon.draw(screen)
            # fallingtxt.draw(screen)
            # jumpingtxt.draw(screen)
            # DEBUG
            # draw map from tiled
            blit_all_tiles(screen, tmxdata, world_offset)

            # update and draw
            player.update(tmxdata, world_offset, colliders)
            player.move(tmxdata, world_offset)

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
                #entity.move(tmxdata, world_offset)

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
