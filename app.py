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
console_handler.setLevel(logging.INFO)
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
    
    def pre_fight_test(self):
        pass

pyboy = PyBoy_Web("red.gb", window="null")

if state_save_path.exists():
    with open(state_save_path, "rb") as f:
        pyboy.load_state(f)

def pyboy_thread():
    if os.getenv('AI_POKEMON_TRAINER_FIGHT_TEST', '0') == "1":
        logger.info("Perpare the fight test")
        print("!!! Move pokemon onto the lawn !!!")

        from test import test_fight
        report = test_fight.run_test(int(os.getenv('AI_POKEMON_TRAINER_TEST_CNT', '20')), pyboy)
        logger.info(report)
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

            if bool(pyboy.memory[0xD057]):
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
    
    print("Enter Python code to execute. Type 'exit' to quit.")
    while True:
        user_input = input(">>> ")
        if user_input.strip().lower() == 'exit':
            print("Exiting interactive console...")
            break
        if not user_input:
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
