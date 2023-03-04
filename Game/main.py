from classes import Car
from drawer import Window
import numpy as np
from matplotlib import pyplot as plt
import pygame



size = width, height = 1024, 768
screen = pygame.display.set_mode(size)
done = False
clock = pygame.time.Clock()
Car1 = Car()
Car1.set_speed(100)
Car1.set_orientation(np.radians(90))

window = Window(screen, width, height)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: done = True

    dt = clock.tick(60) * 1e-3

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        Car1.turn(1)
    elif keys[pygame.K_RIGHT]:
        Car1.turn(-1)
    else:
        Car1.turn(-0.05 * np.rad2deg(Car1.orientation - np.pi/2))

    if(abs(Car1.pos[0] > 100)):
       Car1.accelerate(-10, dt)

    Car1.update_state(dt)

    screen.fill((105, 205, 4))
    window.draw(Car1.pos)
    
    pygame.display.flip()

