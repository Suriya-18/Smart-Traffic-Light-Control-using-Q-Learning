import gym
from gym import spaces
import numpy as np

class TrafficEnv(gym.Env):
    def __init__(self):
        super(TrafficEnv, self).__init__()
        self.max_cars = 10
        self.action_space = spaces.Discrete(2)  # 0: NS green, 1: EW green
        self.observation_space = spaces.MultiDiscrete([self.max_cars+1]*4)  # [N, S, E, W]

        self.reset()

    def reset(self):
        self.state = np.random.randint(0, self.max_cars+1, size=4)
        return self.state

    def step(self, action):
        cars = self.state.copy()
        reward = 0

        # Cars pass based on green signal
        if action == 0:  # NS green
            passed = min(2, cars[0]) + min(2, cars[1])
            reward = passed
            cars[0] = max(0, cars[0] - 2)
            cars[1] = max(0, cars[1] - 2)
        else:  # EW green
            passed = min(2, cars[2]) + min(2, cars[3])
            reward = passed
            cars[2] = max(0, cars[2] - 2)
            cars[3] = max(0, cars[3] - 2)

        # New cars arrive randomly
        new_cars = np.random.randint(0, 3, size=4)
        self.state = np.clip(cars + new_cars, 0, self.max_cars)

        done = False
        return self.state, reward, done, {}

    def render(self, mode='human'):
        print(f"State: N:{self.state[0]} S:{self.state[1]} E:{self.state[2]} W:{self.state[3]}")
