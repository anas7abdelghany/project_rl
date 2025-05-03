from environment import BIRD_X_POS
import pygame
from pygame.locals import *

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

    # Button properties
    button_font = pygame.font.SysFont("comicsans", 25)
    button_width = 200
    button_height = 50
    button_color = (0, 120, 0)  # Dark green
    hover_color = (0, 200, 0)   # Light green
    text_color = (255, 255, 255)
    
    # Start Game button
    start_button_text = "Start Game"
    start_button_x = SW / 2 - button_width / 2
    start_button_y = SH / 2 + 20
    
    # Team Members button
    team_button_text = "Team Members"
    team_button_x = SW / 2 - button_width / 2
    team_button_y = start_button_y + button_height + 20
    
    # Game Info button
    info_button_text = "Game Info"
    info_button_x = SW / 2 - button_width / 2
    info_button_y = team_button_y + button_height + 20

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Check Start Game button
                if start_button_x <= mouse_pos[0] <= start_button_x + button_width and start_button_y <= mouse_pos[1] <= start_button_y + button_height:
                    return  # Exit loop and start game
                # Check Team Members button
                elif team_button_x <= mouse_pos[0] <= team_button_x + button_width and team_button_y <= mouse_pos[1] <= team_button_y + button_height:
                    show_team_members(window)
                # Check Game Info button
                elif info_button_x <= mouse_pos[0] <= info_button_x + button_width and info_button_y <= mouse_pos[1] <= info_button_y + button_height:
                    show_game_info(window)

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

        # Display title
        title_text = font.render("RL PROJECT", 1, (255, 255, 255))
        window.blit(title_text, (SW / 2 - title_text.get_width() / 2, SH / 2 - 50))

        # Draw Start Game button
        mouse_pos = pygame.mouse.get_pos()
        
        # Start button
        start_button_current_color = hover_color if start_button_x <= mouse_pos[0] <= start_button_x + button_width and start_button_y <= mouse_pos[1] <= start_button_y + button_height else button_color
        pygame.draw.rect(window, start_button_current_color, (start_button_x, start_button_y, button_width, button_height))
        start_button_text_render = button_font.render(start_button_text, True, text_color)
        window.blit(start_button_text_render, (start_button_x + button_width / 2 - start_button_text_render.get_width() / 2, 
                                           start_button_y + button_height / 2 - start_button_text_render.get_height() / 2))
        
        # Team Members button
        team_button_current_color = hover_color if team_button_x <= mouse_pos[0] <= team_button_x + button_width and team_button_y <= mouse_pos[1] <= team_button_y + button_height else button_color
        pygame.draw.rect(window, team_button_current_color, (team_button_x, team_button_y, button_width, button_height))
        team_button_text_render = button_font.render(team_button_text, True, text_color)
        window.blit(team_button_text_render, (team_button_x + button_width / 2 - team_button_text_render.get_width() / 2, 
                                          team_button_y + button_height / 2 - team_button_text_render.get_height() / 2))
        
        # Game Info button
        info_button_current_color = hover_color if info_button_x <= mouse_pos[0] <= info_button_x + button_width and info_button_y <= mouse_pos[1] <= info_button_y + button_height else button_color
        pygame.draw.rect(window, info_button_current_color, (info_button_x, info_button_y, button_width, button_height))
        info_button_text_render = button_font.render(info_button_text, True, text_color)
        window.blit(info_button_text_render, (info_button_x + button_width / 2 - info_button_text_render.get_width() / 2, 
                                           info_button_y + button_height / 2 - info_button_text_render.get_height() / 2))

        pygame.display.update()
        clock.tick(FPS)

def render(window, env, generation, reward=None):
    # Render the game (with added reward display)
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
    
    # Add reward display if available
    if reward is not None:
        text3 = font.render("Reward: " + str(round(reward, 2)), True, (255, 255, 255))
        window.blit(text3, (10, 45))
    
    window.blit(text1, (SW - text1.get_width() - 10, 10))
    window.blit(text2, (10, 10))

    pygame.display.update()


def show_team_members(window):
    """Display team members information in a popup screen"""
    team_members = [
        "Ahmed hussain",
        "Ans Abd Elghany",
        "khloud Emad",
        "Omar Hamed"
    ]
    
    running = True
    font = pygame.font.SysFont("comicsans", 25)
    title_font = pygame.font.SysFont("comicsans", 35)
    
    # Back button properties
    back_button_text = "Back"
    button_width = 150
    button_height = 40
    button_x = SW / 2 - button_width / 2
    button_y = SH - 80
    button_color = (0, 120, 0)  # Dark green
    hover_color = (0, 200, 0)   # Light green
    text_color = (255, 255, 255)
    
    clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height:
                    running = False
        
        # Fill background
        window.fill((0, 0, 0))
        
        # Draw title
        title = title_font.render("Team Members", True, (255, 255, 255))
        window.blit(title, (SW / 2 - title.get_width() / 2, 40))
        
        # Draw team members
        y_offset = 120
        for member in team_members:
            text = font.render(member, True, (255, 255, 255))
            window.blit(text, (SW / 2 - text.get_width() / 2, y_offset))
            y_offset += 50
        
        # Draw back button
        mouse_pos = pygame.mouse.get_pos()
        button_current_color = hover_color if button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height else button_color
        pygame.draw.rect(window, button_current_color, (button_x, button_y, button_width, button_height))
        button_text_render = font.render(back_button_text, True, text_color)
        window.blit(button_text_render, (button_x + button_width / 2 - button_text_render.get_width() / 2, button_y + button_height / 2 - button_text_render.get_height() / 2))
        
        pygame.display.update()
        clock.tick(FPS)

def show_game_info(window):
    """Display game information in a popup screen"""
    game_info = [
        "Flappy Bird RL",
        "Mintor : Eng / Maryam Elgendy",
        "Learn to fly using Q_table algorithm",
        "Press SPACE to start",
        "The AI learn with each generation",
        "Higher rewards mean better performance"
    ]
    
    running = True
    font = pygame.font.SysFont("comicsans", 25)
    title_font = pygame.font.SysFont("comicsans", 35)
    
    # Back button properties
    back_button_text = "Back"
    button_width = 150
    button_height = 40
    button_x = SW / 2 - button_width / 2
    button_y = SH - 80
    button_color = (0, 120, 0)  # Dark green
    hover_color = (0, 200, 0)   # Light green
    text_color = (255, 255, 255)
    
    clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height:
                    running = False
        
        # Fill background
        window.fill((0, 0, 0))
        
        # Draw title
        title = title_font.render("Game Information", True, (255, 255, 255))
        window.blit(title, (SW / 2 - title.get_width() / 2, 40))
        
        # Draw game info
        y_offset = 120
        for info in game_info:
            text = font.render(info, True, (255, 255, 255))
            window.blit(text, (SW / 2 - text.get_width() / 2, y_offset))
            y_offset += 50
        
        # Draw back button
        mouse_pos = pygame.mouse.get_pos()
        button_current_color = hover_color if button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height else button_color
        pygame.draw.rect(window, button_current_color, (button_x, button_y, button_width, button_height))
        button_text_render = font.render(back_button_text, True, text_color)
        window.blit(button_text_render, (button_x + button_width / 2 - button_text_render.get_width() / 2, button_y + button_height / 2 - button_text_render.get_height() / 2))
        
        pygame.display.update()
        clock.tick(FPS)
