import cv2
import numpy as np
from flask import Flask, Response, request, jsonify
import pyautogui

app = Flask(__name__)

def capture_screen():
    while True:
        # Capture the screen using pyautogui
        screen = pyautogui.screenshot()
        screen_np = np.array(screen)

        # Convert the color from BGR to RGB
        frame = cv2.cvtColor(screen_np, cv2.COLOR_BGR2RGB)

        # Encode the frame in JPEG format
        ret, jpeg = cv2.imencode('.jpg', frame)

        # Ensure encoding was successful
        if not ret:
            continue

        # Yield the frame as a byte stream
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(capture_screen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return '''
    <h1>Live Screen Feed with Control</h1>
    <img src="/video_feed" width="100%">
    <script>
        document.addEventListener("click", function(event) {
            fetch('/click', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({x: event.clientX, y: event.clientY}),
            });
        });

        document.addEventListener("keydown", function(event) {
            fetch('/keydown', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({key: event.key}),
            });
        });
    </script>
    '''

@app.route('/click', methods=['POST'])
def click():
    data = request.json
    x, y = data['x'], data['y']
    pyautogui.click(x, y)
    return jsonify(success=True)

@app.route('/keydown', methods=['POST'])
def keydown():
    data = request.json
    key = data['key']
    pyautogui.press(key)
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
