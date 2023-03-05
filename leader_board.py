import pygame
import cv2
import pickle
import time

save_file = "pickle.dat"

pygame.init()

screen = pygame.display.set_mode((400, 500))

FONT = pygame.font.SysFont("arialblack", 15)
TEXT_COLOR = (255, 255, 255)
SCREEN_WIDTH = screen.get_width()
SCREEN_HEIGHT = screen.get_height()


class score:
    def __init__(self, duration):
        self.duration = duration
        self.date = time.time()

    def take_picture(self, cap):
        _, img = cap.read()
        self.img = img

class leader_board:
    n_max = 8


    def __init__(self):
        self.scores = []

    def add_score(self, score:score):
        self.scores.append(score)

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
        self.scores = sorted(self.scores, key=lambda score: score.duration, reverse=True)
        self.scores = self.scores[:self.n_max]

    def draw(self, screen):
        padding_y = 0
        max_scores = 8 # We *could* paint every score, but it's not any good if you can't see them (because we run out of the screen).
        n = 1

        for score in self.scores:
            img = FONT.render(f"{n}: time of {score.duration} s", True, TEXT_COLOR)
            text_rect = img.get_rect(center=(SCREEN_WIDTH/2, n / self.n_max * SCREEN_HEIGHT + 10))
            screen.blit(img, text_rect)

            # screen.blit(FONT.render(str(n)+". " +str(score.duration) +": ", 1, (0,0,0)), (220,200 + padding_y))
            padding_y += 20
            n+=1


if __name__ == "__main__":
    l2 = leader_board()
    l2.load()
    print(len(l2.scores))
    for i in l2.scores:
        print(i.duration)
        print(i.date)

    while True:
        screen.fill((0, 0, 0))
        l2.draw(screen)

        pygame.display.flip()

        for i in l2.scores:
            i.duration += 1
        pygame.time.wait(500)

