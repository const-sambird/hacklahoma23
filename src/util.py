from os import walk
import pygame

def import_folder(path):
    surface_list = []
    for root, dirs, imgs in walk(path):
        for img in imgs:
            full_path = path + '/' + img
            surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(surface)
    
    return surface_list
