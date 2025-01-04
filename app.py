from flask import Flask, render_template, Response, request, jsonify
from pyboy import PyBoy
import threading
import time
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/screen', methods=['GET'])
def get_screen():
    if last_frame:
        return Response(last_frame, mimetype='image/png')
    else:
        return jsonify({"error": "No frame available"}), 404

@app.route('/press', methods=['POST'])
def press_key():
    key = request.json.get('key')
    if key and key not in pressed_keys:
        pressed_keys.add(key)
    return jsonify({"status": "key pressed"}), 200

@app.route('/release', methods=['POST'])
def release_key():
    key = request.json.get('key')
    if key and key in pressed_keys:
        pressed_keys.remove(key)
    return jsonify({"status": "key released"}), 200

@app.route('/save', methods=['POST'])
def save_progress():
    with open(state_save_path, 'wb') as save_file:
        pyboy.save_state(save_file)
    return jsonify({"status": "Game saved successfully!"})

@app.route('/load', methods=['POST'])
def load_progress():
    if os.path.exists(state_save_path):
        with open(state_save_path, 'rb') as load_file:
            pyboy.load_state(load_file)
        return jsonify({"status": "Game loaded successfully!"})
    else:
        return jsonify({"error": "Save state file not found"}), 404

@app.route('/get_run_data', methods=['GET'])
def get_run_data():
    return jsonify(pyboy.run_data)

if __name__ == '__main__':
    log = logging.getLogger('werkzeug')
    log.disabled = True
    app.run(host='0.0.0.0', port=8000, debug=True)
