from os import walk
from settings import *


def import_folder(path, scale):
    surface_list = []

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            image_surf = pygame.transform.scale(image_surf, (image_surf.get_rect().width * scale, image_surf.get_rect().height * scale))
            image_surf.set_colorkey("#ffffff")
            surface_list.append(image_surf)

    return surface_list


def import_from_one_image(path, vertical_parts, horizontal_parts, scale, tile_size):
    image = pygame.image.load(path)
    image = pygame.transform.scale(image, (image.get_rect().width * scale, image.get_rect().height * scale))
    ret = []


    for j in range(vertical_parts):
        for i in range(horizontal_parts):
            img = pygame.Surface(tile_size)
            img.blit(image, [0 - tile_size[0] * i, 0 - tile_size[1] * j])
            img.set_colorkey("#ffffff")
            ret.append(img)

    return ret


def import_images():
    ret = {
        "Character": {
            "idle": import_folder(PATHS["Character"]["idle"], TILE_SIZE / 8),
            "run": import_folder(PATHS["Character"]["run"], TILE_SIZE / 8),
            "jump": import_folder(PATHS["Character"]["jump"], TILE_SIZE / 8),
        },

        "Textures": {
            "platforms": import_folder(PATHS["Textures"]["platforms"], TILE_SIZE / 8),
            "blocks": import_from_one_image(PATHS["Textures"]["blocks"], 1, 5, TILE_SIZE / 8, [TILE_SIZE, TILE_SIZE]),
            "grass": import_folder(PATHS["Textures"]["grass"], TILE_SIZE / 8),
        }
    }

    return ret