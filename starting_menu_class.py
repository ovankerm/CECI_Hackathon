import time
import pygame
import cv2
import mediapipe as mp
import numpy as np
from Finger_Detection import process_img_fingers
import threading
import multiprocessing
import copy
















"""def __quick_test():
    for i in range(0, 101):
        screen.fill((0, 0, 60))

        draw_text("Choose number of player", TEXT_COLOR, 0.5, 0.4)
        rectangle(0.25, 0.65, i / 100, screen, "1 PLAYER")
        rectangle(0.75, 0.65, i / 100, screen, "2 PLAYERS")
        rectangle(0.5, 0.9, 0, screen, "EXIT")
        pygame.display.update()
        pygame.time.wait(20)"""


class multi:
    def __init__(self):
        #self.screen = screen
        self.finger_counter = multiprocessing.Array("i", 2)
        self.treshold = 30

    def run(self):
        p1 = multiprocessing.Process(target=self.img_func)
        p2 = multiprocessing.Process(target=self.menu_func)

        # menu_func(treshold)

        p1.start()
        p2.start()

        p1.join()
        p2.join()

        cap.release()
        cv2.destroyAllWindows()


    def img_func(self):
        cap = cv2.VideoCapture(0)
        prev_time = time.time()

        while True:
            success, img = cap.read()
            if not success:
                raise Exception

            process_img_fingers(img, self.finger_counter)

            # FPS counter
            cur_time = time.time()
            FPS = int(1 / (cur_time - prev_time))
            prev_time = cur_time

            cv2.putText(img, f"{FPS} FPS", (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 10)
            cv2.imshow("Image", img)
            cv2.waitKey(1)


    def menu_func(self):
        pygame.init()

        self.size = self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 1024, 768
        self.TEXT_COLOR = (255, 255, 255)
        self.FONT = pygame.font.SysFont("arialblack", 40)
        self.screen = pygame.display.set_mode(self.size)

        while True:
            one, two = self.finger_counter
            self.draw_text("Choose number of players", self.TEXT_COLOR, 0.5, 0.4)
            self.rectangle(0.25, 0.65, one / self.treshold, self.screen, "1 PLAYER")
            self.rectangle(0.75, 0.65, two / self.treshold, self.screen, "2 PLAYERS")
            self.rectangle(0.5, 0.9, 0, self.screen, "EXIT")
            pygame.display.flip()
            pygame.time.wait(50)
            if one >= self.treshold:
                print(1)
                break
            elif two >= self.treshold:
                print(2)
                break

    def draw_text(self,text, text_color, x_rel, y_rel):
        img = self.FONT.render(text, True, text_color)
        text_rect = img.get_rect(center=(x_rel * self.SCREEN_WIDTH, y_rel * self.SCREEN_HEIGHT))
        self.screen.blit(img, text_rect)

    def rectangle(self, x_rel, y_rel, filling, screen, text):
        rect_height = self.SCREEN_HEIGHT / 5
        rect_width = self.SCREEN_WIDTH / 4
        rect1 = pygame.Rect(0, 0, filling * rect_width, rect_height)
        rect1.bottomleft = (x_rel * self.SCREEN_WIDTH - rect_width / 2, y_rel * self.SCREEN_HEIGHT + rect_height / 2)
        rect2 = pygame.Rect(0, 0, (1 - filling) * rect_width, rect_height)
        rect2.bottomright = (x_rel * self.SCREEN_WIDTH + rect_width / 2, y_rel * self.SCREEN_HEIGHT + rect_height / 2)

        GREEN = (0, 255, 0)
        RED = (255, 0, 0)

        pygame.draw.rect(self.screen, GREEN, rect1)
        pygame.draw.rect(self.screen, RED, rect2)

        img = self.FONT.render(text, True, self.TEXT_COLOR)
        text_rect = img.get_rect(center=(x_rel * self.SCREEN_WIDTH, y_rel * self.SCREEN_HEIGHT))
        self.screen.blit(img, text_rect)


if __name__ == "__main__":

    m = multi()
    m.run()
