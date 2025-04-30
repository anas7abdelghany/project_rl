import pygame
import random
import numpy as np

# Game constants
SW = 280
SH = 511
BASEY = SH * 0.8
PIPE_GAP = int(SH / 4)
PIPE_VEL_X = -4
BIRD_X_POS = int(SW / 5)
BIRD_Y_VEL = -9
BIRD_Y_MAX_VEL = 10
BIRD_Y_VEL_MIN = -8
BIRD_Y_ACC = 1
PLAYER_FLAP_ACC_V = -8

class FlappyBirdEnv:
    def __init__(self):
        # Load images
        self.images = {
            'bird': pygame.image.load(r'C:\Users\cc\OneDrive\Desktop\reinforce\imgs\bird1.png').convert_alpha(),
            'background': pygame.image.load(r'C:\Users\cc\OneDrive\Desktop\reinforce\imgs\bg.png').convert(),
            'pipe': (
                pygame.transform.rotate(pygame.image.load(r'C:\Users\cc\OneDrive\Desktop\reinforce\imgs\pipe.png').convert_alpha(), 180),
                pygame.image.load(r'C:\Users\cc\OneDrive\Desktop\reinforce\imgs\pipe.png').convert_alpha()
            ),
            'base': pygame.image.load(r'C:\Users\cc\OneDrive\Desktop\reinforce\imgs\base.png').convert_alpha()
        }
        
        # Initialize game state
        self.bird_y_pos = int(SH / 2)
        self.bird_y_vel = 0
        self.player_flapped = False
        self.basex1 = 0
        self.basex2 = SW
        self.bgx1 = 0
        self.bgx2 = self.images['background'].get_width()
        self.score = 0
        
        # Initialize pipes
        new_pipe1 = self.get_new_pipe()
        new_pipe2 = self.get_new_pipe()
        self.up_pipes = [
            {'x': SW + 200, 'y': new_pipe1[0]['y']},
            {'x': SW + 500, 'y': new_pipe2[0]['y']}
        ]
        self.bttm_pipes = [
            {'x': SW + 200, 'y': new_pipe1[1]['y']},
            {'x': SW + 500, 'y': new_pipe2[1]['y']}
        ]
        
        self.action_space = [0, 1]  # 0: Do nothing, 1: Jump

    def reset(self):
        # Reset game state
        self.bird_y_pos = int(SH / 2)
        self.bird_y_vel = 0
        self.player_flapped = False
        self.basex1 = 0
        self.basex2 = SW
        self.bgx1 = 0
        self.bgx2 = self.images['background'].get_width()
        self.score = 0
        
        # Reset pipes
        new_pipe1 = self.get_new_pipe()
        new_pipe2 = self.get_new_pipe()
        self.up_pipes = [
            {'x': SW + 200, 'y': new_pipe1[0]['y']},
            {'x': SW + 500, 'y': new_pipe2[0]['y']}
        ]
        self.bttm_pipes = [
            {'x': SW + 200, 'y': new_pipe1[1]['y']},
            {'x': SW + 500, 'y': new_pipe2[1]['y']}
        ]
        
        return self.get_state()

    def get_state(self):
        # Get state as defined in convert function
        x, y = self.convert()
        return x, y

    def convert(self):
        # Convert bird and pipe positions to state
        x = min(280, self.bttm_pipes[0]['x'])
        y = self.bttm_pipes[0]['y'] - self.bird_y_pos
        if y < 0:
            y = abs(y) + 408
        return int(x / 40 - 1), int(y / 40)

    def step(self, action):
        # Update game state based on action
        jump = action == 1
        
        # Handle jump
        if jump and self.bird_y_pos > 0:
            self.bird_y_vel = PLAYER_FLAP_ACC_V
            self.player_flapped = True

        # Update bird velocity and position
        if self.bird_y_vel < BIRD_Y_MAX_VEL and not self.player_flapped:
            self.bird_y_vel += BIRD_Y_ACC
        if self.player_flapped:
            self.player_flapped = False
        
        player_height = self.images['bird'].get_height()
        self.bird_y_pos += min(self.bird_y_vel, BASEY - self.bird_y_pos - player_height)

        # Update pipes
        for upper_pipe, lower_pipe in zip(self.up_pipes, self.bttm_pipes):
            upper_pipe['x'] += PIPE_VEL_X
            lower_pipe['x'] += PIPE_VEL_X

        # Add new pipe
        if 0 < self.up_pipes[0]['x'] < 5:
            new_pipe = self.get_new_pipe()
            self.up_pipes.append(new_pipe[0])
            self.bttm_pipes.append(new_pipe[1])

        # Remove off-screen pipes
        if self.up_pipes[0]['x'] < -self.images['pipe'][0].get_width():
            self.up_pipes.pop(0)
            self.bttm_pipes.pop(0)

        # Update base and background
        self.basex1 -= 4
        self.basex2 -= 4
        if self.basex1 <= -self.images['base'].get_width():
            self.basex1 = self.basex2
            self.basex2 = self.basex1 + self.images['base'].get_width()
        
        self.bgx1 -= 2
        self.bgx2 -= 2
        if self.bgx1 <= -self.images['background'].get_width():
            self.bgx1 = self.bgx2
            self.bgx2 = self.bgx1 + self.images['background'].get_width()

        # Check collision
        done = self.collision()
        reward = -1000 if done else 15

        # Update score
        player_mid_pos = BIRD_X_POS + self.images['bird'].get_width() / 2
        for pipe in self.up_pipes:
            pipe_mid_pos = pipe['x'] + self.images['pipe'][0].get_width() / 2
            if pipe_mid_pos <= player_mid_pos < pipe_mid_pos + 4:
                self.score += 1

        next_state = self.get_state()
        info = {"score": self.score}

        return next_state, reward, done, info

    def collision(self):
        # Check for collision
        if self.bird_y_pos >= BASEY - self.images['bird'].get_height() or self.bird_y_pos < 0:
            return True
        for pipe in self.up_pipes:
            pipe_height = self.images['pipe'][0].get_height()
            if (self.bird_y_pos < pipe_height + pipe['y'] and 
                abs(BIRD_X_POS - pipe['x']) < self.images['pipe'][0].get_width()):
                return True
        for pipe in self.bttm_pipes:
            if (self.bird_y_pos + self.images['bird'].get_height() > pipe['y'] and 
                abs(BIRD_X_POS - pipe['x']) < self.images['pipe'][0].get_width()):
                return True
        return False

    def get_new_pipe(self):
        # Generate new pipe
        pipe_height = self.images['pipe'][1].get_height()
        gap = PIPE_GAP
        y2 = int(gap + random.randrange(0, int(SH - self.images['base'].get_height() - 1.2 * gap)))
        pipe_x = int(SW + 300)
        y1 = int(pipe_height - y2 + gap)
        pipe = [
            {'x': pipe_x, 'y': -y1},
            {'x': pipe_x, 'y': y2}
        ]
        return pipe
