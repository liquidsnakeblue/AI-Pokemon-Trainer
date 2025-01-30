from flask import Flask, render_template, Response, request, jsonify
import websockets
import asyncio
from pyboy import PyBoy
import threading
import base64
import time
import json
import io
from werkzeug.serving import WSGIRequestHandler
import os, logging
from pathlib import Path

from engine.fight import do_fight

app = Flask(__name__)

last_frame = None
pressed_keys = set()

BASE_DIR = Path(__file__).resolve().parent
state_save_path = BASE_DIR / "red.gb.state"

logger = logging.getLogger("ai_pokemon_trainer")
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
logger.addHandler(console_handler)

class PyBoy_Web(PyBoy):
    run_data = {
        "status_msg": "Manual Operation",
        "action_msg": "There not Action now.",
        "reason_msg": "There not Reason now.",
    }
    
    def tick(self, count=1, render=True):
        global last_frame
        screen = self.screen
        image = screen.image
        byte_io = io.BytesIO()
        image.save(byte_io, 'PNG')
        byte_io.seek(0)
        last_frame = byte_io.getvalue()
        return super().tick(count, render)

pyboy = PyBoy_Web("red.gb", window_type="headless")

if state_save_path.exists():
    with open(state_save_path, "rb") as f:
        pyboy.load_state(f)

def pyboy_thread():
    while True:
        for key in pressed_keys:
            pyboy.button_press(key)
        
        pyboy.tick()
        
        for key in list(pressed_keys):
            pyboy.button_release(key)

        if bool(pyboy.memory[0xD057]):
            do_fight(pyboy)
        
        time.sleep(0.01)

pyboy_thread_instance = threading.Thread(target=pyboy_thread)
pyboy_thread_instance.daemon = True
pyboy_thread_instance.start()

async def websocket_handler(websocket, path):
    if path == "/screen":
        while True:
            base64_data = "data:image/jpeg;base64," + str(base64.b64encode(last_frame), 'utf-8')
            await websocket.send(base64_data)
            await asyncio.sleep(0.1)
            
    elif path == "/get_run_data":
        while True:
            await websocket.send(json.dumps(pyboy.run_data))
            await asyncio.sleep(0.1)
            
    elif path == "/press":
        async for message in websocket:
            key = message
            if key and key not in pressed_keys:
                pressed_keys.add(key)
                
    elif path == "/release":
        async for message in websocket:
            key = message
            if key and key in pressed_keys:
                pressed_keys.remove(key)
                
    elif path == "/save_load":
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

def start_websocket_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    start_server = websockets.serve(websocket_handler, "0.0.0.0", 8080)
    loop.run_until_complete(start_server)
    loop.run_forever()

websocket_thread = threading.Thread(target=start_websocket_server)
websocket_thread.daemon = True
websocket_thread.start()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    log = logging.getLogger('werkzeug')
    log.disabled = True
    app.run(host='0.0.0.0', port=8000, debug=False)
