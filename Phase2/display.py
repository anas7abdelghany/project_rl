import pygame
from pygame.locals import *

from environment import BIRD_X_POS

# Game constants
SW = 280
SH = 511
BASEY = SH * 0.8
FPS = 32

def static(window):
    # Display the starting screen
    birdxpos = int(SW / 5)
    birdypos = int((SH - pygame.image.load('imgs/bird1.png').get_height()) / 2)
    basex = 0
    font = pygame.font.SysFont("comicsans", 30)
    images = {
        'background': pygame.image.load('imgs/bg.png').convert(),
        'bird': pygame.image.load('imgs/bird1.png').convert_alpha(),
        'base': pygame.image.load('imgs/base.png').convert_alpha()
    }
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
        window.blit(images['background'], (0, 0))
        window.blit(images['bird'], (birdxpos, birdypos))
        window.blit(images['base'], (basex, BASEY))
        text1 = font.render("AI PROJECT", 1, (255, 255, 255))
        text2 = font.render("HARKISHAN SINGH", 1, (255, 255, 255))
        window.blit(text1, (SW / 2, SH / 2))
        window.blit(text2, (10, 50))
        pygame.display.update()
        pygame.time.Clock().tick(FPS)

def render(window, env, generation):
    # Render the game
    window.blit(env.images['background'], (env.bgx1, 0))
    window.blit(env.images['background'], (env.bgx2, 0))
    for upper_pipe, lower_pipe in zip(env.up_pipes, env.bttm_pipes):
        window.blit(env.images['pipe'][0], (upper_pipe['x'], upper_pipe['y']))
        window.blit(env.images['pipe'][1], (lower_pipe['x'], lower_pipe['y']))
    window.blit(env.images['base'], (env.basex1, BASEY))
    window.blit(env.images['base'], (env.basex2, BASEY))
    font = pygame.font.SysFont("comicsans", 30)
    text1 = font.render("Score: " + str(env.score), 1, (255, 255, 255))
    text2 = font.render("Generation: " + str(generation), 1, (255, 255, 255))
    window.blit(text1, (SW - 10 - text1.get_width(), 10))
    window.blit(text2, (0, 0))
    window.blit(env.images['bird'], (BIRD_X_POS, env.bird_y_pos))
    pygame.display.update()
