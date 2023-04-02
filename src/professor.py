import pygame
from util import import_folder

class Professor(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations[self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        
         # movement
        self.direction = -1
        self.speed = 4
        self.gravity = 0.8

        # appearance
        self.state = 'idle'
        self.facing_right = False
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
    
    def import_character_assets(self):
        path = '../assets/professor/'
        self.animations = import_folder(path)
    
    def animate(self):
        animation = self.animations

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        image = animation[int(self.frame_index)]

        if self.on_left:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image
    
    def update(self, x_shift):
        self.rect.x += x_shift
        self.animate()