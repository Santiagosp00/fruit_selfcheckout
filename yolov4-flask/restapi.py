"""
Run a rest API exposing the yolov5s object detection model
"""
import argparse
import io
from PIL import Image
import numpy as np
import cv2
import base64
from object_detector import inference
from flask import Flask, request

app = Flask(__name__)

DETECTION_URL = "/v1/object-detection/yolov4"


@app.route(DETECTION_URL, methods=["POST"])
def predict():
    if not request.method == "POST":
        return

    if request.files.get("image"):
        image_file = request.files["image"]
        img_bytes = image_file.read()
        npimg = np.fromstring(img_bytes, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        tags = ["apple","banana","grapefruit","orange","tomato"]
        _, class_img = inference(img, tags)

        return class_img


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask api exposing yolov4 model")
    parser.add_argument("--port", default=5000, type=int, help="port number")
    args = parser.parse_args()

    # model = torch.hub.load(
    #     "ultralytics/yolov5", "yolov5s", pretrained=True, force_reload=True
    # ).autoshape()  # force_reload = recache latest code
    # model.eval()
    app.run(host="0.0.0.0", port=args.port)  # debug=True causes Restarting with stat
