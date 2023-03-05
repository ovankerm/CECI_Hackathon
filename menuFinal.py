import pygame
import cv2
import mediapipe as mp
import numpy as np


from menus import diplay_menu, hands_detection_utils


pygame.init()

class pygame_utils:
    def __init__(self, cap):
        self.cap = cap
        self.size = self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 1024, 768
        self.TEXT_COLOR = (255, 255, 255)
        self.FONT = pygame.font.SysFont("arialblack", 40)
        self.screen = pygame.display.set_mode(self.size)




if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    pgu = pygame_utils(cap)
    hdu = hands_detection_utils(cap)
    start_texts = ["1 PLAYER", "2 PLAYERS", "EXIT"]
    one_player_texts = ["CHRONO", "RANDOM", "BACK"]
    result = 0
    while True:
        start = diplay_menu(start_texts, pgu, hdu)
        if start == 1:
            one = diplay_menu(one_player_texts, pgu, hdu)
            if one == 1:
                print("CHRONO")
                result = 11
                break
            elif one == 2:
                print("RANDOM")
                result = 12
                break
            elif one==0:
                continue
        elif start == 2:
            print("TWO PLAYER GAME")
            result = 2
            break
        else:
            print("END GAME")
            break
