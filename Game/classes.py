import numpy as np

MAX_ORIENTATION = 10

class Car:
    def __init__(self):
        self.pos = np.zeros(2)
        self.speed = 0
        self.orientation = 0
        self.top_speed = 100

    def accelerate(self, acc, dt):
        self.speed += acc * dt

    def set_speed(self, speed):
        self.speed = speed

    def set_orientation(self, orientation):
        self.orientation = orientation

    def turn(self, angle):
        self.orientation = min(MAX_ORIENTATION, self.orientation + np.radians(angle))

    def update_state(self, dt):
        self.pos[0] += np.cos(self.orientation) * self.speed * dt 
        self.pos[1] += np.sin(self.orientation) * self.speed * dt