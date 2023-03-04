from classes import Car
from drawer import Window
import numpy as np
from matplotlib import pyplot as plt
import pygame

import asyncio
import evdev
from enum import Enum
import sys

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
class Action(Enum):
    LEFT =  0
    RIGHT = 1
    GAS = 2
    BREAK = 3
    PAUSE = 4

rot = (8600,24200)
class TurnState:
    def __init__(self, value, tol=0.01, scaling=4.0) -> None:
        self.value = value
        self.action = Action.LEFT
        self.tol = tol
        self.scaling_coef = scaling
    def update(self, value) -> float:
        if abs(value - self.value)/self.value < self.tol: return 0
        if value > self.value:
            self.action = Action.RIGHT
        else:
            self.action = Action.LEFT
        num = ((180) / (rot[-1] - rot[0]))
        value_deg =  num * (value - rot[0])
        curr_value_deg = num * (self.value - rot[0])
        self.value = value
        return (curr_value_deg - value_deg) * self.scaling_coef
        

class AccelerateState:
    def __init__(self, value, tol=0.01) -> None:
        self.value = value
        self.action = Action.GAS
        self.tol = tol
    def update(self, value):
        if value == 0: self.action = Action.BREAK; return
        if abs(value - self.value)/self.value < self.tol: return
        if value < self.value:
            self.action = Action.BREAK
        else:
            self.action = Action.GAS
        self.value = value


async def print_events(device, id, turn, acc, Car1):
    # turn, acc = obj[device]
    async for event in device.async_read_loop():
            code = event.code
            type = event.type
            value = event.value
            type_code = (type, code)
            if type_code in event_types:
                event_type = event_types[type_code]
                if event_type == "ABS_WHEEL":
                    deg = turn.update(value)
                    print(id, turn.action, acc.action, deg)
                    Car1.turn(deg)
                    dt = clock.tick(60) * 1e-3
                    if(abs(Car1.pos[0] > 100)):
                        Car1.accelerate(-10, dt)
                    Car1.update_state(dt)

                    screen.fill((105, 205, 4))
                    window.draw(Car1.pos)
                    
                    pygame.display.flip()
                elif event_type == "ABS_GAS":
                    acc.update(value)
                    print(id, turn.action, acc.action)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: sys.exit(0)
                # keys = pygame.key.get_pressed()

                # if keys[pygame.K_LEFT]:
                    
                # elif keys[pygame.K_RIGHT]:
                #     Car1.turn(-1)
                # else:
                #     Car1.turn(-0.05 * np.rad2deg(Car1.orientation - np.pi/2))



if __name__ == "__main__":
    size = width, height = 1024, 768
    screen = pygame.display.set_mode(size)
    done = False
    clock = pygame.time.Clock()
    Car1 = Car()
    Car1.set_speed(100)
    Car1.set_orientation(np.radians(90))

    window = Window(screen, width, height)
    devs = get_devices()
    print(devs)
    for i, device in enumerate(devs):
        turn = TurnState(1)
        acc = AccelerateState(1)
        # obj[device] = (turn, acc)
        asyncio.ensure_future(print_events(device, i, turn, acc, Car1))

    loop = asyncio.get_event_loop()
    loop.run_forever()




# while not done:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT: done = True



