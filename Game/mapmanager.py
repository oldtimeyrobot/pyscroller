from Game.Utils.imports import *
import pygame
# TILED FUNCTIONS#########################################################################
def blit_all_tiles(screen, tmxdata, world_offset):
    for layer in tmxdata:
        for tile in layer.tiles():
            # tile[0] -> x grid location
            # tile[1] -> y grid location
            # tile[2] -> image data for blitting
            # img = pygame.transform.scale(tile[2], (40,40))
            x_pixel = tile[0] * 32 + world_offset[0]
            y_pixel = tile[1] * 32 + world_offset[1]
            screen.blit(tile[2], (x_pixel, y_pixel))


def get_tile_properties(tmxdata, x, y, world_offset):
    # print("XX::: " + str(x))
    world_x = x - world_offset[0]
    world_y = y - world_offset[1]
    tile_x = world_x // 32
    tile_y = world_y // 32
    try:
        properties = tmxdata.get_tile_properties(tile_x, tile_y, 0)
        # print("X:: " + str(tile_x) + " Y:: " + str(tile_y))
        # print("WX:: " + str(world_x) + " WY:: " + str(world_y))

    except ValueError:
        properties = {"ground": 0, "solid": 0}
    if properties is None:
        properties = {"ground": 0, "solid": 0}
    #print(properties)
    return properties

def build_colliders(tmxdata):
    colliders = []

    for layer in tmxdata:
        for tile in layer.tiles():
            for x, y, gid in layer:
                tile = tmxdata.get_tile_image_by_gid(gid)
                if tile:
                    tile_props = tmxdata.get_tile_properties_by_gid(gid)
                    # Check if the tile has a 'solid' property
                   #print(tile_props)
                    if tile_props and tile_props.get("solid"):
                        # Create a rectangle for each solid tile and add it to collision_tiles
                        tile_rect = pygame.Rect(x * tmxdata.tilewidth, y * tmxdata.tileheight, tmxdata.tilewidth,
                                                tmxdata.tileheight)
                        colliders.append(tile_rect)
    return colliders


###############################Tiled Functions End#########################################