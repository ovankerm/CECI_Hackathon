import pygame
import numpy as np

dark_grass = pygame.Color(0, 154, 0)
light_grass = pygame.Color(16, 200, 16)
white_rumble = pygame.Color(255, 255, 255)
black_rumble = pygame.Color(0, 0, 0)
dark_road = pygame.Color(105, 105, 105)
light_road = pygame.Color(107, 107, 107)

rumble = [white_rumble, black_rumble]
road = [light_road, dark_road]
grass = [light_grass, dark_grass]

class Camera():
    def __init__(self, x, y, z, f):
        self.x = x
        self.y = y
        self.z = z
        self.f = f

class Window():
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.camera = Camera(0, 0, 0, 100)

    def project(self, point):
        u = self.camera.f * (point[0] - self.camera.x)/(point[2] - self.camera.z) + self.width/2
        v = -self.camera.f * (point[1] - self.camera.y)/(point[2] - self.camera.z) + self.height/2
        return(u, v,)
    
    def draw_rectangle(self, points, color):
        to_draw = np.zeros((4, 2))
        for i, p in enumerate(points):
            to_draw[i] = self.project(p)
        pygame.draw.polygon(self.screen, color, to_draw)
        
    def draw(self, player_position):
        initial_index = int(player_position[1]//10) - 2
        self.camera.x = player_position[0]
        self.camera.y = 50
        self.camera.z = player_position[1] - 30.01
        for i in range(20):
            color = grass[(initial_index + i)%2]
            points = [[-1000, 0, 10 * (initial_index + i)], [-1000, 0, 10 * (initial_index + i) + 10], [1000, 0, 10 * (initial_index + i) + 10], [1000, 0, 10 * (initial_index + i)]]
            self.draw_rectangle(points, color)

            color = rumble[(initial_index + i)%2]
            points = [[-110, 0, 10 * (initial_index + i)], [-110, 0, 10 * (initial_index + i) + 10], [110, 0, 10 * (initial_index + i) + 10], [110, 0, 10 * (initial_index + i)]]
            self.draw_rectangle(points, color)

            color = road[(initial_index + i)%2]
            points = [[-100, 0, 10 * (initial_index + i)], [-100, 0, 10 * (initial_index + i) + 10], [100, 0, 10 * (initial_index + i) + 10], [100, 0, 10 * (initial_index + i)]]
            self.draw_rectangle(points, color)






    

    