import cv2
import time
import pygame
import numpy as np
from detections import process_single_img_fingers, hands_detection_utils

def draw_text(text, text_color, x_rel, y_rel, pgu):
    img = pgu.FONT.render(text, True, text_color)
    text_rect = img.get_rect(center=(x_rel * pgu.SCREEN_WIDTH, y_rel * pgu.SCREEN_HEIGHT))
    pgu.screen.blit(img, text_rect)


def rectangle(x_rel, y_rel, filling, text, pgu):
    rect_height = pgu.SCREEN_HEIGHT / 5
    rect_width = pgu.SCREEN_WIDTH / 4
    rect1 = pygame.Rect(0, 0, filling * rect_width, rect_height)
    rect1.bottomleft = (x_rel * pgu.SCREEN_WIDTH - rect_width / 2, y_rel * pgu.SCREEN_HEIGHT + rect_height / 2)
    rect2 = pygame.Rect(0, 0, (1 - filling) * rect_width, rect_height)
    rect2.bottomright = (x_rel * pgu.SCREEN_WIDTH + rect_width / 2, y_rel * pgu.SCREEN_HEIGHT + rect_height / 2)

    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    pygame.draw.rect(pgu.screen, GREEN, rect1)
    pygame.draw.rect(pgu.screen, RED, rect2)

    img = pgu.FONT.render(text, True, pgu.TEXT_COLOR)
    text_rect = img.get_rect(center=(x_rel * pgu.SCREEN_WIDTH, y_rel * pgu.SCREEN_HEIGHT))
    pgu.screen.blit(img, text_rect)



def diplay_menu(texts, pgu, hdu:hands_detection_utils):
    hdu.counter = [0,0,0]
    while pgu.cap.isOpened():

        process_single_img_fingers(hdu)

        pgu.screen.fill((0, 0, 60))

        draw_text("Choose number of players", pgu.TEXT_COLOR, 0.5, 0.4, pgu)
        rectangle(0.25, 0.65, hdu.counter[0]/hdu.treshold, texts[0], pgu)
        rectangle(0.75, 0.65, hdu.counter[1]/hdu.treshold, texts[1], pgu)
        rectangle(0.5, 0.9, hdu.counter[2]/hdu.treshold, texts[2], pgu)
        pygame.display.update()

        if hdu.counter[0] >= hdu.treshold:
            # One player validated
            return 1
        elif hdu.counter[1] >= hdu.treshold:
            # Two players validated
            return 2
        elif hdu.counter[2] >= hdu.treshold:
            # Exit menu
            return 0

    cap.release()
    cv2.destroyAllWindows()