import pygame

class Stairs(pygame.sprite.Sprite): # stairs to move to the next level
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.image.load('../assets/tiles/stairs.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

    def update(self, x_shift):
        self.rect.x += x_shift