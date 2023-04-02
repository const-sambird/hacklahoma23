import pygame
from util import import_folder

class ParkingServiceTicket(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations[self.frame_index]
        self.rect = self.image.get_rect(midtop = pos)
        
         # movement
        self.direction = -1
        self.speed = 12
        
        # functionality 
        self.here = 1 # checks if the ticket has been killed

        # appearance
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
    
    def import_character_assets(self):
        path = '../assets/projectile/'
        self.animations = import_folder(path)

    def animate(self):
        animation = self.animations

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.rect.center)
        self.image = image
    
    def update(self, x_shift):
        self.rect.x += x_shift
        self.animate()