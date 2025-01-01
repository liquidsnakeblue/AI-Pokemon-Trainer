from flask import Flask, render_template, Response, request, jsonify
from pyboy import PyBoy
import threading
import time
import io
from werkzeug.serving import WSGIRequestHandler
import os, logging

from engine.fight import do_fight

app = Flask(__name__)

pyboy = PyBoy("red.gb", window_type="headless")

last_frame = None
pressed_keys = set()
SAVE_STATE_PATH = "red.gb.state"

def pyboy_thread():
    global last_frame
    while True:
        for key in pressed_keys:
            pyboy.button_press(key)
        
        pyboy.tick(20,True)
        
        for key in list(pressed_keys):
            pyboy.button_release(key)

        if bool(pyboy.memory[0xD057]):
            do_fight(pyboy)
        
        screen = pyboy.screen
        image = screen.image
        byte_io = io.BytesIO()
        image.save(byte_io, 'PNG')
        byte_io.seek(0)
        last_frame = byte_io.getvalue()
        
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
    with open(SAVE_STATE_PATH, 'wb') as save_file:
        pyboy.save_state(save_file)
    return jsonify({"status": "Game saved successfully!"})

@app.route('/load', methods=['POST'])
def load_progress():
    if os.path.exists(SAVE_STATE_PATH):
        with open(SAVE_STATE_PATH, 'rb') as load_file:
            pyboy.load_state(load_file)
        return jsonify({"status": "Game loaded successfully!"})
    else:
        return jsonify({"error": "Save state file not found"}), 404

if __name__ == '__main__':
    log = logging.getLogger('werkzeug')
    log.disabled = True
    app.run(host='0.0.0.0', port=5000, debug=True)
