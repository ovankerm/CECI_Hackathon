from classes import Car
import scene as sc
import numpy as np
from matplotlib import pyplot as plt
import pygame

size = width, height = 480, 480

screen = pygame.display.set_mode(size)

done = False
clock = pygame.time.Clock()

Car1 = Car()
Car1.set_speed(500)
Car1.set_orientation(-np.radians(90))

window = sc.GameWindow(screen, clock)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: done = True

    dt = clock.tick(60) * 1e-3
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        Car1.turn(-0.5)
    elif keys[pygame.K_RIGHT]:
        Car1.turn(0.5)
    else:
        Car1.turn(-0.05 * np.rad2deg(Car1.orientation + np.pi/2))

    window.draw_scene(dt, Car1.pos, Car1.speed)

    # if(abs(Car1.pos[0] > 10)):
    #    Car1.accelerate(-10, dt)

    Car1.update_state(dt)
    
    pygame.display.flip()

