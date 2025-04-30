import pygame
from pygame.locals import *
import matplotlib.pyplot as plt
from environment import FlappyBirdEnv
from algorithm import QLAgent
from display import static, render

# Game constants
SW = 280
SH = 511
FPS = 32

def main():
    pygame.init()
    window = pygame.display.set_mode((SW, SH))
    pygame.display.set_caption("AI PROJECT")
    clock = pygame.time.Clock()
    
    env = FlappyBirdEnv()
    agent = QLAgent()
    generation = 1
    x = []
    y = []
    
    static(window)
    
    while True:
        state = env.reset()
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == QUIT:
                    plt.scatter(x, y)
                    plt.xlabel("GENERATION/Number of Trials")
                    plt.ylabel("SCORE")
                    plt.title("Flappy Birds : AI Project")
                    plt.show()
                    pygame.quit()
                    exit()
            
            x_prev, y_prev = state
            action = agent.choose_action(x_prev, y_prev)
            next_state, reward, done, info = env.step(action)
            x_new, y_new = next_state
            agent.update(x_prev, y_prev, action, reward, x_new, y_new)
            render(window, env, generation)
            clock.tick(FPS)
            
            state = next_state
            if done:
                x.append(generation)
                y.append(info['score'])
                generation += 1
                print(f"Generation {generation}, Score: {info['score']}")
                break

if __name__ == "__main__":
    main()
