import time
import pygame
import cv2
import mediapipe as mp
import numpy as np
from Finger_Detection import process_img_fingers
import threading
import multiprocessing
import copy



pygame.init()

size = SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
TEXT_COLOR = (255, 255, 255)
FONT = pygame.font.SysFont("arialblack", 40)

screen = pygame.display.set_mode(size)


def draw_text(text, text_color, x_rel, y_rel):
    img = FONT.render(text, True, text_color)
    text_rect = img.get_rect(center=(x_rel * SCREEN_WIDTH, y_rel * SCREEN_HEIGHT))
    screen.blit(img, text_rect)


def rectangle(x_rel, y_rel, filling, screen, text):
    rect_height = SCREEN_HEIGHT / 5
    rect_width = SCREEN_WIDTH / 4
    rect1 = pygame.Rect(0, 0, filling * rect_width, rect_height)
    rect1.bottomleft = (x_rel * SCREEN_WIDTH - rect_width / 2, y_rel * SCREEN_HEIGHT + rect_height / 2)
    rect2 = pygame.Rect(0, 0, (1 - filling) * rect_width, rect_height)
    rect2.bottomright = (x_rel * SCREEN_WIDTH + rect_width / 2, y_rel * SCREEN_HEIGHT + rect_height / 2)

    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    pygame.draw.rect(screen, GREEN, rect1)
    pygame.draw.rect(screen, RED, rect2)

    img = FONT.render(text, True, TEXT_COLOR)
    text_rect = img.get_rect(center=(x_rel * SCREEN_WIDTH, y_rel * SCREEN_HEIGHT))
    screen.blit(img, text_rect)







"""def __quick_test():
    for i in range(0, 101):
        screen.fill((0, 0, 60))

        draw_text("Choose number of player", TEXT_COLOR, 0.5, 0.4)
        rectangle(0.25, 0.65, i / 100, screen, "1 PLAYER")
        rectangle(0.75, 0.65, i / 100, screen, "2 PLAYERS")
        rectangle(0.5, 0.9, 0, screen, "EXIT")
        pygame.display.update()
        pygame.time.wait(20)"""


def menus(cap, texts):
    treshold = 40

    prev_time = time.time()  # Used for FPS calculation

    finger_counter = np.zeros(3)

    while cap.isOpened():
        success, img = cap.read()
        if not success:
            raise Exception

        process_img_fingers(img, finger_counter)
        # print(finger_counter)

        screen.fill((0, 0, 60))

        draw_text("Choose number of players", TEXT_COLOR, 0.5, 0.4)
        rectangle(0.25, 0.65, finger_counter[0]/treshold, screen, texts[0])
        rectangle(0.75, 0.65, finger_counter[1]/treshold, screen, texts[1])
        rectangle(0.5, 0.9, finger_counter[2]/treshold, screen, texts[2])
        pygame.display.update()
        #pygame.time.wait(20)

        # FPS counter
        cur_time = time.time()
        FPS = int(1 / (cur_time - prev_time))
        prev_time = cur_time

        if finger_counter[0] >= treshold:
            # One player validated
            return 1
        elif finger_counter[1] >= treshold:
            # Two players validated
            return 2
        elif finger_counter[2] >= treshold:
            # Exit menu
            return 0

        # print(FPS)

        cv2.putText(img, f"{FPS} FPS", (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 10)
        cv2.imshow("Image", img)
        cv2.waitKey(10)  # Waits wait_time ms

    cap.release()
    cv2.destroyAllWindows()

def menu_one_player():
    pass


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    start_texts = ["1 PLAYER", "2 PLAYERS", "EXIT"]
    one_player_texts = ["CHRONO", "RANDOM MODE", "BACK"]
    result = 0
    while True:
        start = menus(cap, start_texts)
        if start == 1:
            one = menus(cap, one_player_texts)
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
