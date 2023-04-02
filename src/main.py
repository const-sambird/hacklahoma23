import pygame, sys, cv2
from settings import *
from tiles import Tile
from level import Level

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

backgrounds = pygame.image.load("../assets/backgrounds/devon floor 1.jpg")
# Get the image dimensions
image_width, image_height = backgrounds.get_size()

# Calculate the x and y coordinates for the image to be centered on the screen
x = (screen_width - image_width) / 2
y = (screen_height - image_height) / 2


levels = [level_map_1, level_map_2, level_map_3, level_map_4, level_map_5]
level_index = 5

lives = 3
level = Level(levels[level_index - 1], screen, level_index, lives)


# Dictionary of level numbers and corresponding background image filenames
backgrounds = {1: "../assets/backgrounds/devon floor 1.jpg", 2: "../assets/backgrounds/devon floor 2.jpg", 3: "../assets/backgrounds/devon floor 3.jpg", 4: "../assets/backgrounds/devon floor 4.jpg", 5: "../assets/backgrounds/902358-pixel-art-artwork-city-sunrise-skyline-cityscape.png"}
background_img = pygame.image.load(backgrounds[1])

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    
    screen.blit(background_img, (x,y))
    level.run()
    
    pygame.display.update()
    clock.tick(60)

    if level.next_level:
        cap = cv2.VideoCapture('../assets/cutscene.mov')
        success, img = cap.read()
        shape = img.shape[1::-1]
        while success:
            clock.tick(60)
            success, img = cap.read()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    success = False
            if not success:
                break
            screen.blit(pygame.image.frombuffer(img.tobytes(), shape, "BGR"), (0, 0))
            pygame.display.update()

        if (level_index <= 5):
            level_index += 1
            level = Level(levels[level_index - 1], screen, level_index, lives)
            # Load background image based on current level number
            background_img = pygame.image.load(backgrounds[level_index])
            screen.blit(background_img, (x,y))
            pygame.display.update()
            
    
    if level.dead:
        lives -= 1
        level_index = 1
        level = Level(levels[level_index - 1], screen, level_index, lives)
        if lives < 1:
            break

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill('black')
    font = pygame.font.Font('../assets/font.ttf', 64)
    game_over = font.render("Game Over", False, 'white')
    w, h = font.size("Game Over")
    screen.blit(game_over, ((screen_width - w) // 2, (screen_height - h) // 2))
    pygame.display.update()
    clock.tick(60)
