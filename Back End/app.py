from flask import Flask, render_template, Response, request, redirect, jsonify
from flask_cors import CORS
import os
from face_utils import VideoCamera, train_model

app = Flask(__name__)
CORS(app)  # <-- Enable CORS

os.makedirs('static/faces', exist_ok=True)

# Globals
camera = None
current_name = None
mode = None

@app.route('/')
def home():
    return jsonify({"message": "Flask backend for face recognition is running."})

@app.route('/register', methods=['POST'])
def register():
    global camera, current_name, mode
    current_name = request.form.get('name')
    if not current_name:
        return jsonify({"error": "Name is required"}), 400

    mode = 'register'
    camera = VideoCamera(mode, current_name)
    return jsonify({"status": "Camera started for registration."})

@app.route('/detect', methods=['GET'])
def detect():
    global camera, current_name, mode
    mode = 'detect'
    current_name = None
    camera = VideoCamera(mode)
    return jsonify({"status": "Camera started for detection."})

@app.route('/video_feed')
def video_feed():
    global camera
    if not camera:
        return "Camera not initialized", 400
    return Response(camera.get_frame_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
