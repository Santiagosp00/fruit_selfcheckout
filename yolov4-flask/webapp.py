"""
Simple app to upload an image via a web form 
and view the inference results on the image in the browser.
"""
import argparse
import io
import sys
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

def ticket_generation(content_txt,Total,counter):
    txt_base = """Producto        Cantidad        Precio Unitario """
    txt_final = """

    Total              """+str(counter)+"""               $ """+str(Total)+"""                
    """
    ticket = ''.join([txt_base,content_txt,txt_final])
    with open("./ticket.txt","w") as f:
        f.write(ticket)
    return ticket

def fruits_writer(class_img):
    tags = ["Manzana","Plátano","Toronja","Naranja","Jitomate"]
    prices = [20.00,8.00,14.00,7.00,5.00]
    fruits_dic = {tags[i]:{"count":class_img.count(i),"price":prices[i]} for i in class_img}
    fruits_sorted = dict(sorted(fruits_dic.items()))
    fruit_cost = 0
    for fruit_dic in fruits_sorted.values():
        fruit_cost += fruit_dic["count"] * fruit_dic["price"]

    fruits_txt = ''.join(["""
    """+key+"""             """+str(dic_val['count'])+"""               $ """+str(dic_val['price'])+""" """ 
    for key, dic_val in fruits_sorted.items()])

    return fruits_txt,fruit_cost

@app.route("/", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        if "files[]" not in request.files:
            app.logger.info("No hay file")
            return redirect(request.url)
        app.logger.info("Sí hay file")
        files = request.files.getlist("files[]")
        if not files:
            return
        counter = 0
        Total = 0
        fruits_txt = ''
        images = []
        for idx,file in enumerate(files):
            img_bytes = file.read()
            npimg = np.fromstring(img_bytes, np.uint8)
            img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
            tags = ["apple","banana","grapefruit","orange","tomato"]
            pred_img, class_img = inference(img,tags)
            rgb_img = cv2.cvtColor(pred_img, cv2.COLOR_BGR2RGB)
            file_name = "static/result_"+str(idx)+".jpg"
            images.append(file_name)
            cv2.imwrite(file_name,rgb_img)
            counter += len(class_img)
            fruit_section,fruit_cost = fruits_writer(class_img)
            fruits_txt = ''.join([fruits_txt,fruit_section])
            Total += fruit_cost
        ticket = ticket_generation(fruits_txt,Total,counter)

        return render_template("result.html", counter=counter,ticket=ticket,images=images)

    return render_template("index.html")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask app exposing yolov4 models")
    parser.add_argument("--port", default=5000, type=int, help="port number")
    args = parser.parse_args()
    app.run(host="0.0.0.0", port=args.port)  # debug=True causes Restarting with stat
