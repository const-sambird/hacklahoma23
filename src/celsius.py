import pygame


class Celsius(pygame.sprite.Sprite): # powerup to increase speed
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.image.load('../assets/tiles/celsius.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
    
    def update(self, x_shift):
        self.rect.x += x_shift