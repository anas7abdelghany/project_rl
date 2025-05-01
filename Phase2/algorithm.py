import numpy as np

class QLAgent:
    def __init__(self, learning_rate=0.1, decay_factor=0.9, gamma=0.95):
        self.Q = np.zeros((7, 21, 2), dtype=float)
        self.actions = [0, 1]
        self.learning_rate = learning_rate
        self.decay_factor = decay_factor
        self.gamma = gamma

    def choose_action(self, x, y):
        return 1 if self.Q[x][y][1] > self.Q[x][y][0] else 0

    def update(self, x_prev, y_prev, action, reward, x_next, y_next):
        max_future_q = max(self.Q[x_next][y_next])
        current_q = self.Q[x_prev][y_prev][action]
        self.Q[x_prev][y_prev][action] = (self.decay_factor * current_q + self.learning_rate * (reward + self.gamma * max_future_q))
