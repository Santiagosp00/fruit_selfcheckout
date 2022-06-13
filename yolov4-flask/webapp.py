"""
Simple app to upload an image via a web form 
and view the inference results on the image in the browser.
"""
import argparse
import io
import os
import numpy as np
import cv2
from PIL import Image
import base64
import tensorflow as tf
import keras
from object_detector import inference
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

def ticket_generation(class_img):
    tags = ["Manzana","Plátano","Toronja","Naranja","Jitomate"]
    prices = [20.00,8.00,14.00,7.00,5.00]
    fruits_dic = {tags[i]:{"count":class_img.count(i),"price":prices[i]} for i in class_img}
    fruits_sorted = dict(sorted(fruits_dic.items()))
    Total = 0
    for fruit_dic in fruits_sorted.values():
        Total += fruit_dic["count"] * fruit_dic["price"]
    txt_base = """Producto        Cantidad        Precio Unitario """
    fruits_txt = ''.join(["""
    """+key+"""             """+str(dic_val['count'])+"""               $ """+str(dic_val['price'])+""" """ 
    for key, dic_val in fruits_sorted.items()])

    txt_final = """

    Total                               $ """+str(Total)+"""                
    """
    ticket = ''.join([txt_base,fruits_txt,txt_final])
    with open("./ticket.txt","w") as f:
        f.write(ticket)
    return ticket


@app.route("/", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        if not file:
            return

        img_bytes = file.read()
        npimg = np.fromstring(img_bytes, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        tags = ["apple","banana","grapefruit","orange","tomato"]
        pred_img, class_img = inference(img,tags)
        rgb_img = cv2.cvtColor(pred_img, cv2.COLOR_BGR2RGB)
        cv2.imwrite("static/result.jpg",rgb_img)
        counter = len(class_img)
        ticket = ticket_generation(class_img)

        return render_template("result.html", counter=counter,ticket=ticket)

    return render_template("index.html")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask app exposing yolov4 models")
    parser.add_argument("--port", default=5000, type=int, help="port number")
    args = parser.parse_args()
    app.run(host="0.0.0.0", port=args.port)  # debug=True causes Restarting with stat
