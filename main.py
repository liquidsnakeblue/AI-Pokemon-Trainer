from pyboy import PyBoy
from pathlib import Path
import time
import keyboard
import logging

from engine.fight import do_fight

BASE_DIR = Path(__file__).resolve().parent
state_save_path = BASE_DIR / "red.gb.state"

logger = logging.getLogger("ai_pokemon_trainer")
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s](%(module)s)[%(levelname)s] %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

class PyBoy_Web(PyBoy):
    total_usage_token = 0
    def update_run_data(self, *_):
        ...

pyboy = PyBoy_Web("red.gb")

if state_save_path.exists():
    with open(state_save_path, "rb") as f:
        pyboy.load_state(f)

def pyboy_thread():
    while True:
        # pyboy.memory[0xD023] = 0
        # pyboy.memory[0xD024] = 0 # revise enemy's max hp into 0 so that skip the discussion
        pyboy.tick()
        if keyboard.is_pressed("\\"):
            logger.info("Saving state...")
            with open(state_save_path, "wb") as f:
                pyboy.save_state(f)
            logger.info("State Saved!")
        if bool(pyboy.memory[0xD057]):
            do_fight(pyboy)
        
        time.sleep(0.01)

pyboy_thread()