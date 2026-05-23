from flask import Flask, render_template, request, Response
from ultralytics import YOLO
import cv2
import os
import uuid

app = Flask(__name__)

# =========================================
# FOLDERS
# =========================================

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "static/outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# =========================================
# LOAD YOLO MODEL
# =========================================

model = YOLO("best.pt")

# =========================================
# CAMERA
# =========================================

camera = None

# =========================================
# HOME PAGE
# =========================================

@app.route('/')
def home():
    return render_template('index.html')

# =========================================
# IMAGE DETECTION
# =========================================

@app.route('/predict', methods=['POST'])
def predict():

    if 'file' not in request.files:
        return "No file uploaded"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    # Generate unique filename
    filename = str(uuid.uuid4()) + ".jpg"

    upload_path = os.path.join(UPLOAD_FOLDER, filename)
    output_path = os.path.join(OUTPUT_FOLDER, filename)

    # Save uploaded image
    file.save(upload_path)

    # YOLO prediction
    results = model.predict(
        source=upload_path,
        conf=0.4
    )

    # Draw detections
    plotted = results[0].plot()

    # Save output image
    cv2.imwrite(output_path, plotted)

    return render_template(
        'index.html',
        output_image=output_path
    )

# =========================================
# LIVE CAMERA FRAME GENERATOR
# =========================================

def generate_frames():

    global camera

    # Initialize camera only when needed
    if camera is None:
        camera = cv2.VideoCapture(0)

    while True:

        success, frame = camera.read()

        if not success:
            break

        # YOLO prediction
        results = model.predict(
            source=frame,
            conf=0.4,
            verbose=False
        )

        # Draw detections
        annotated_frame = results[0].plot()

        # Encode frame
        ret, buffer = cv2.imencode('.jpg', annotated_frame)

        frame = buffer.tobytes()

        # Stream frame
        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            frame +
            b'\r\n'
        )

# =========================================
# VIDEO FEED ROUTE
# =========================================

@app.route('/video_feed')
def video_feed():

    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

# =========================================
# LIVE PAGE
# =========================================

@app.route('/live')
def live():
    return render_template('live.html')

# =========================================
# MAIN
# =========================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )