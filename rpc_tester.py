import multiprocessing
import os
import subprocess
import threading

import zerorpc
from main import start_instance

def main():
    # todo switch to using subprocess input instead of rpc

    p = multiprocessing.Process(target=start_instance)
    p.start()
    c = zerorpc.Client()
    c.connect("tcp://127.0.0.1:4242")
    while True:
        console = str(input())
        if console == "quit":
            return
        elif console == "up":
            print(c.move_up())
        elif console == "down":
            print(c.move_down())
        elif console == "left":
            print(c.move_left())
        elif console == "right":
            print(c.move_right())
        elif console == "up left":
            print(c.move_up_left())
        elif console == "up right":
            print(c.move_up_right())
        elif console == "down left":
            print(c.move_down_left())
        elif console == "down right":
            print(c.move_down_right())
        elif console == "pickup":
            print(c.pickup())
        elif console == "descend":
            print(c.descend())
        elif console == "inventory":
            print(c.inventory())
            console = str(input())
            while True:
                if len(console) < 1 and ord("a") <= ord(console) <= ord("z"):
                    print(c.inventory_key(console))
                    break
                else:
                    print("input only one lowercase letter")
        else:
            print("invalid input")


if __name__ == "__main__":
    main()
