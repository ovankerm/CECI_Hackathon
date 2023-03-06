import random

import pygame
import cv2
import pickle
import time
from menuFinal import pygame_utils

save_file = "pickle.dat"

def rectangle_simple(x_rel, y_rel, filling, pgu):
    rect_height = pgu.SCREEN_HEIGHT / 30
    rect_width = pgu.SCREEN_WIDTH / 4
    rect1 = pygame.Rect(0, 0, filling * rect_width, rect_height)
    rect1.bottomleft = (x_rel * pgu.SCREEN_WIDTH - rect_width / 2, y_rel * pgu.SCREEN_HEIGHT + rect_height / 2)
    rect2 = pygame.Rect(0, 0, (1 - filling) * rect_width, rect_height)
    rect2.bottomright = (x_rel * pgu.SCREEN_WIDTH + rect_width / 2, y_rel * pgu.SCREEN_HEIGHT + rect_height / 2)

    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    pygame.draw.rect(pgu.screen, GREEN, rect1)
    pygame.draw.rect(pgu.screen, RED, rect2)

class score:
    def __init__(self, duration):
        self.duration = duration
        self.date = time.time()


class leader_board:
    n_max = 5

    def __init__(self, pgu):
        self.scores = []
        self.pgu = pgu
        self.pgu.FONT = pygame.font.SysFont("arialblack", 30)
        self.padding_y = int(self.pgu.SCREEN_HEIGHT / (self.n_max + 8))

    def add_score(self, score: score):
        self.scores.append(score)
        self.sort_scores()

    def save(self):
        with open(save_file, "wb") as file:
            pickle.dump(self.scores, file)

    def load(self):
        with open(save_file, "rb") as file:
            try:
                # print("yo")
                # print(pickle.load(file))
                self.scores = pickle.load(file)
            except EOFError:
                pass

    def sort_scores(self):
        self.scores = sorted(self.scores, key=lambda score: score.duration)
        self.scores = self.scores[:self.n_max]

    def draw(self, pgu: pygame_utils):

        n = 1

        BIG_FONT = pygame.font.SysFont("arialblack", 60)
        color = (255, 215, 0)
        img = BIG_FONT.render("LEADERBOARD", True, color)
        text_rect = img.get_rect(center=(self.pgu.SCREEN_WIDTH / 2, 3 * self.padding_y))
        self.pgu.screen.blit(img, text_rect)

        for score in self.scores:
            img = self.pgu.FONT.render(f"Number {n}: {score.duration} s", True, pgu.TEXT_COLOR)
            text_rect = img.get_rect(center=(self.pgu.SCREEN_WIDTH / 2, (n + 4) * self.padding_y))
            self.pgu.screen.blit(img, text_rect)
            n += 1


def new_score_to_leaderboard(duration):
    pgu = pygame_utils(cap=None)
    l2 = leader_board(pgu)
    l2.load()
    l2.add_score(score(duration))
    l2.save()

    n = 200
    for i in range(n + 1):
        to_draw = pygame.transform.scale(pygame.image.load("Images/background.jpg"), (pgu.SCREEN_WIDTH, pgu.SCREEN_HEIGHT))
        pgu.screen.blit(to_draw, (0, 0))
        l2.draw(pgu)
        rectangle_simple(0.5, 0.9, i/n, pgu)
        pygame.display.flip()
        pygame.time.wait(50)



if __name__ == "__main__":
    new_score_to_leaderboard(57)
