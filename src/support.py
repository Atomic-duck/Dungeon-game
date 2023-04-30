from csv import reader
import pygame
from setting import TILE_SIZE
from os import walk


def import_folder(path):
    surface_list = []

    for _, __, image_files in walk(path):
        for image in image_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list


def import_sprite(full_path, num, frame_width, frame_height, img_width):
    surface_list = []

    image_surf = pygame.image.load(full_path).convert_alpha()
    area = pygame.Rect(0, 0, frame_width, frame_height)

    for i in range(num):
        x = i*frame_width
        y = int(x/img_width) * frame_height
        if x >= img_width:
            x %= img_width

        area.x = x
        area.y = y
        cropped = pygame.Surface((frame_width, frame_height))
        cropped.fill((11, 11, 11))
        cropped.set_colorkey((11, 11, 11))
        cropped.blit(image_surf, (0, 0), area)
        surface_list.append(cropped)

    return surface_list


def import_csv_layout(path):
    tile_layout = []
    with open(path) as map:
        level = reader(map, delimiter=',')
        for row in level:
            tile_layout.append(list(row))

    return tile_layout


def import_cut_graphics(path):
    surface_list = []
    surface = pygame.image.load(path).convert_alpha()
    num_col = int(surface.get_size()[0]/TILE_SIZE)
    num_row = int(surface.get_size()[1]/TILE_SIZE)

    if num_col == 0:
        num_col = 1
    if num_row == 0:
        num_row = 1

    for idx_row in range(num_row):
        for idx_col in range(num_col):
            cutted_surface = pygame.Surface(
                (TILE_SIZE, TILE_SIZE), flags=pygame.SRCALPHA)
            cutted_surface
            x = idx_col * TILE_SIZE
            y = idx_row * TILE_SIZE

            cutted_surface.blit(surface, (0, 0), pygame.Rect(
                x, y, TILE_SIZE, TILE_SIZE))
            surface_list.append(cutted_surface)

    return surface_list
