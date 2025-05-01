import pygame
from pygame.locals import *
from environment import BIRD_X_POS

# Game constants
SW = 500
SH = 500
BASEY = SH * 0.8
FPS = 32

def static(window):
    # Display the starting screen
    birdxpos = int(SW / 5)
    birdypos = int((SH - pygame.image.load('imgs/bird1.png').get_height()) / 2)
    font = pygame.font.SysFont("comicsans", 30)
    
    images = {
        'background': pygame.image.load('imgs/bg.png').convert(),
        'bird': pygame.image.load('imgs/bird1.png').convert_alpha(),
        'base': pygame.image.load('imgs/base.png').convert_alpha()
    }
    
    # Get the background and base image width
    bg_width = images['background'].get_width()
    base_width = images['base'].get_width()

    # Initialize background and base positions
    bgx1 = 0
    bgx2 = bg_width
    basex1 = 0
    basex2 = base_width
    basex3 = basex2 + base_width
    base_speed = 4

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return

        # Move base
        basex1 -= base_speed
        basex2 -= base_speed
        basex3 -= base_speed

        # Reposition base when off-screen
        if basex1 + base_width < 0:
            basex1 = basex3 + base_width
        if basex2 + base_width < 0:
            basex2 = basex1 + base_width
        if basex3 + base_width < 0:
            basex3 = basex2 + base_width

        # Draw everything
        window.blit(images['background'], (bgx1, 0))
        window.blit(images['background'], (bgx2, 0))
        window.blit(images['bird'], (birdxpos, birdypos))
        window.blit(images['base'], (basex1, BASEY))
        window.blit(images['base'], (basex2, BASEY))
        window.blit(images['base'], (basex3, BASEY))

        # Display text
        text1 = font.render("AI PROJECT", 1, (255, 255, 255))
        text2 = font.render("HARKISHAN SINGH", 1, (255, 255, 255))
        window.blit(text1, (SW / 2 - text1.get_width() / 2, SH / 2))
        window.blit(text2, (10, 50))

        pygame.display.update()
        clock.tick(FPS)

def render(window, env, generation):
    # Render the game
    bg_width = env.images['background'].get_width()
    window.blit(env.images['background'], (env.bgx1, 0))
    window.blit(env.images['background'], (env.bgx2, 0))
    
    for upper_pipe, lower_pipe in zip(env.up_pipes, env.bttm_pipes):
        window.blit(env.images['pipe'][0], (upper_pipe['x'], upper_pipe['y']))
        window.blit(env.images['pipe'][1], (lower_pipe['x'], lower_pipe['y']))
    
    # Draw base (repeated 3 times)
    base_width = env.images['base'].get_width()
    window.blit(env.images['base'], (env.basex1, BASEY))
    window.blit(env.images['base'], (env.basex2, BASEY))
    window.blit(env.images['base'], (env.basex2 + base_width, BASEY))

    # Draw bird
    window.blit(env.images['bird'], (BIRD_X_POS, env.bird_y_pos))

    # Draw text
    font = pygame.font.SysFont("comicsans", 30)
    text1 = font.render("Score: " + str(env.score), True, (255, 255, 255))
    text2 = font.render("Generation: " + str(generation), True, (255, 255, 255))
    
    window.blit(text1, (SW - text1.get_width() - 10, 10))
    window.blit(text2, (10, 10))

    pygame.display.update()
