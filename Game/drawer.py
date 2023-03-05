import pygame
import numpy as np
import classes as cl

dark_grass = pygame.Color(231,196,150)
light_grass = pygame.Color(236,204,162)
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
        for i in range(50):
            color = grass[(initial_index + i)%2]
            points = [[-2000, 0, 10 * (initial_index + i)], [-2000, 0, 10 * (initial_index + i) + 10], [2000, 0, 10 * (initial_index + i) + 10], [2000, 0, 10 * (initial_index + i)]]
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
    
    def draw_speedometer(self, speedometer : cl.Speedometer):
        self.screen.blit(speedometer.image, (speedometer.screen_x, speedometer.screen_y))

        angle = np.pi * speedometer.car.speed / speedometer.car.top_speed -0.6
        tip_x = speedometer.needle_x - speedometer.needle_length * np.cos(angle)
        tip_y = speedometer.needle_y - speedometer.needle_length * np.sin(angle)
        pygame.draw.line(self.screen, speedometer.needle_color, (speedometer.needle_x, speedometer.needle_y), (tip_x, tip_y), 2)

    def draw_adversary(self, car_self : cl.Car, car_adversaire : cl.Car):
        if(car_self.pos[1] < car_adversaire.pos[1] + 30 and car_adversaire.pos[1]-car_self.pos[1] < 500):
            self.draw_car(car_adversaire, True)


    def draw_finish(self, z_pos):
        self.draw_shape([[-100, 80, z_pos], [100, 80, z_pos], [100, 100, z_pos], [-100, 100, z_pos]], (111, 76, 15))
        self.draw_shape([[-100, 0, z_pos], [-100, 100, z_pos], [-110, 100, z_pos], [-110, 0, z_pos]], (111, 76, 15))
        self.draw_shape([[100, 0, z_pos], [110, 0, z_pos], [110, 100, z_pos], [100, 100, z_pos]], (111, 76, 15))

    def draw_background(self):
        to_draw = pygame.transform.scale(pygame.image.load("Images/background.jpg"), (self.width, self.width/2))
        self.screen.blit(to_draw, (self.orig_x, self.orig_y))

    def draw_scene(self, car, obstacles, visible_obstacles, speedometer, finish):
        self.draw_background()
        self.camera.x = car.pos[0]
        self.camera.y = 100
        self.camera.z = car.pos[1] - 30.01
        self.draw_road(car.pos)

        if(visible_obstacles[0] < len(obstacles)):
            if(obstacles[visible_obstacles[0]].z_pos < self.camera.z + 5):
                visible_obstacles[0] += 1

        if(visible_obstacles[1] < len(obstacles)):
            if obstacles[visible_obstacles[1]].z_pos < car.pos[1] + 500 :
                visible_obstacles[1] += 1

        if(visible_obstacles[0] == len(obstacles)): car.finished = True


        for i in range(visible_obstacles[0], min(visible_obstacles[1], len(obstacles))):
            self.draw_obstacle(obstacles[i])

        if(finish - car.pos[1] < 500):
            self.draw_finish(finish)
        
        self.draw_speedometer(speedometer)
        self.draw_car(car, False)

    def draw_car(self, car: cl.Car, adversary : bool):
        bottom_right = self.project((car.pos[0] + car.width/2, car.pos[2], car.pos[1]))
        top_left = self.project((car.pos[0] - car.width/2, car.pos[2] + car.width*car.aspect_ratio/self.vert_scale, car.pos[1]))
        if not adversary:
            to_draw = pygame.transform.rotate(pygame.transform.smoothscale(car.my_image, (bottom_right[0] - top_left[0], bottom_right[1] - top_left[1])), 5 * car.orientation_bool).convert_alpha()
        else:
            to_draw = pygame.transform.rotate(pygame.transform.smoothscale(car.for_adversary, (bottom_right[0] - top_left[0], bottom_right[1] - top_left[1])), 5 * car.orientation_bool).convert_alpha()
            to_draw.set_alpha(128)
        self.screen.blit(to_draw, top_left)


        
        







    

    