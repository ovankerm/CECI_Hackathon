import pygame
import os
import sys

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

TEXT_COLOR = (255, 255, 255)
SCREEN_WIDTH = screen.get_width()
SCREEN_HEIGHT = screen.get_height()
FONT = pygame.font.SysFont("arialblack", 40)


for i in range(0, 1000):
    screen.fill((0, 0, 60))

    image = pygame.transform.smoothscale(pygame.image.load(get_resource_path("car_side.png")), (30, 200)).convert_alpha()
    screen.blit(image, (0.5*SCREEN_WIDTH, 0.5 * SCREEN_HEIGHT))
    pygame.display.update()
    pygame.time.wait(20)