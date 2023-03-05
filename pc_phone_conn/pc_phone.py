import asyncio
import evdev
from enum import Enum

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
    def __init__(self, value, tol=0.01) -> None:
        self.value = value
        self.action = Action.LEFT
        self.tol = tol
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
        return value_deg - curr_value_deg
        

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


async def print_events(device, id, turn, acc):
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
                elif event_type == "ABS_GAS":
                    acc.update(value)
                    print(id, turn.action, acc.action)


if __name__ == "__main__":
    devs = get_devices()
    print(devs)
    for i, device in enumerate(devs):
        turn = TurnState(1)
        acc = AccelerateState(1)
        # obj[device] = (turn, acc)
        asyncio.ensure_future(print_events(device, i, turn, acc))

    loop = asyncio.get_event_loop()
    loop.run_forever()

    # for dev in devs:
    #     print(dev.capabilities())
    #     turn = TurnState(1)
    #     acc = AccelerateState(1)
    #     for event in dev.read_loop():
    #         code = event.code
    #         type = event.type
    #         value = event.value
    #         type_code = (type, code)
    #         if type_code in event_types:
    #             event_type = event_types[type_code]
    #             if event_type == "ABS_WHEEL":
    #                 print(value)
    #                 turn.update(value)
    #             elif event_type == "ABS_GAS":
    #                 acc.update(value)
    #             print(turn.action, acc.action)




