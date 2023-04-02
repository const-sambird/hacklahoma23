import pygame

class Chatgpt(pygame.sprite.Sprite): # powerup for dashing
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.image.load('../assets/tiles/chatgpt.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
    
    def update(self, x_shift):
        self.rect.x += x_shift