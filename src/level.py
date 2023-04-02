import pygame
from random import randint
from tiles import Tile
from player import Player
from settings import tile_size, screen_width
from stairs import Stairs
from celsius import Celsius
from chatgpt import Chatgpt
from professor import Professor
from parkingservicesAI import ParkingServicesAI
from parkingservicesTicket import ParkingServiceTicket
from boss import Boss

import random

songs = ['../music/world_1.mp3', '../music/world_2.mp3', '../music/cynthia.mp3']


class Level:
    def __init__(self, level_data, surface, level_index, lives):
        self.display_surface = surface
        self.level_index = level_index

        self.load_assets()
        self.setup_level(level_data)

        self.world_shift = 0
        self.current_x = 0
        self.basespeed = 8
        self.lives = lives

        self.next_level = False
        self.dead = False

    def load_assets(self):
        if (self.level_index == 1):
            pygame.mixer.music.load('../music/world_1.mp3')
        elif (self.level_index == 2):
            pygame.mixer.music.load('../music/world_2.mp3')
        elif (self.level_index == 3):
            pygame.mixer.music.load('../music/world_3.mp3')
        elif (self.level_index == 4):
            pygame.mixer.music.load('../music/world_4.mp3')
        elif (self.level_index == 5):
            pygame.mixer.music.load('../music/cynthia.mp3')
        
        self.font = pygame.font.Font('../assets/font.ttf', 32)

        pygame.mixer.music.play(-1)


    def setup_level(self, layout):

        self.tiles = pygame.sprite.Group()
        self.professors = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.stairs = pygame.sprite.GroupSingle()
        self.celsius = pygame.sprite.Group()
        self.chatgpt = pygame.sprite.Group()
        self.parkingServicesAI = pygame.sprite.Group()
        self.parkingServiceTicket = pygame.sprite.Group()
        self.boss = pygame.sprite.GroupSingle()

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
                elif cell == 'S':
                    tile = Celsius((x,y), tile_size)
                    self.celsius.add(tile)
                elif cell == 'G':
                    tile = Chatgpt((x,y), tile_size)
                    self.chatgpt.add(tile)
                elif cell == 'O':
                    professors = Professor((x,y))
                    self.professors.add(professors) 
                elif cell == 'A':
                    parkingServicesAI = ParkingServicesAI((x,y), tile_size)
                    self.parkingServicesAI.add(parkingServicesAI) 
                # make rng
                elif cell == "L":
                    staircase = Stairs((x, y), tile_size)
                    self.stairs.add(staircase)
                elif cell == "B":
                    boss_sprite = Boss((x, y))
                    self.boss.add(boss_sprite)
                # if cell == 'G':
                #     chatgpt = Chatgpt((x,y),tile_size)
                #     self.Chatgpt.add()

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8 * player.boost
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8 * player.boost
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8 * player.boost

    def horizontal_movement_collision(self):
        player = self.player.sprite
        
        player.rect.x += player.direction.x * player.speed

        # have powerups expired?
        if pygame.time.get_ticks() - player.boosted_at > 3000:
            player.boost = 1

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
        
        # collision with powerup
        for sprite in self.celsius.sprites():
            if sprite.rect.colliderect(player.rect):
                player.boost = 2
                player.boosted_at = pygame.time.get_ticks()
                sprite.kill()

        for sprite in self.chatgpt.sprites():
            if sprite.rect.colliderect(player.rect):
                player.dashes += 1
                sprite.kill()
                
        # updates the direction and speed of each professor sprite
        for professor in self.professors.sprites():
            professor.rect.x += professor.direction.x * professor.speed

            # collision function for professors
            for sprite in self.tiles.sprites():
                if sprite.rect.colliderect(professor.rect):
                    if professor.direction.x < 0:
                        professor.rect.left = sprite.rect.right
                        professor.on_left = True
                        professor.on_right = False
                        professor.direction.x = -professor.direction.x

                    elif professor.direction.x > 0:
                        professor.rect.right = sprite.rect.left
                        professor.on_right = True
                        professor.on_left = False
                        professor.direction.x = -professor.direction.x

            if professor.rect.colliderect(player.rect) and player.direction.y >= 0:
                self.go_die()

        # updates the direction and speed of each professor sprite
        for parkingServiceTicket in self.parkingServiceTicket.sprites():
            parkingServiceTicket.rect.x += parkingServiceTicket.direction * parkingServiceTicket.speed
        
            # collsion funtion for tickets
            for sprite in self.tiles.sprites():
                if sprite.rect.colliderect(parkingServiceTicket.rect):
                    parkingServiceTicket.kill()
                    parkingServiceTicket.here = 0

            if parkingServiceTicket.rect.colliderect(player.rect):
                self.go_die()
            
        
    

        # updates the direction and speed of each professor sprite
        for boss in self.boss.sprites():
            boss.speed = random.randint(6,12)
            boss.rect.x += boss.direction * boss.speed
            for sprite in self.tiles.sprites():
                if sprite.rect.colliderect(boss.rect):
                    if boss.direction < 0:
                        boss.rect.left = sprite.rect.right
                        boss.on_left = True
                        boss.on_right = False
                        boss.direction = -boss.direction

                    elif boss.direction > 0:
                        boss.rect.right = sprite.rect.left
                        boss.on_right = True
                        boss.on_left = False
                        boss.direction = -boss.direction

            if player.rect.colliderect(boss.rect) and player.direction.y >= 0:
                self.go_die()

        # # collision function for professors
        # for sprite in self.tiles.sprites():
        #     for boss in self.boss.sprites():
        #         if sprite.rect.colliderect(boss.rect):
        #             if boss.direction < 0:
        #                 boss.rect.left = sprite.rect.right
        #                 boss.on_left = True
        #                 boss.on_right = False
        #                 boss.direction = -boss.direction
        #
        #             elif boss.direction > 0:
        #                 boss.rect.right = sprite.rect.left
        #                 boss.on_right = True
        #                 boss.on_left = False
        #                 boss.direction = -boss.direction

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
        
        for professor in self.professors.sprites():
            professor.apply_gravity()
            for sprite in self.tiles.sprites():
                if sprite.rect.colliderect(professor.rect):
                    if professor.direction.y >= 0:
                        professor.rect.bottom = sprite.rect.top
                        professor.direction.y = 0
                        professor.on_ground = True
                    elif professor.direction.y < 0:
                        professor.rect.top = sprite.rect.bottom
                        professor.direction.y = 0
                        professor.on_ceiling = True

        for boss in self.boss.sprites():
            if boss.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.jump()
                    if (boss.health == 1):
                        boss.kill()
                    else:
                        boss.health -= 1

        for professor in self.professors.sprites():
            if professor.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.jump()
                    professor.kill()

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

        # need a collision function for professors
    
    def go_stairs(self):
        player = self.player.sprite

        stair_sprite = self.stairs.sprites()[0]

        if stair_sprite.rect.colliderect(player.rect):
            self.next_level = True
            pygame.mixer.pause()
            #print(main.level_number)
    
    def go_die(self):
        self.dead = True
        pygame.mixer.pause()
    
    def draw_overlay(self):
        player = self.player.sprite
        dashes = player.dashes
        lives = self.lives
        tick = pygame.time.get_ticks() # replace

        dashes_text = self.font.render("DASH " + str(dashes), False, 'white')
        lives_text = self.font.render("LIFE " + str(lives), False, 'white')
        tick_text = self.font.render("TICK " + str(tick), False, 'white')


        self.display_surface.blit(dashes_text, (screen_width / 8, 100))
        self.display_surface.blit(lives_text, (3 * screen_width / 8, 100))
        self.display_surface.blit(tick_text, (5 * screen_width / 8, 100))

        if (self.level_index == 5):
            try:
                boss_text = self.font.render("BOSS HP: " + str(self.boss.sprites()[0].health), False, 'red')
                self.display_surface.blit(boss_text, (5 * screen_width / 8, 50))
            except:
                pass

        if (player.boost == 2):
            celsius_text = self.font.render("CELSIUS", False, 'grey')
            self.display_surface.blit(celsius_text, (screen_width / 8, 50))

    def throw_ticket(self):
        for sprite in self.parkingServicesAI.sprites():
            roll = randint(1, 100)
            # print(roll)
            if roll == 4:
                ticket = ParkingServiceTicket((sprite.rect.x, sprite.rect.y), tile_size)
                self.parkingServiceTicket.add(ticket)

    def run(self):
        self.stairs.update(self.world_shift)
        self.stairs.draw(self.display_surface)

        try:
            self.go_stairs()
        except:
            pass

        # draw tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()

        # draw celsius powerup 
        self.celsius.update(self.world_shift)
        self.celsius.draw(self.display_surface)

        # draw celsius powerup
        self.chatgpt.update(self.world_shift)
        self.chatgpt.draw(self.display_surface)

         # draw professors
        self.professors.update(self.world_shift)
        self.professors.draw(self.display_surface)
        
        # draw parking service 
        self.parkingServicesAI.update(self.world_shift)
        self.parkingServicesAI.draw(self.display_surface)
        
        # draw parking service ticket
        self.throw_ticket()
        self.parkingServiceTicket.draw(self.display_surface)
        self.parkingServiceTicket.update(self.world_shift)
        

        # draw professor
        self.boss.update(self.world_shift)
        self.boss.draw(self.display_surface)

        # draw player
        self.player.update()

        self.vertical_movement_collision()
        self.horizontal_movement_collision()

        self.player.draw(self.display_surface)

        self.draw_overlay() # THIS GOES LAST
        