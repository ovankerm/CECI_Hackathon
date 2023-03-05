import numpy as np
import random
import pygame as pg

MIN_ORIENTATION = np.radians(60)
MAX_ORIENTATION = np.radians(120)

average_obstacle_distance = 200

class Car:
    def __init__(self, i, screen_width):
        self.pos = np.zeros(2)
        self.speed = 0
        self.orientation = 0
        self.top_speed = 300
        self.orientation_bool = 0
        self.width = 200 / 5.1
        self.length = (int) (self.width*645/293)
        self.height = (int) (self.width*162/293)
        self.side = pg.transform.smoothscale(pg.image.load("Images/side_gt40_{}.png".format(i)), (self.length, self.height)).convert_alpha()
        self.back = pg.transform.smoothscale(pg.image.load("Images/back_gt40_{}.png".format(i)), (self.width, self.height)).convert_alpha()


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
        if angle < 0:
            self.orientation = max(self.orientation, MIN_ORIENTATION)
        elif angle > 0:
            self.orientation = min(self.orientation, MAX_ORIENTATION)
        
            
    def update_state(self, dt):
        self.pos[0] += np.cos(self.orientation) * self.speed * dt 
        self.pos[1] += np.sin(self.orientation) * self.speed * dt

class Speedometer:
    def __init__(self, car, screen_width, screen_height):
        self.car = car

        speedometer_width = screen_width / 4
        speedometer_height = screen_height / 4

        self.image = pg.transform.smoothscale(pg.image.load("Images/speedometer.png"), (speedometer_width, speedometer_height)).convert_alpha()

        self.screen_x = screen_width - (speedometer_width)
        self.screen_y = screen_height - (speedometer_height)

        self.needle_x = screen_width - (speedometer_width / 2)
        self.needle_y = screen_height - 20
        self.needle_length = speedometer_height / 1.7
        self.needle_color = pg.Color("#1f51ff")



def check_collision(car : Car, obstacles, visible_obstacles):
    for i in range(visible_obstacles[0], visible_obstacles[1]):
        if(not obstacles[i].collided and abs(car.pos[0] - obstacles[i].middle_x) < obstacles[i].length * 20 and abs(car.pos[1] - obstacles[i].z_pos) < 10):
            obstacles[i].collided = True
            return True
    return False

class Obstacle:
    def __init__(self, length, z_pos, x_pos, speed_multiplier, color):
        self.length = length
        self.z_pos = z_pos
        self.x_pos = x_pos
        self.middle_x = -100 + (x_pos + length/2) * 40
        self.vertices = [[-100 + x_pos * 40, 0, z_pos - 5],
                         [-100 + x_pos * 40, 0, z_pos + 5],
                         [-100 + (x_pos + length) * 40, 0, z_pos + 5],
                         [-100 + (x_pos + length) * 40, 0, z_pos - 5],
                         [-100 + x_pos * 40, 1, z_pos - 5],
                         [-100 + x_pos * 40, 1, z_pos + 5],
                         [-100 + (x_pos + length) * 40, 1, z_pos + 5],
                         [-100 + (x_pos + length) * 40, 1, z_pos - 5]]
        self.collided = False
        self.speed_multiplier = speed_multiplier
        self.color = color
        
    def get_faces(self, camera_x):
        if(camera_x < self.middle_x):
            return [[self.vertices[0], self.vertices[3], self.vertices[7], self.vertices[4]],
                    [self.vertices[0], self.vertices[4], self.vertices[5], self.vertices[1]],
                    [self.vertices[4], self.vertices[7], self.vertices[6], self.vertices[5]]]
        else :
            return [[self.vertices[0], self.vertices[3], self.vertices[7], self.vertices[4]],
                    [self.vertices[3], self.vertices[2], self.vertices[6], self.vertices[7]],
                    [self.vertices[4], self.vertices[7], self.vertices[6], self.vertices[5]]]

def generate_random_obstacle(last_z):
    x_pos = random.randrange(5)
    z_pos = last_z + 200 + random.uniform(-30, 30)
    boost = 6 * random.random() < 1
    if(boost):
        return Obstacle(1, z_pos, x_pos, 1.5, (255, 0, 255))
    length = random.randrange(1, 6 - x_pos)
    return Obstacle(length, z_pos, x_pos, 0.5, (0, 0, 0))

