import numpy as np

class QLAgent:
    def __init__(self):
        # Initialize Q-Table
        self.Q = np.zeros((7, 21, 2), dtype=float)
        self.actions = [0, 1]  # 0: Do nothing, 1: Jump

    def choose_action(self, x, y):
        # Choose action based on Q-values
        return 1 if self.Q[x][y][1] > self.Q[x][y][0] else 0

    def update(self, x_prev, y_prev, action, reward, x_new, y_new):
        # Update Q-Table
        if action == 1:
            self.Q[x_prev][y_prev][1] = 0.4 * self.Q[x_prev][y_prev][1] + (0.6) * (
                reward + max(self.Q[x_new][y_new][0], self.Q[x_new][y_new][1])
            )
        else:
            self.Q[x_prev][y_prev][0] = 0.4 * self.Q[x_prev][y_prev][0] + (0.6) * (
                reward + max(self.Q[x_new][y_new][0], self.Q[x_new][y_new][1])
            )
