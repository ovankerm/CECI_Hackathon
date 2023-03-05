import pygame
from menuFinal import menu
import numpy as np
import classes as cl
import cv2
from drawer import Window
from detections import face_detection_utils, face_detector_singleIMG_multi, face_detector_singleIMG_single

import numpy as np
import classes as cl
import pygame
from drawer import Window

from classes import Car, Speedometer, Obstacle, Action, ActionType, check_collision, generate_random_obstacle
from drawer import Window
import numpy as np
from matplotlib import pyplot as plt
import pygame
import random
import asyncio
import evdev
import sys
import concurrent

from selectors import DefaultSelector, EVENT_READ
selector = DefaultSelector()

size = width, height = 1024, 512
screen = pygame.display.set_mode(size)

def get_devices():
    devs = []
    for path in evdev.list_devices():
        device = evdev.InputDevice(path)
        print(device.name)
        if "Yoke" in device.name:
            devs.append(device)
            device = devs[-1] 
            print(device.path, device.name, device.phys)
    return devs
    # device = evdev.InputDevice("/dev/input/event16")

event_types = {(3,8): "ABS_WHEEL", (3, 27): "ABS_TILT_Y", (3, 9): "ABS_GAS", (3, 10): "ABS_BRAKE",
               (1, 314): "BTN_SELECT", (1, 315): "BTN_START"}

event_types = {(3,8): "ABS_WHEEL", (1, 311): "BTN_TR", }#(3, 9): "ABS_GAS", }
rot = (8600,24200)
class TurnState:
    def __init__(self, value, tol=0.05, scaling=4.0) -> None:
        self.value = value
        self.action = ActionType.LEFT
        self.tol = tol
        self.scaling_coef = scaling
    def update(self, value) -> float:
        if abs(value - self.value)/self.value < self.tol: return 0
        if value > self.value:
            self.action = ActionType.RIGHT
        else:
            self.action = ActionType.LEFT
        num = ((180) / (rot[-1] - rot[0]))
        value_deg =  num * (value - rot[0])
        curr_value_deg = num * (self.value - rot[0])
        self.value = value
        return (curr_value_deg - value_deg) * self.scaling_coef
        

class AccelerateState:
    def __init__(self, value, tol=0.05) -> None:
        self.value = value
        self.action = ActionType.BREAK
        self.tol = tol
    def update(self, value):
        if value:
            self.action = ActionType.GAS
        else:
            self.action = ActionType.BREAK
        self.value = value 


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
    
    if(True):
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
    devs = get_devices()
    n_players = len(devs)
    print(n_players)
    turn_acc = []
    for i, dev in enumerate(devs):
        turn = TurnState(1)
        acc = AccelerateState(1)
        selector.register(dev, EVENT_READ)
        turn_acc.append((turn, acc))
    counter = -100000
    n_players = len(devs)
    # print(f"{n_players=}")
    prev_events = [[("ABS_WHEEL", 0), ("BTN_TR", True)] for _ in range(n_players)]
    while True:
        dt = clock.tick(60) * 1e-3
        events = [[] for _ in range(n_players)]
        if counter %20 == 0:
            for key, mask in selector.select():
                device = key.fileobj
                i = hash(device.name) % len(devs)
                turn, acc = turn_acc[i]
                turn_actions = []
                accelerate_actions = []
                for event in device.read():
                    code = event.code
                    type = event.type
                    value = event.value
                    type_code = (type, code)
                    event_type = event_types.get(type_code, None)
                    if event_type == None: 
                        continue
                    if event_type == "ABS_WHEEL":
                        turn_actions.append((event_type, value))
                    if event_type == "BTN_TR":
                        accelerate_actions.append((event_type, value))
                if len(turn_actions) > 0: 
                    events[i].append(turn_actions[-1])
                if len(accelerate_actions) > 0:
                    s = sum([v for t, v in accelerate_actions])
                    events[i].append(("BTN_TR", s))
                prev_events = events
        else:
            events = prev_events
        time += dt
        for i in range(n_players):
            
            for j in range(len(events[i])):
                turn, acc = turn_acc[i]
                time += dt
                event_type = events[i][j][0]
                value = events[i][j][1] 
                action = Action()
                # print(event_type)
                if event_type == "ABS_WHEEL":
                    deg = turn.update(value)
                    action.update(turn.action, deg)
                    print(i, turn.action, acc.action, deg)

                elif event_type == "BTN_TR":
                    acc.update(True)
                    action.update(acc.action, 1)
                    print(i, turn.action, acc.action)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: sys.exit(0)
                screen.fill((105, 205, 4))
                
                car = Cars[i]
                car.controller_input(dt, action)
                car.update_state(dt)
                if not car.finished:
                    if check_collision(car, obstacles[visible_obstacles[i, 0]]) :
                        car.speed *= obstacles[visible_obstacles[i, 0]].speed_multiplier
                Windows[i].draw_scene(car, obstacles, visible_obstacles[i,:], Speedometers[i], finish)
                # n_players  = len(Cars)
                # if (n_players==2):
                #     Windows[i].draw_adversary(car, Cars[(i+1)%2])
                if(car.pos[1] >= finish):
                    winner = i
                    done = True
                    print("Winner is car number %d, with a time of %.2f seconds!!!"%(i+1,time))
                    sys.exit(0)

                img = font.render("%.2f"%time, True, (0, 0, 255))
                screen.blit(img, (20, 20))
                pygame.display.flip()
        counter+=1
    # count = 0
    # while not done:
    #     dt = clock.tick(60) * 1e-3
    #     time += dt
    #     keys = pygame.key.get_pressed()
    #     check_faces = count%15 == 0
    #     if check_faces : detection_function(face_detect_ut)
    #     for i, car in enumerate(Cars):
    #         car.get_input(keys, dt, Controls[i], face_detect_ut, check_faces)
    #         car.update_state(dt)
    #         if not car.finished:
    #             if cl.check_collision(car, obstacles[visible_obstacles[i, 0]]) :
    #                 car.speed *= obstacles[visible_obstacles[i, 0]].speed_multiplier
    #         Windows[i].draw_scene(car, obstacles, visible_obstacles[i,:], Speedometers[i], finish)
    #         if(n_players == 2):
    #             Windows[i].draw_adversary(car, Cars[(i+1)%2])
    #         if(car.pos[1] >= finish):
    #             winner = i
    #             done = True
    #             return winner, time

    #     img = font.render("Time : %.2f"%time, True, (255, 255, 255))
    #     screen.blit(img, (20, 20))
        
    #     pygame.display.flip()

    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT: done = True
    #     count += 1

def end_credits(winner, time, width, height, screen):
    t = 0.0
    clock = pygame.time.Clock()
    done = False
    title = pygame.font.SysFont(pygame.font.get_default_font(), 100)
    while t < 5:
        dt = clock.tick(60) * 1e-3
        t += dt
        to_draw = pygame.transform.scale(pygame.image.load("../Images/background.jpg"), (width, height))
        screen.blit(to_draw, (0, 0))

        img = title.render("The winner is player %d\n With a time of %.2f seconds"%(winner,time), True, (255, 255, 255))
        screen.blit(img, (20, 20))

        pygame.display.flip()

        for event in pygame.event.get():  
            if event.type == pygame.QUIT: done = True
        
    run_all()

if __name__ == "__main__":
    run_all()


