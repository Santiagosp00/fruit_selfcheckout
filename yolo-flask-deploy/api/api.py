from cProfile import run
import time
from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
import cv2
import base64
from PIL import Image
import os , io , sys
from object_detector import inference

app = Flask(__name__)
CORS(app)

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/processImage', methods=['POST'])
def process_image():
    file = request.files['image'].read()
    npimg = np.fromstring(file, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    pred_img, _ = inference(img, ["pothole"])

    pred_img = Image.fromarray(pred_img.astype("uint8"))
    rawBytes = io.BytesIO()
    pred_img.save(rawBytes, "JPEG")
    rawBytes.seek(0)
    img_base64 = base64.b64encode(rawBytes.read())

    return jsonify({
        'success': True,
        'image': str(img_base64)
    })