import pygame, sys
from settings import *
from tiles import Tile
from level import Level

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

levels = [level_map_1, level_map_2, level_map_3, level_map_4, level_map_5]
level_index = 1

level = Level(levels[level_index], screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill('black')
    level.run()

    pygame.display.update()
    clock.tick(60)

    if level.next_level:

        if (level_index <= 5):
            level_index += 1
            level = Level(levels[level_index - 1], screen)
