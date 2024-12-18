from pyboy import PyBoy
import time

from engine.fight import do_fight

pyboy = PyBoy("red.gb")

def pyboy_thread():
    while True:
        pyboy.tick()

        if bool(pyboy.memory[0xD057]):
            do_fight(pyboy)
        
        time.sleep(0.01)

if __name__ == "__main__":
    pyboy_thread()