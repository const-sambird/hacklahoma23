import pygame
from util import import_folder

class Josh(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations[self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        
         # movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 0
        self.gravity = 0.8

        # appearance
        self.state = 'idle'
        self.facing_right = False
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
    
    def import_character_assets(self):
        path = '../assets/josh/'
        self.animations = import_folder(path)
    
    def animate(self):
        animation = self.animations

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.rect.center)

        self.image = image
    
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def update(self, x_shift):
        self.rect.x += x_shift
        self.animate()