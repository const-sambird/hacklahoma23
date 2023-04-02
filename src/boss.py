import pygame
from util import import_folder


class Boss(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations[self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

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

# import pygame
# from util import import_folder
#
#
# class Boss(pygame.sprite.Sprite):
#     def __init__(self, pos):
#         super().__init__()
#         self.import_character_assets()
#         self.frame_index = 0
#         self.animation_speed = 0.15
#         self.image = self.animations['idle'][self.frame_index]
#         self.rect = self.image.get_rect(topleft=pos)
#
#         # player movement
#         self.direction = pygame.math.Vector2()
#         self.speed = 4
#         self.gravity = 0.8
#
#         # player appearance
#         self.state = 'idle'
#         self.facing_right = True
#         self.on_ground = False
#         self.on_ceiling = False
#         self.on_left = False
#         self.on_right = False
#
#     def import_character_assets(self):
#         character_path = '../assets/character/'
#         self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': []}
#
#         for animation in self.animations.keys():
#             full_path = character_path + animation
#             self.animations[animation] = import_folder(full_path)
#
#     def animate(self):
#         animation = self.animations[self.state]
#
#         self.frame_index += self.animation_speed
#         if self.frame_index >= len(animation):
#             self.frame_index = 0
#
#         image = animation[int(self.frame_index)]
#
#         if self.facing_right:
#             self.image = image
#         else:
#             flipped_image = pygame.transform.flip(image, True, False)
#             self.image = flipped_image
#
#         # set the rect
#         if self.on_ground and self.on_right:
#             self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
#         elif self.on_ground and self.on_left:
#             self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
#         elif self.on_ground:
#             self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
#         if self.on_ceiling and self.on_right:
#             self.rect = self.image.get_rect(topright=self.rect.topright)
#         elif self.on_ceiling and self.on_left:
#             self.rect = self.image.get_rect(topleft=self.rect.topleft)
#         elif self.on_ceiling:
#             self.rect = self.image.get_rect(midtop=self.rect.midtop)
#         else:
#             self.rect = self.image.get_rect(center=self.rect.center)
#
#     def get_state(self):
#         if self.direction.y < 0:
#             self.state = 'jump'
#             self.animation_speed = 0.1
#         elif self.direction.y > self.gravity:
#             self.state = 'fall'
#             self.animation_speed = 0.1
#         elif self.direction.x != 0:
#             self.state = 'run'
#             self.animation_speed = 0.3
#         else:
#             self.state = 'idle'
#             self.animation_speed = 0.15
#
#     def update(self, x_shift):
#         self.rect.x += x_shift
#
#         self.get_state()
#         self.animate()
