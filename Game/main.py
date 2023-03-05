import pygame
from game import run

size = width, height = 1024, 768
screen = pygame.display.set_mode(size)

run(2, screen, width, height)
