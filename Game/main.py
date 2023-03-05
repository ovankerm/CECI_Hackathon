import pygame
from game import run
if __name__ == "__main__":
    size = width, height = 1024, 512
    screen = pygame.display.set_mode(size)

    run(2, screen, width, height)




