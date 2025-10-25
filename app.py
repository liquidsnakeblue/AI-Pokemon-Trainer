from flask import (
    Flask,
    render_template,
    Response,
    request,
    jsonify
)
from pyboy import PyBoy

import websockets
import asyncio
import threading
import warnings
import logging
import signal
import base64
import time
import code
import json
import sys
import io
import os

from pygments.lexers import PythonLexer
from prompt_toolkit import PromptSession
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.history import InMemoryHistory

from werkzeug.serving import WSGIRequestHandler
from pathlib import Path

from engine.fight import do_fight

LISTEN_ADDR = os.getenv('AI_POKEMON_TRAINER_LISTEN_ADDR', '0.0.0.0')
HTTP_PORT = int(os.getenv('AI_POKEMON_TRAINER_HTTP_PORT', '8000'))
WS_PORT = int(os.getenv('AI_POKEMON_TRAINER_WS_PORT', '18080'))

app = Flask(__name__)
master_pid = os.getpid()

enable_auto_tick = True
last_frame = None
pressed_keys = set()
pressed_keys_lock = threading.Lock()
run_data_lock = threading.Lock()

BASE_DIR = Path(__file__).resolve().parent
state_save_path = BASE_DIR / "red.gb.state"

logger = logging.getLogger("ai_pokemon_trainer")
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
if os.getenv('AI_POKEMON_TRAINER_DEBUG', '0') == '0':
    console_handler.setLevel(logging.INFO)
else:
    console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s](%(module)s)[%(levelname)s] %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

class PyBoy_Web(PyBoy):
    total_usage_token = 0
    
    __run_data = {
        "status_msg": "Manual Operation",
        "action_msg": "There not Action now.",
        "reason_msg": "There not Reason now.",
        "think_status": False,
    }

    def update_run_data(self, field, msg):
        with run_data_lock:
            self.__run_data[field] = msg
    
    def get_run_data(self):
        with run_data_lock:
            return self.__run_data
            
    def get_party_data(self):   # Our new Party Status Tracker
        """Read party Pokemon data from memory"""
        from engine.index_data import internal_index
        from engine.component import connect_digit_list

        party = []
        party_count = self.memory[0xD163]  # Number of Pokemon in party

        # Party Pokemon data structure (matching fight.py)
        party_slots = [
            {"species": 0xD164, "hp": [0xD16C, 0xD16D], "level": 0xD18C, "max_hp": [0xD18D, 0xD18E]},  # Slot 1
            {"species": 0xD165, "hp": [0xD198, 0xD199], "level": 0xD1B8, "max_hp": [0xD1B9, 0xD1BA]},  # Slot 2
            {"species": 0xD166, "hp": [0xD1C4, 0xD1C5], "level": 0xD1E4, "max_hp": [0xD1E5, 0xD1E6]},  # Slot 3
            {"species": 0xD167, "hp": [0xD1F0, 0xD1F1], "level": 0xD210, "max_hp": [0xD211, 0xD212]},  # Slot 4
            {"species": 0xD168, "hp": [0xD21C, 0xD21D], "level": 0xD23C, "max_hp": [0xD23D, 0xD23E]},  # Slot 5
            {"species": 0xD169, "hp": [0xD248, 0xD249], "level": 0xD268, "max_hp": [0xD269, 0xD26A]},  # Slot 6
        ]

        for i in range(6):
            if i >= party_count:
                party.append({"exists": False})
                continue

            slot = party_slots[i]
            species_id = self.memory[slot["species"]]

            if species_id == 0 or species_id == 0xFF:
                party.append({"exists": False})
                continue

            # Get Pokemon name from index (internal_index is a list indexed by species ID)
            pokemon_name = "Unknown"
            try:
                if 0 <= species_id < len(internal_index):
                    pokemon_name = internal_index[species_id]["name"]
                else:
                    logger.debug(f"Species ID {species_id} out of range (max: {len(internal_index)-1})")
            except Exception as e:
                logger.error(f"Error looking up Pokemon name for species {species_id}: {e}")

            # Read HP values using the correct function from component.py
            current_hp = connect_digit_list([self.memory[slot["hp"][0]], self.memory[slot["hp"][1]]])
            max_hp = connect_digit_list([self.memory[slot["max_hp"][0]], self.memory[slot["max_hp"][1]]])
            level = self.memory[slot["level"]]

            party.append({
                "exists": True,
                "name": pokemon_name,
                "level": level,
                "hp": current_hp,
                "max_hp": max_hp,
                "hp_percent": int((current_hp / max_hp * 100) if max_hp > 0 else 0)
            })

        return party
    
    def tick(self, count=1, render=True):
        global last_frame
        screen = self.screen
        image = screen.image
        byte_io = io.BytesIO()
        image.save(byte_io, 'PNG')
        byte_io.seek(0)
        last_frame = byte_io.getvalue()
        if os.getenv('AI_POKEMON_TRAINER_SKIP_ANIMATION') == '0':
            time.sleep(0.01)
        return super().tick(count, render)

    def press_and_release(self, key):
        """
        Automatic Press Button
        """
        for _ in range(10):
            self.tick()
        self.button_press(key)
        for _ in range(10):
            self.tick()
        self.button_release(key)
        for _ in range(10):
            self.tick()
    
    def pre_fight_test(self, pyboy):
        pass

pyboy = PyBoy_Web("red.gb", window="null", sound_emulated=False)

if state_save_path.exists():
    with open(state_save_path, "rb") as f:
        pyboy.load_state(f)

def pyboy_thread():
    if os.getenv('AI_POKEMON_TRAINER_FIGHT_TEST', '0') == "1":
        logger.info("Perpare the fight test")
        print("!!! Move pokemon onto the lawn !!!")

        from test import test_fight
        report = test_fight.run_test(int(os.getenv('AI_POKEMON_TRAINER_TEST_CNT', '20')), pyboy)
        logger.info("End of the test, exit.")
        os.kill(master_pid, signal.SIGTERM)
    else:
        while True:
            with pressed_keys_lock:
                tmp = pressed_keys

                for key in tmp:
                    pyboy.button_press(key)

                if enable_auto_tick:
                    pyboy.tick()
        
                for key in tmp:
                    pyboy.button_release(key)

            if os.getenv('AI_POKEMON_TRAINER_NO_AUTO') == '0' and pyboy.memory[0xD057]==1:
                do_fight(pyboy)
        
            time.sleep(0.01)

pyboy_thread_instance = threading.Thread(target=pyboy_thread)
pyboy_thread_instance.daemon = True
pyboy_thread_instance.start()
logger.info("Stared PyBoy thread.")

async def websocket_handler(websocket, path):
    if path == "/screen":
        try:
            last_data = None
            while True:
                base64_data = "data:image/jpeg;base64," + str(base64.b64encode(last_frame), 'utf-8')
                if last_data!=base64_data:
                    await websocket.send(base64_data)
                    last_data=base64_data
                await asyncio.sleep(0.01)
        except (websockets.exceptions.ConnectionClosedOK,websockets.exceptions.ConnectionClosedError):
            logger.warning("websockets connection closed.")
            
    elif path == "/get_run_data":
        try:
            last_data = None
            while True:
                tmp = json.dumps(pyboy.get_run_data())
                if last_data!=tmp:
                    await websocket.send(tmp)
                    last_data=tmp
                await asyncio.sleep(0.1)
        except (websockets.exceptions.ConnectionClosedOK,websockets.exceptions.ConnectionClosedError):
            logger.warning("websockets connection closed.")
    
    elif path == "/get_party_data":
        try:
            last_data = None
            while True:
                tmp = json.dumps(pyboy.get_party_data())
                if last_data!=tmp:
                    await websocket.send(tmp)
                    last_data=tmp
                await asyncio.sleep(0.5)  # Update every 0.5 seconds
        except (websockets.exceptions.ConnectionClosedOK,websockets.exceptions.ConnectionClosedError):
            logger.warning("websockets connection closed.")
            
    elif path == "/press":
        try:
            async for message in websocket:
                key = message
                if key and key not in pressed_keys:
                    with pressed_keys_lock:
                        pressed_keys.add(key)
        except (websockets.exceptions.ConnectionClosedOK,websockets.exceptions.ConnectionClosedError):
            logger.warning("websockets connection closed.")
                
    elif path == "/release":
        try:
            async for message in websocket:
                key = message
                if key and key in pressed_keys:
                    with pressed_keys_lock:
                        pressed_keys.remove(key)
        except (websockets.exceptions.ConnectionClosedOK,websockets.exceptions.ConnectionClosedError):
            logger.warning("websockets connection closed.")
                
    elif path == "/save_load":
        try:
            async for message in websocket:
                if message == "save":
                    with open(state_save_path, 'wb') as save_file:
                        pyboy.save_state(save_file)
                    await websocket.send("Game saved successfully!")
                
                elif message == "load":
                    if os.path.exists(state_save_path):
                        with open(state_save_path, 'rb') as load_file:
                            pyboy.load_state(load_file)
                        await websocket.send("Game loaded successfully!")
                    else:
                        await websocket.send("Save state file not found")
        except (websockets.exceptions.ConnectionClosedOK,websockets.exceptions.ConnectionClosedError):
            logger.warning("websockets connection closed.")

def start_websocket_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    start_server = websockets.serve(websocket_handler, LISTEN_ADDR, WS_PORT)
    loop.run_until_complete(start_server)
    loop.run_forever()

websocket_thread = threading.Thread(target=start_websocket_server)
websocket_thread.daemon = True
websocket_thread.start()
logger.info(f"Started WebSocket Thread in Port {WS_PORT}.")

def shell_console():
    console = code.InteractiveConsole(globals())

    history = InMemoryHistory()
    session = PromptSession(history=history)
    
    print("Enter Python code to execute. Type 'exit' to quit.")
    while True:
        user_input = session.prompt(
            ">>> ",
            lexer=PygmentsLexer(PythonLexer),
        )
        if user_input.strip().lower() == 'exit':
            print("Exiting interactive console...")
            break
        if not user_input.strip():
            time.sleep(0.1)
            continue

        try:
            console.push(user_input)
        except Exception as e:
            print(f"Error: {e}")
    os.kill(master_pid, signal.SIGTERM)

shell_thread = threading.Thread(target=shell_console)

@app.route('/')
def index():
    return render_template('index.html', WS_PORT = WS_PORT)

log = logging.getLogger('werkzeug')
log.disabled = True
cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None
logger.info(f"Start HTTP Web Server http://{LISTEN_ADDR}:{HTTP_PORT}/ .")

if os.getenv('AI_POKEMON_TRAINER_SHELL', '0') == '1':
    shell_thread.start()

app.run(host=LISTEN_ADDR, port=HTTP_PORT, debug=False)
