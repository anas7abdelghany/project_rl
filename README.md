# Flappy Bird AI: Reinforcement Learning 

A Reinforcement Learning project where agents learn to play Flappy Bird using Q-Learning and Deep Q-Network (DQN). The agents navigate through pipes by deciding whether to flap or not, optimizing actions based on rewards. The project uses Pygame for the game environment and Matplotlib for visualizing performance.

## Project Overview
This project implements two Reinforcement Learning algorithms—Q-Learning and Deep Q-Network (DQN)—to train AI agents to play Flappy Bird. The custom environment, built with Pygame, includes dynamic pipes, collision detection, and a scoring system. The Q-Learning agent uses a discretized state space (7x21) to update a Q-table, while the DQN agent leverages a neural network to approximate Q-values. Performance is visualized through score progression over generations.

## Features
- **Custom Flappy Bird Environment**: Built with Pygame, featuring dynamic pipes and real-time rendering.
- **Q-Learning Agent**: Uses a 7x21 state space with a learning rate of 0.6 to learn optimal flapping decisions.
- **DQN Agent**: Employs a neural network to approximate Q-values, enabling more complex state handling.
- **Performance Visualization**: Plots score vs. generation using Matplotlib to track learning progress.
- **Interactive Gameplay**: Displays the game with score and generation counters in real-time.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/anas7abdelghany/project_rl.git
   cd project_rl
