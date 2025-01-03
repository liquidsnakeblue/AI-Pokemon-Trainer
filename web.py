import main
import threading, io
from flask import Flask, render_template, Response, request, jsonify

def get_screen():
    screen = main.pyboy.screen
    image = screen.image
    byte_io = io.BytesIO()
    image.save(byte_io, 'PNG')
    byte_io.seek(0)
    return byte_io.getvalue()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/screen', methods=['GET'])
def get_screen_web():
    return Response(get_screen(), mimetype='image/png')

threads = [
    threading.Thread(target=main.pyboy_thread),
    # threading.Thread(target=webserver)
]

if __name__ == "__main__":

    for i in threads:
        i.start()

    app.run(host='0.0.0.0', port=8000, debug=True)