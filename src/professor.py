import pygame

class Professor(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft = pos)
        
         # movement
        self.direction = -1
        self.speed = 12
        self.gravity = 0.8

        # appearance
        self.state = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
    
    def update(self, x_shift):
        self.rect.x += x_shift