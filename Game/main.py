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



time = 0
size = width, height = 1024, 512
screen = pygame.display.set_mode(size)
done = False
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont(pygame.font.get_default_font(), 50)

from selectors import DefaultSelector, EVENT_READ
selector = DefaultSelector()

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
    def __init__(self, value, tol=0.01, scaling=4.0) -> None:
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
    def __init__(self, value, tol=0.01) -> None:
        self.value = value
        self.action = ActionType.BREAK
        self.tol = tol
    def update(self, value):
        if value:
            self.action = ActionType.GAS
        else:
            self.action = ActionType.BREAK
        self.value = value 

        # if value == 0: self.action = ActionType.BREAK; return
        # if abs(value - self.value)/self.value < self.tol: return
        # if value < self.value:
        #     self.action = ActionType.BREAK
        # else:
        #     self.action = ActionType.GAS
        # self.value = value


def print_events(devs, turn_acc, Cars: np.ndarray[Car], Windows: np.ndarray, Speedometers: np.ndarray, finish, obstacles, visible_obstacles):
                    #clock, font, screen):
    global time
    counter = -100000
    n_players = len(devs)
    prev_events = [[] for _ in range(n_players)]
    while True:
        dt = clock.tick(60) * 1e-3
        events = [[] for _ in range(n_players)]
        if counter % 5 == 0:
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
        global time
        time += dt
        for i in range(n_players):
            for j in range(len(events[i])):
                turn, acc = turn_acc[i]
                time += dt
                event_type = events[i][j][0]
                value = events[i][j][1] 
                action = Action()
                print(event_type)
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
                n_players  = len(Cars)
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

def main():

    devs = get_devices()
    n_players = len(devs)
    print(n_players)
    Cars = np.empty(n_players, dtype=Car)
    Windows = np.empty(n_players, dtype=Window)
    visible_obstacles = np.zeros((n_players, 2), dtype=int)
    Speedometers = np.empty(n_players, dtype=Speedometer)

    #Controls = [[pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN],
    #        [pygame.K_q, pygame.K_d, pygame.K_z, pygame.K_s]]

    for i in range(n_players):
        Cars[i] = Car(i)
        Cars[i].set_speed(200)
        Cars[i].set_orientation(np.radians(90))

        Windows[i] = Window(screen, width, height, 0, i * height/(n_players*2), 1/n_players)

        Speedometers[i] = Speedometer(Cars[i], width, height)
    last_obstacle_z = 4000
    n_obstacles = 5
    obstacles = np.empty(n_obstacles, dtype=Obstacle)

    for i in range(n_obstacles):
        o = generate_random_obstacle(last_obstacle_z)
        last_obstacle_z = o.z_pos
        obstacles[i] = o

    finish = obstacles[-1].z_pos + 200
    turn_acc = []
    for i, dev in enumerate(devs):
        turn = TurnState(1)
        acc = AccelerateState(1)
        selector.register(dev, EVENT_READ)
        turn_acc.append((turn, acc))
        # obj[device] = (turn, acc)
    print_events(devs, turn_acc, Cars, Windows, Speedometers, finish, obstacles, visible_obstacles)

if __name__ == "__main__":
    main()




# while not done:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT: done = True
# ======================================================================

# size = width, height = 1024, 768
# screen = pygame.display.set_mode(size)
# done = False
# clock = pygame.time.Clock()

# n_players = 2

# Cars = np.empty(n_players, dtype=cl.Car)
# Windows = np.empty(n_players, dtype=Window)
# visible_obstacles = np.zeros((n_players, 2), dtype=int)
# Speedometers = np.empty(n_players, dtype=cl.Speedometer)

# Controls = [[pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN],
#            [pygame.K_q, pygame.K_d, pygame.K_z, pygame.K_s]]

# for i in range(n_players):
#     Cars[i] = cl.Car(i)
#     Cars[i].set_speed(200)
#     Cars[i].set_orientation(np.radians(90))

#     Windows[i] = Window(screen, width, height, 0, i * height/n_players, 1/n_players)

#     Speedometers[i] = cl.Speedometer(Cars[i], width, height)


# last_obstacle_z = 400
# n_obstacles = 5
# obstacles = np.empty(n_obstacles, dtype=cl.Obstacle)

# for i in range(n_obstacles):
#     o = cl.generate_random_obstacle(last_obstacle_z)
#     last_obstacle_z = o.z_pos
#     obstacles[i] = o

# finish = obstacles[-1].z_pos + 200

# time = 0
# pygame.font.init()
# font = pygame.font.SysFont(pygame.font.get_default_font(), 50)

# while not done:
#     dt = clock.tick(60) * 1e-3
#     time += dt
#     keys = pygame.key.get_pressed()

#     screen.fill((105, 205, 4))
    
#     for i, car in enumerate(Cars):
#         car.get_input(keys, dt, Controls[i])
#         car.update_state(dt)
#         if not car.finished:
#             if cl.check_collision(car, obstacles[visible_obstacles[i, 0]]) :
#                 car.speed *= obstacles[visible_obstacles[i, 0]].speed_multiplier
#         Windows[i].draw_scene(car, obstacles, visible_obstacles[i,:], Speedometers[i], finish)
#         if (n_players==2):
#             Windows[i].draw_adversary(car, Cars[(i+1)%2])
#         if(car.pos[1] >= finish):
#             winner = i
#             done = True
#             print("Winner is car number %d, with a time of %.2f seconds!!!"%(i+1,time))
        

#     img = font.render("%.2f"%time, True, (0, 0, 255))
#     screen.blit(img, (20, 20))
    
#     pygame.display.flip()

    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT: done = True

