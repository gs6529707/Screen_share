# Live Screen Feed with Control

This project is a Flask application that streams the live screen feed of your computer and allows control via mouse clicks and keyboard inputs. The application captures the screen using `pyautogui`, converts the image for streaming, and uses Flask to serve the video feed and handle user interactions.

## Features

- **Live Screen Feed**: Stream the live screen feed of your computer in real-time.
- **Mouse Click Control**: Control the mouse clicks remotely through the web interface.
- **Keyboard Input Control**: Control the keyboard inputs remotely through the web interface.

## Technologies Used

- **Python**
  - `Flask`: A lightweight WSGI web application framework.
  - `pyautogui`: A module for programmatically controlling the mouse and keyboard.
  - `OpenCV (cv2)`: A library for computer vision tasks.
  - `NumPy`: A library for numerical computations.
- **HTML and JavaScript**: For the web interface to display the video feed and capture user interactions.

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Application**:
    ```bash
    python app.py
    ```

## Usage

1. **Access the Application**:
   Open your web browser and go to `http://localhost:8000` to view the live screen feed.

2. **Control the Screen**:
   - **Mouse Click**: Click anywhere on the screen feed to send a mouse click to that position on your computer.
   - **Keyboard Input**: Press any key while focused on the screen feed to send that key press to your computer.

## Code Overview

### `app.py`

- **Imports and Setup**:
    ```python
    import cv2
    import numpy as np
    from flask import Flask, Response, request, jsonify
    import pyautogui

    app = Flask(__name__)
    ```

- **Screen Capture Function**:
    ```python
    def capture_screen():
        while True:
            screen = pyautogui.screenshot()
            screen_np = np.array(screen)
            frame = cv2.cvtColor(screen_np, cv2.COLOR_BGR2RGB)
            ret, jpeg = cv2.imencode('.jpg', frame)
            if not ret:
                continue
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
    ```

- **Routes**:
    - **Video Feed Route**:
        ```python
        @app.route('/video_feed')
        def video_feed():
            return Response(capture_screen(), mimetype='multipart/x-mixed-replace; boundary=frame')
        ```

    - **Index Route**:
        ```python
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
        ```

    - **Mouse Click Route**:
        ```python
        @app.route('/click', methods=['POST'])
        def click():
            data = request.json
            x, y = data['x'], data['y']
            pyautogui.click(x, y)
            return jsonify(success=True)
        ```

    - **Keyboard Input Route**:
        ```python
        @app.route('/keydown', methods=['POST'])
        def keydown():
            data = request.json
            key = data['key']
            pyautogui.press(key)
            return jsonify(success=True)
        ```

- **Run the Application**:
    ```python
    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=8000, debug=True)
    ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

