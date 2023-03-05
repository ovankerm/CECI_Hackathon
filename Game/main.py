import classes as cl
from drawer import Window
import numpy as np
from matplotlib import pyplot as plt
import pygame
from speedometer import Speedometer



size = width, height = 1024, 768
screen = pygame.display.set_mode(size)
done = False
clock = pygame.time.Clock()

Car1 = cl.Car(0)
Car1.set_speed(200)
Car1.set_orientation(np.radians(90))

Car2 = cl.Car(1)
Car2.set_speed(200)
Car2.set_orientation(np.radians(90))

window1 = Window(screen, width, height, 0, 0, 0.5)
window2 = Window(screen, width, height, 0, height/2, 0.5)

last_obstacle_z = 400
n_obstacles = 100
obstacles = np.empty(n_obstacles, dtype=cl.Obstacle)
visible_obstacles1 = [0, 0]
visible_obstacles2 = [0, 0]

for i in range(n_obstacles):
    o = cl.generate_random_obstacle(last_obstacle_z)
    last_obstacle_z = o.z_pos
    obstacles[i] = o

time = 0
pygame.font.init()
font = pygame.font.SysFont(pygame.font.get_default_font(), 50)

while not done:
    dt = clock.tick(60) * 1e-3
    time += dt
    keys = pygame.key.get_pressed()

    Car1.get_input(keys, dt, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN)
    Car1.update_state(dt)

    Car2.get_input(keys, dt, pygame.K_q, pygame.K_d, pygame.K_z, pygame.K_s)
    Car2.update_state(dt)

    screen.fill((105, 205, 4))

    if cl.check_collision(Car1, obstacles, visible_obstacles1) :
        Car1.speed *= obstacles[visible_obstacles1[0]].speed_multiplier
    if cl.check_collision(Car2, obstacles, visible_obstacles2) :
        Car2.speed *= obstacles[visible_obstacles2[0]].speed_multiplier

    window1.draw_scene(Car1.pos, obstacles, visible_obstacles1)
    window2.draw_scene(Car2.pos, obstacles, visible_obstacles2)

    img = font.render("%.2f"%time, True, (0, 0, 255))
    screen.blit(img, (20, 20))
    
    pygame.draw.circle(screen, [255, 255, 255], [width/2 + Car1.pos[0], height/2], 10)
    speedometer = Speedometer(Car1, width, width)
    speedometer.render(screen)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: done = True

