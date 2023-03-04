import numpy as np
import random

MIN_ORIENTATION = np.radians(60)
MAX_ORIENTATION = np.radians(120)

average_obstacle_distance = 200

class Car:
    def __init__(self):
        self.pos = np.zeros(2)
        self.speed = 0
        self.orientation = 0

    def accelerate(self, acc, dt):
        self.speed += acc * dt

    def set_speed(self, speed):
        self.speed = speed

    def set_orientation(self, orientation):
        self.orientation = orientation

    def turn(self, angle):
        """
        angle en degrés
        """
        self.orientation = self.orientation + np.radians(angle)
        if angle < 0 :
            self.orientation = max(self.orientation, MIN_ORIENTATION)
        elif angle > 0:
            self.orientation = min(self.orientation, MAX_ORIENTATION)
            
    def update_state(self, dt):
        self.pos[0] += np.cos(self.orientation) * self.speed * dt 
        self.pos[1] += np.sin(self.orientation) * self.speed * dt

class Obstacle:
    def __init__(self, length, y_pos, x_pos):
        self.length = length
        self.y_pos = y_pos
        self.x_pos = x_pos

    def get_faces(self):
        r1 = 1

def generate_random_obstacle(last_x):
    y_pos = random.randrange(5)
    length = random.randrange(y_pos, 5)
    x_pos = last_x + 200 + random.uniform(-10, 10)
    return Obstacle(length, y_pos, x_pos)
