import pygame
from pygame.locals import *
import sys
import os
import numpy as np
from environment import FlappyBirdEnv
from algorithm import QLAgent
from display import static, render

SW = 500
SH = 500
FPS = 32

def main():
    # Initialize Pygame and set up the window
    pygame.init()
    window = pygame.display.set_mode((SW, SH))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()
    
    # Initialize environment and agent
    env = FlappyBirdEnv()
    agent = QLAgent()
    
    # Load Q-table if it exists
    if os.path.exists('q_table.npy'):
        agent.Q = np.load('q_table.npy')
        print("Loaded Q-table from q_table.npy")
    
    generation = 1
    
    # Show the starting screen
    static(window)
    
    while True:
        # Move the base and reset the environment
        env.move_base()
        state = env.reset()
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            
            # Get current state and choose action
            x_prev, y_prev = state
            action = agent.choose_action(x_prev, y_prev)
            
            # Take action and update Q-table
            next_state, reward, done, info = env.step(action)
            x_new, y_new = next_state
            agent.update(x_prev, y_prev, action, reward, x_new, y_new)
            
            # Render the game
            render(window, env, generation)
            clock.tick(FPS)
            
            state = next_state
            if done:
                # Save Q-table after each generation
                np.save('q_table.npy', agent.Q)
                generation += 1
                print(f"Generation {generation}, Score: {info['score']}")
                break

if __name__ == "__main__":
    main()
