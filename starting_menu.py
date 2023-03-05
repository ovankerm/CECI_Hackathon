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

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


TEXT_COLOR = (255, 255, 255)
SCREEN_WIDTH = screen.get_width()
SCREEN_HEIGHT = screen.get_height()
FONT = pygame.font.SysFont("arialblack", 40)










"""def __quick_test():
    for i in range(0, 101):
        screen.fill((0, 0, 60))

        draw_text("Choose number of player", TEXT_COLOR, 0.5, 0.4)
        rectangle(0.25, 0.65, i / 100, screen, "1 PLAYER")
        rectangle(0.75, 0.65, i / 100, screen, "2 PLAYERS")
        rectangle(0.5, 0.9, 0, screen, "EXIT")
        pygame.display.update()
        pygame.time.wait(20)"""

#while True:

def main1():
    cap = cv2.VideoCapture(0)
    #print(analyze_img(cap, treshold=50, wait_time=1))

    treshold = 30

    prev_time = time.time()  # Used for FPS calculation

    finger_counter = np.zeros(2)

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

    while cap.isOpened():
        success, img = cap.read()
        if not success:
            raise Exception

        process_img_fingers(img, finger_counter)
        # print(finger_counter)

        draw_text("Choose number of players", TEXT_COLOR, 0.5, 0.4)
        rectangle(0.25, 0.65, finger_counter[0]/treshold, screen, "1 PLAYER")
        rectangle(0.75, 0.65, finger_counter[1]/treshold, screen, "2 PLAYERS")
        rectangle(0.5, 0.9, 0, screen, "EXIT")
        pygame.display.update()
        #pygame.time.wait(20)

        # FPS counter
        cur_time = time.time()
        FPS = int(1 / (cur_time - prev_time))
        prev_time = cur_time

        if finger_counter[0] >= treshold:
            print(1)
            break
        elif finger_counter[1] >= treshold:
            print(2)
            break

        # print(FPS)

        cv2.putText(img, f"{FPS} FPS", (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 10)
        cv2.imshow("Image", img)
        cv2.waitKey(10)  # Waits wait_time ms

    cap.release()
    cv2.destroyAllWindows()


def mutliprocessing():
    #finger_counter = np.zeros(2)
    finger_counter = multiprocessing.Array("i", 2)
    #global prev_time
    #prev_time = time.time()


    # print(analyze_img(cap, treshold=50, wait_time=1))

    treshold = 30
    # Used for FPS calculation

    #p1 = multiprocessing.Process(target=img_func, args=(finger_counter,))
    #p2 = multiprocessing.Process(target=menu_func, args=(treshold,))

    menu_func(treshold)

    #p1.start()
    #p2.start()

    #p1.join()
    #p2.join()

    cap.release()
    cv2.destroyAllWindows()









def img_func(finger_counter):
    cap = cv2.VideoCapture(0)
    prev_time = time.time()

    while True:
        success, img = cap.read()
        if not success:
            raise Exception

        img = cv2.GaussianBlur(img, (15, 15), 0)
        #list_lock.acquire()
        #lst_temp = copy.deepcopy(finger_counter)
        #print("Taken by img")

        #list_lock.release()
        #print("Released by img")

        img = cv2.GaussianBlur(img, (15, 15), 0)

        process_img_fingers(img, finger_counter)
        #list_lock.acquire()
        #finger_counter = lst_temp
        #list_lock.release()

        # FPS counter
        cur_time = time.time()
        FPS = int(1 / (cur_time - prev_time))
        prev_time = cur_time

        cv2.putText(img, f"{FPS} FPS", (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 10)
        cv2.imshow("Image", img)
        cv2.waitKey(1)


def menu_func(treshold):
    finger_counter = np.zeros(2)



    while True:
        one, two = finger_counter
        draw_text("Choose number of players", TEXT_COLOR, 0.5, 0.4)
        rectangle(0.25, 0.65, one / treshold, screen, "1 PLAYER")
        rectangle(0.75, 0.65, two / treshold, screen, "2 PLAYERS")
        rectangle(0.5, 0.9, 0, screen, "EXIT")
        pygame.display.update()
        pygame.time.wait(50)
        if one >= treshold:
            print(1)
            break
        elif two >= treshold:
            print(2)
            break


if __name__ == "__main__":
    main1()
