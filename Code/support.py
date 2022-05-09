import pygame
import os


def import_cut_graphics(path: str, tile_width: int, tile_height: int) -> list:
    image = pygame.image.load(os.path.join("../Resources/", path)).convert_alpha()
    tile_num_x = image.get_size()[0] // tile_width
    tile_num_y = image.get_size()[1] // tile_height
    cut_images = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_width
            y = row * tile_height
            cut = pygame.Surface((tile_width, tile_height))
            cut.set_colorkey(0)
            cut = cut.convert_alpha()
            cut.blit(image, (0, 0), pygame.Rect(x, y, tile_width, tile_height))
            cut_images.append(cut)

    return cut_images


def get_center(surface=None) -> tuple:
    if surface:
        center_x = pygame.display.get_window_size()[0] / 2 - surface.get_size()[0] / 2
        center_y = pygame.display.get_window_size()[1] / 2 - surface.get_size()[1] / 2
    else:
        center_x = pygame.display.get_window_size()[0] / 2
        center_y = pygame.display.get_window_size()[1] / 2
    return center_x, center_y


def timer(current_time, duration):
    """
    :param current_time: Time since the timer start
    :param duration: Transition duration in seconds
    :return: True if the timer ends, False if not
    """
    if pygame.time.get_ticks() - current_time > (duration * 1000):
        return True
    return False
