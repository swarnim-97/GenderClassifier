import json
import requests
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
from keras.models import load_model
from keras.models import model_from_json
from keras.preprocessing import image


app = Flask(__name__, template_folder='templates')

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def hello_world():
    return render_template('uploadImage.html')

@app.route('/preview')
def preview():
    return render_template('preview_image.html')

#load Model
def loadModel():
    path = os.path.join(APP_ROOT, "model_in_json.json")
    print(path)
    model_path = os.path.join(APP_ROOT, "model.h5")
    print(model_path)
    with open(path,'r') as f:
        model_json = json.load(f)

    loaded_model = model_from_json(model_json)
    loaded_model.load_weights(model_path)
    return loaded_model

#predict
def predicts(filename, loaded_model):
    img_width, img_height = 64, 64
    image_path = filename
    img = image.load_img(image_path, target_size=(img_width, img_height))
    # print("image loaded")
    x = image.img_to_array(img)
    # plt.imshow(x)
    x = np.expand_dims(img, axis=0)

    images = np.vstack([x])
    classes = loaded_model.predict_classes(images, batch_size=10)
    # print(classes)
    return classes

@app.route("/uploadImage", methods=["POST"])
def upload_image():
    target = os.path.join(APP_ROOT, 'images/')
    # target = os.path.join(APP_ROOT, 'static/')
    # print(target)
    if not os.path.isdir(target):
            os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    # print(request.files.getlist("image"))
    # image = request.files.getlist("image")
    for upload in request.files.getlist("image"):
        # print(upload)
        # print("{} is the file name".format(upload.filename))
        filename = upload.filename
        destination = "/".join([target, filename])
        # print ("Accept incoming file:", filename)
        # print ("Save it to:", destination)
        upload.save(destination)

        #converting image to ndarray
        img = mpimg.imread(upload)
        loaded_model = loadModel()
        # print("Model_loaded")
        label = predicts(destination, loaded_model)
        # print(img)

    # return send_from_directory("images", filename, as_attachment=True)
    return render_template("preview_image.html", image_name=filename, label=label)

@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)

if __name__ == "__main__":
    app.run(debug = True)
