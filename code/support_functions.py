from os import walk
from settings import *


def import_folder(path: str, scale):
    """
    Importing Folder of images

    :param path: path of a folder of images to import
    :param scale: The number by which you need to increase the image size

    :return: list of pygame.image images
    """
    surface_list = []

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            image_surf = pygame.transform.scale(image_surf, (image_surf.get_rect().width * scale, image_surf.get_rect().height * scale))
            image_surf.set_colorkey("#ffffff")
            surface_list.append(image_surf)

    return surface_list


def import_from_one_image(path:str, vertical_parts:int, horizontal_parts:int, scale, tile_size:int):
    """
    Importing images from one big image

    :param path: path of a folder of images to import
    :param vertical_parts: Number of columns of images
    :param horizontal_parts: Number of rows of images
    :param scale: The number by which you need to increase the image size
    :param tile_size: size of each tile after scaling the image -> width = height = int

    :return: list of pygame.image images
    """
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
    """
    Importing all Images that game need

    :return: dict of textures
    """
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