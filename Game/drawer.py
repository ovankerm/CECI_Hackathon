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
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.camera = Camera(0, 0, 0, 100)
    
    def project(self, point):
        u = self.camera.f * (point[0] - self.camera.x)/(point[2] - self.camera.z) + self.width/2
        v = -self.camera.f * (point[1] - self.camera.y)/(point[2] - self.camera.z) + self.height/2
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
    
    def draw_speedometer(self, speedometer : cl.Speedometer):
        self.screen.blit(speedometer.image, (speedometer.screen_x, speedometer.screen_y))

        angle = np.pi * speedometer.car.speed / speedometer.car.top_speed
        tip_x = speedometer.needle_x - speedometer.needle_length * np.cos(angle)
        tip_y = speedometer.needle_y - speedometer.needle_length * np.sin(angle)
        pygame.draw.line(self.screen, speedometer.needle_color, (speedometer.needle_x, speedometer.needle_y), (tip_x, tip_y), 3)

    def draw_scene(self, player_position, obstacles, visible_obstacles, speedometer, car):
        self.camera.x = player_position[0]
        self.camera.y = 100
        self.camera.z = player_position[1] - 30.01
        self.draw_road(player_position)

        if(obstacles[visible_obstacles[0]].z_pos < self.camera.z + 5):
            visible_obstacles[0] += 1
        elif(obstacles[visible_obstacles[1]].z_pos < player_position[1] + 500):
            visible_obstacles[1] += 1

        for i in range(visible_obstacles[0], visible_obstacles[1]):
            self.draw_obstacle(obstacles[i])
        
        self.draw_speedometer(speedometer)
        self.draw_car(car)

    def draw_car(self, car: cl.Car):
        bottom_right = self.project((car.pos[0] + car.width/2, 0, car.pos[1]))
        top_left = self.project((car.pos[0] - car.width/2, car.width*162/293, car.pos[1]))

        # self.length = (int) (self.width*645/293)
        # self.height = (int) (self.width*162/293)
        # self.side = pygame.transform.smoothscale(pygame.image.load("Images/side_gt40_{}.png".format(1)), (self.length, self.height)).convert_alpha()
        car.back = pygame.transform.rotate(pygame.transform.smoothscale(pygame.image.load("Images/back_gt40_{}.png".format(1)), (bottom_right[0] - top_left[0], bottom_right[1] - top_left[1])), 5 * car.orientation_bool).convert_alpha()

        self.screen.blit(car.back, top_left)
        #self.screen.blit(car.side, (self.width/2, self.height-150))


        
        







    

    