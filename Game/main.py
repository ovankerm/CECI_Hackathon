import classes as cl
from drawer import Window
import numpy as np
from matplotlib import pyplot as plt
import pygame

size = width, height = 1024, 768
screen = pygame.display.set_mode(size)
done = False
clock = pygame.time.Clock()

n_players = 1

Cars = np.empty(n_players, dtype=cl.Car)
Windows = np.empty(n_players, dtype=Window)
visible_obstacles = np.zeros((n_players, 2), dtype=int)
Speedometers = np.empty(n_players, dtype=cl.Speedometer)

Controls = [[pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN],
           [pygame.K_q, pygame.K_d, pygame.K_z, pygame.K_s]]

for i in range(n_players):
    Cars[i] = cl.Car(i)
    Cars[i].set_speed(200)
    Cars[i].set_orientation(np.radians(90))

    Windows[i] = Window(screen, width, height, 0, i * height/n_players, 1/n_players)

    Speedometers[i] = cl.Speedometer(Cars[i], width, height)


last_obstacle_z = 400
n_obstacles = 40
obstacles = np.empty(n_obstacles, dtype=cl.Obstacle)

for i in range(n_obstacles):
    o = cl.generate_random_obstacle(last_obstacle_z)
    last_obstacle_z = o.z_pos
    obstacles[i] = o

finish = obstacles[-1].z_pos + 200

time = 0
pygame.font.init()
font = pygame.font.SysFont(pygame.font.get_default_font(), 50)

while not done:
    dt = clock.tick(60) * 1e-3
    time += dt
    keys = pygame.key.get_pressed()

    screen.fill((105, 205, 4))
    
    for i, car in enumerate(Cars):
        car.get_input(keys, dt, Controls[i])
        car.update_state(dt)
        if not car.finished:
            if cl.check_collision(car, obstacles[visible_obstacles[i, 0]]) :
                car.speed *= obstacles[visible_obstacles[i, 0]].speed_multiplier
        Windows[i].draw_scene(car, obstacles, visible_obstacles[i,:], Speedometers[i], finish)
        if (n_players==2):
            Windows[i].draw_adversary(car, Cars[(i+1)%2])
        if(car.pos[1] >= finish):
            winner = i
            done = True
            print("Winner is car number %d, with a time of %.2f seconds!!!"%(i+1,time))
        

    img = font.render("%.2f"%time, True, (0, 0, 255))
    screen.blit(img, (20, 20))
    
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: done = True

