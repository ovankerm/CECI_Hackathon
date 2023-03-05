import classes as cl
from drawer import Window
import numpy as np
from matplotlib import pyplot as plt
import pygame



size = width, height = 1024, 768
screen = pygame.display.set_mode(size)
done = False
clock = pygame.time.Clock()
Car1 = cl.Car(1,width)
Car1.set_speed(200)
Car1.set_orientation(np.radians(90))

window = Window(screen, width, height)

last_obstacle_z = 400
n_obstacles = 100
obstacles = np.empty(n_obstacles, dtype=cl.Obstacle)
visible_obstacles = [0, 0]

for i in range(n_obstacles):
    o = cl.generate_random_obstacle(last_obstacle_z)
    last_obstacle_z = o.z_pos
    obstacles[i] = o

time = 0
pygame.font.init()
font = pygame.font.SysFont(pygame.font.get_default_font(), 50)

speedometer = cl.Speedometer(Car1, width, height)

while not done:
    dt = clock.tick(60) * 1e-3
    time += dt

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        Car1.turn(1)
        Car1.orientation_bool = 1
    elif keys[pygame.K_RIGHT]:
        Car1.turn(-1)
        Car1.orientation_bool = -1
    else:
        Car1.turn(-0.05 * np.rad2deg(Car1.orientation - np.pi/2))
        Car1.orientation_bool = 0

    if keys[pygame.K_UP]:
        Car1.accelerate(10, dt)
    elif keys[pygame.K_DOWN]:
        Car1.accelerate(-50, dt)

    if(abs(Car1.pos[0] > 100)):
       Car1.accelerate(-20, dt)

    Car1.update_state(dt)

    screen.fill((105, 205, 4))

    img = font.render("%.2f"%time, True, (0, 0, 255))
    screen.blit(img, (20, 20))

    if cl.check_collision(Car1, obstacles, visible_obstacles) :
        Car1.speed *= obstacles[visible_obstacles[0]].speed_multiplier
    window.draw_scene(Car1.pos, obstacles, visible_obstacles, speedometer, Car1)
    
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: done = True

