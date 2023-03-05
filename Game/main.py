import pygame
from menuFinal import menu
import numpy as np
import classes as cl
import cv2
from drawer import Window
from detections import face_detection_utils, face_detector_singleIMG_multi, face_detector_singleIMG_single

size = width, height = 1024, 768
screen = pygame.display.set_mode(size)

def run_all():
    game_mode = menu()
    if(game_mode == 0): return
    winner, time = run(game_mode, screen, width, height)
    end_credits(winner, time, width, height, screen)


def run(return_value, screen, width, height):
    if(return_value == 2):
        n_players = 2
        chrono = False
        random = True
    elif(return_value == 11):
        n_players = 1
        chrono = True
        random = False  
    elif(return_value == 12):
        n_players = 1
        chrono = False
        random = True

    clock = pygame.time.Clock()
    cap = cv2.VideoCapture(0)

    Cars = np.empty(n_players, dtype=cl.Car)
    Windows = np.empty(n_players, dtype=Window)
    visible_obstacles = np.zeros((n_players, 2), dtype=int)
    Speedometers = np.empty(n_players, dtype=cl.Speedometer)

    face_detect_ut = face_detection_utils(cap)
    if(n_players == 1):
        detection_function = face_detector_singleIMG_single
    else:
        detection_function = face_detector_singleIMG_multi

    Controls = [[pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_SPACE],
            [pygame.K_q, pygame.K_d, pygame.K_z, pygame.K_s, pygame.K_TAB]]

    for i in range(n_players):
        Cars[i] = cl.Car(i)
        Cars[i].set_speed(200)
        Cars[i].set_orientation(np.radians(90))

        Windows[i] = Window(screen, width, height, 0, i * height/n_players, 1/n_players)

        Speedometers[i] = cl.Speedometer(Cars[i], width, height)
    
    if(random):
        last_obstacle_z = 400
        n_obstacles = 40
        obstacles = np.empty(n_obstacles, dtype=cl.Obstacle)

        for i in range(n_obstacles):
            o = cl.generate_random_obstacle(last_obstacle_z)
            last_obstacle_z = o.z_pos
            obstacles[i] = o

        finish = last_obstacle_z + 200

    time = 0

    pygame.font.init()
    font = pygame.font.SysFont(pygame.font.get_default_font(), 50)

    title = pygame.font.SysFont(pygame.font.get_default_font(), 200)

    done = False
    t = 0.0
    while(t < 3 and not done):
        for i, car in enumerate(Cars):
            Windows[i].draw_scene(car, obstacles, visible_obstacles[i,:], Speedometers[i], finish)
        
        img = title.render("%d"%(3 - int(t)%3), True, (255, 255, 255))
        screen.blit(img, (width/2 - 40, height/2 - 200))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: done = True
        t += clock.tick(60) * 1e-3

    count = 0
    while not done:
        dt = clock.tick(60) * 1e-3
        time += dt
        keys = pygame.key.get_pressed()
        check_faces = count%15 == 0
        if check_faces : detection_function(face_detect_ut)
        for i, car in enumerate(Cars):
            car.get_input(keys, dt, Controls[i], face_detect_ut, check_faces)
            car.update_state(dt)
            if not car.finished:
                if cl.check_collision(car, obstacles[visible_obstacles[i, 0]]) :
                    car.speed *= obstacles[visible_obstacles[i, 0]].speed_multiplier
            Windows[i].draw_scene(car, obstacles, visible_obstacles[i,:], Speedometers[i], finish)
            if(n_players == 2):
                Windows[i].draw_adversary(car, Cars[(i+1)%2])
            if(car.pos[1] >= finish):
                winner = i
                done = True
                return winner, time

        img = font.render("Time : %.2f"%time, True, (255, 255, 255))
        screen.blit(img, (20, 20))
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: done = True
        count += 1

def end_credits(winner, time, width, height, screen):
    t = 0.0
    clock = pygame.time.Clock()
    done = False
    title = pygame.font.SysFont(pygame.font.get_default_font(), 100)
    while t < 5:
        dt = clock.tick(60) * 1e-3
        t += dt
        to_draw = pygame.transform.scale(pygame.image.load("Images/background.jpg"), (width, height))
        screen.blit(to_draw, (0, 0))

        img = title.render("The winner is player %d\n With a time of %.2f seconds"%(winner,time), True, (255, 255, 255))
        screen.blit(img, (20, 20))

        pygame.display.flip()

        for event in pygame.event.get():  
            if event.type == pygame.QUIT: done = True
        
    run_all()

if __name__ == "__main__":
    run_all()


