from pyboy import PyBoy
import time
import keyboard
from engine.fight import do_fight

pyboy = PyBoy("red.gb")
state_save_path="red.gb.state"
with open(state_save_path, "rb") as f:
    pyboy.load_state(f)

def pyboy_thread():
    while True:
        pyboy.tick()
        if keyboard.is_pressed("\\"):
                    print("Saving state...")
                    with open(state_save_path, "wb") as f:
                        pyboy.save_state(f)
                    print("State Saved!")
        if bool(pyboy.memory[0xD057]):
            do_fight(pyboy)
        
        time.sleep(0.01)

if __name__ == "__main__":
    pyboy_thread()