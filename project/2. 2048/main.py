import random
from pynput import keyboard
import time
import numpy as np

game_state = {"game": True}
map = []


def init_map():
    for i in range(4):
        map.append([])
        for j in range(4):
            map[i].append(0)
    random_create()
    random_create()


def print_map():
    for i in range(5):
        if i < 4:
            print("+----+----+----+----+")
            for j in range(5):
                if j < 4:
                    print("|", end='')
                    if map[i][j] == 0:
                        print("    ", end="")
                    if 0 < map[i][j] < 10:
                        print("  %d " % map[i][j], end="")
                    if 9 < map[i][j] < 100:
                        print(" %d " % map[i][j], end="")
                    if 99 < map[i][j] < 1000:
                        print(" %d" % map[i][j], end="")
                else:
                    print("|")
        else:
            print("+----+----+----+----+")


def on_press(key):
    # 按下按键时执行。
    if not game_state['game']:
        print("game ove")
        return False
    try:
        if key.char == 'w':
            print("w")
            move("w")
            return False
        if key.char == 'a':
            print("a")
            move("a")
            return False
        if key.char == 's':
            print("s")
            move("s")
            return False
        if key.char == 'd':
            print("d")
            move("d")
            return False
    except AttributeError:
        pass


def on_release(key):
    global game_state
    '松开按键时执行。'
    if not game_state['game']:
        print("game ov")
        return False
    if key == keyboard.Key.esc:
        game_state['game'] = False
        print("esc")
        time.sleep(1)
        return False


def state():
    n = 0
    map2 = list(zip(*map))
    for i in range(4):
        for j in range(3):
            if map[i][j] == map[i][j + 1]:
                n += 1
            if map2[i][j] == map2[i][j + 1]:
                n += 1
    if n == 0 or not game_state['game']:
        return False
    return True


def keys():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


def random_create():
    l1 = []
    l2 = []
    l3 = [2, 2, 2, 2, 2, 2, 2, 2, 2, 4]
    for i in range(4):
        for j in range(4):
            if map[i][j] == 0:
                l1.append(i)
                l2.append(j)
    if len(l1) > 0:
        r = random.randrange(0, len(l1))
        r2 = random.randrange(0, 10)
        map[l1[r]][l2[r]] = l3[r2]
    else:
        return False


def start_game():
    while state():
        print_map()
        keys()
        random_create()
    print("game over")


def move(x):
    global map
    if x == "w":
        map = np.transpose(map).tolist()
        left_merge()
        map = np.transpose(map).tolist()
    if x == "a":
        left_merge()
    if x == "s":
        map = np.transpose(map).tolist()
        right_merge()
        map = np.transpose(map).tolist()
    if x == "d":
        right_merge()


def clear_left():
    for i in range(4):
        for j in range(4):
            for k in range(j, -1, -1):
                if map[i][j] != 0 and map[i][k] == 0:
                    map[i][k] = map[i][j]
                    map[i][j] = 0


def clear_right():
    for i in range(4):
        for j in range(3, -1, -1):
            for k in range(j, 4):
                if map[i][j] != 0 and map[i][k] == 0:
                    map[i][k] = map[i][j]
                    map[i][j] = 0


def left_merge():
    global map
    for i in range(4):
        for j in range(3):
            if map[i][j] == map[i][j + 1]:
                map[i][j] += map[i][j + 1]
                map[i][j + 1] = 0
            clear_left()


def right_merge():
    global map
    for i in range(4):
        for j in range(3):
            if map[i][j] == map[i][j + 1]:
                map[i][j + 1] += map[i][j]
                map[i][j] = 0
            clear_right()


if __name__ == "__main__":
    init_map()
    start_game()
