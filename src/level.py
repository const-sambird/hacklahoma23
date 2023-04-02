import pygame
from tiles import Tile
from player import Player
from settings import tile_size, screen_width
from stairs import Stairs


class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.setup_level(level_data)

        self.world_shift = 0
        self.current_x = 0

        self.next_level = False


    def setup_level(self, layout):
        pygame.mixer.music.load('../music/world1.mp3')
        pygame.mixer.music.play(-1)

        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.stairs = pygame.sprite.GroupSingle()

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if cell == 'X':
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                elif cell == 'P':
                    tile = Player((x, y))
                    self.player.add(tile)
                if cell == "L":
                    staircase = Stairs((x, y), tile_size)
                    self.stairs.add(staircase)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right
        
        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        elif player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False
    
    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()


        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
        
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    def go_stairs(self):
        player = self.player.sprite

        stair_sprite = self.stairs.sprites()[0]

        if stair_sprite.rect.colliderect(player.rect):
            self.next_level = True
            #print(main.level_number)

    def run(self):
        self.stairs.update(self.world_shift)
        self.stairs.draw(self.display_surface)

        # draw tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()

        # draw player
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()

        self.go_stairs()
        self.player.draw(self.display_surface)