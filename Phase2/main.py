import pygame
from pygame.locals import *
import sys  
from environment import FlappyBirdEnv
from algorithm import QLAgent
from display import static, render

SW = 280
SH = 511
FPS = 32

def main():
    pygame.init()
    window = pygame.display.set_mode((SW, SH))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()
    
    env = FlappyBirdEnv()
    agent = QLAgent()
    generation = 1
    
    static(window)
    
    while True:
        state = env.reset()
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit() 
            
            x_prev, y_prev = state
            action = agent.choose_action(x_prev, y_prev)
            next_state, reward, done, info = env.step(action)
            x_new, y_new = next_state
            agent.update(x_prev, y_prev, action, reward, x_new, y_new)
            render(window, env, generation)
            clock.tick(FPS)
            
            state = next_state
            if done:
                generation += 1
                print(f"Generation {generation}, Score: {info['score']}")
                break

if __name__ == "__main__":
    main()
