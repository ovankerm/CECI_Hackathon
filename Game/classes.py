import numpy as np
import pygame as pg

MAX_ORIENTATION = 10

class Car:
    def __init__(self, i, screen_width, screen_height):
        self.pos = np.zeros(2)
        self.speed = 0
        self.orientation = 0
        self.top_speed = 100
        car_width = screen_width / 4
        car_length = (int) (car_width*645/293)
        car_height = (int) (car_width*162/293)
        print(car_length, car_height)
        self.side =  pg.transform.smoothscale(pg.image.load("Images/side_gt40_{}.png".format(i)), (car_length, car_height)).convert_alpha()
        self.back = pg.transform.smoothscale(pg.image.load("Images/back_gt40_{}.png".format(i)), (car_width, car_height)).convert_alpha()
        print(type(self.side))
        sidedata = pg.surfarray.array3d(self.side)
        backdata = pg.surfarray.array3d(self.back)

        self.screen_x = screen_width - (car_width)
        self.screen_y = screen_height - (car_height)

        print(sidedata.shape)
        print(sidedata[30,15,:])
        print(backdata.shape)


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

    def render(self, screen):
        print(self.screen_x-200, self.screen_y-200)
        screen.blit(self.back, (self.screen_x-100, self.screen_y-100))
        screen.blit(self.side, (self.screen_x-150, self.screen_y-150))

        # angle = self.orientation
        # tip_x = self.needle_x - self.needle_length * cos(angle)
        # tip_y = self.needle_y - self.needle_length * sin(angle)
        # pg.draw.line(screen, self.needle_color, (self.needle_x, self.needle_y), (tip_x, tip_y), 3)
    
    