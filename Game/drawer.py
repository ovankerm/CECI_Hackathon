import pygame
import numpy as np
import classes as cl

dark_grass = pygame.Color(0, 154, 0)
light_grass = pygame.Color(16, 200, 16)
white_rumble = pygame.Color(255, 255, 255)
red_rumble = pygame.Color(255, 0, 0)
dark_road = pygame.Color(105, 105, 105)
light_road = pygame.Color(107, 107, 107)

rumble = [white_rumble, red_rumble]
road = [light_road, dark_road]
grass = [light_grass, dark_grass]

class Camera():
    def __init__(self, x, y, z, f):
        self.x = x
        self.y = y
        self.z = z
        self.f = f

class Window():
    def __init__(self, screen, width, height, orig_x, orig_y, vert_scale):
        self.screen = screen
        self.width = width
        self.height = height
        self.camera = Camera(0, 0, 0, 100)
        self.orig_x = orig_x
        self.orig_y = orig_y
        self.vert_scale = vert_scale

    def project(self, point):
        u = self.camera.f * (point[0] - self.camera.x)/(point[2] - self.camera.z) + self.width/2 + self.orig_x
        v = (-self.camera.f * (point[1] - self.camera.y)/(point[2] - self.camera.z) + self.height/2) * self.vert_scale + self.orig_y
        return(u, v,)
    
    def draw_shape(self, points, color):
        to_draw = np.zeros((len(points), 2))
        for i, p in enumerate(points):
            to_draw[i] = self.project(p)
        pygame.draw.polygon(self.screen, color, to_draw)
        
    def draw_road(self, player_position):
        initial_index = int(player_position[1]//10) - 2
        for i in range(40):
            color = grass[(initial_index + i)%2]
            points = [[-1000, 0, 10 * (initial_index + i)], [-1000, 0, 10 * (initial_index + i) + 10], [1000, 0, 10 * (initial_index + i) + 10], [1000, 0, 10 * (initial_index + i)]]
            self.draw_shape(points, color)

            color = rumble[(initial_index + i)%2]
            points = [[-110, 0, 10 * (initial_index + i)], [-110, 0, 10 * (initial_index + i) + 10], [110, 0, 10 * (initial_index + i) + 10], [110, 0, 10 * (initial_index + i)]]
            self.draw_shape(points, color)

            color = road[(initial_index + i)%2]
            points = [[-100, 0, 10 * (initial_index + i)], [-100, 0, 10 * (initial_index + i) + 10], [100, 0, 10 * (initial_index + i) + 10], [100, 0, 10 * (initial_index + i)]]
            self.draw_shape(points, color)

    def draw_obstacle(self, obstacle : cl.Obstacle):
        for face in obstacle.get_faces(self.camera.x):
            self.draw_shape(face, obstacle.color)


    def draw_scene(self, player_position, obstacles, visible_obstacles):
        pygame.draw.rect(self.screen, (105, 205, 4), pygame.Rect(self.orig_x, self.orig_y, self.width, self.height))
        
        self.camera.x = player_position[0]
        self.camera.y = 50
        self.camera.z = player_position[1] - 30.01
        self.draw_road(player_position)

        if(obstacles[visible_obstacles[0]].z_pos < self.camera.z + 5):
            visible_obstacles[0] += 1
        elif(obstacles[visible_obstacles[1]].z_pos < player_position[1] + 400):
            visible_obstacles[1] += 1

        for i in range(visible_obstacles[0], visible_obstacles[1]):
            self.draw_obstacle(obstacles[i])







    

    