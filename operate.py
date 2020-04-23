import json
import requests
from difflib import get_close_matches
from flask import Flask, request, redirect, url_for, render_template
# from keras.models import load_model
# from keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
import io
from base64 import b64encode

app = Flask(__name__, template_folder='templates')

@app.route('/')
def hello_world():
    return render_template('uploadImage.html')

@app.route('/preview')
def preview():
    return render_template('preview_image.html')


@app.route("/uploadImage", methods=["GET", "POST"])
def upload_image():

    if request.method == "POST":

        if request.files:
            # files = image
            image = request.files["image"]
            #read image file string data
            # img = image.read()
            # mystring = TextIOWrapper(img)
            # print(mystring)
            # files = image.read().decode('UTF-8')
            if image.filename == "":
                print("No filename")
                return redirect(request.url)

            img = mpimg.imread(image)
            print(image.filename)
            #nd array image
            byte = b64encode(image.read()).decode("utf-8")
            print(image.filename)
            #convert string data to numpy array
            # npimg = np.fromstring(img, np.uint8)
            # print(type(image))
            # print(byte)
            # print()
            # print(files)
            # print(type(img))
            # print("***")
            # saving images
            im1 = Image.open(image)
            im1 = im1.save('image.png')
            # imgs = Image.fromarray(img, 'RGB')
            # imgs.save('image.png')
            # imgs.show()
            print(plt.imshow(img))
            print(type(img))
            print(type(im1))
            # plt.show()
            # arr = np.array(img)
            # images = Image.fromarray(arr.astype('uint8'))
            # create file-object in memory
            # file_object = io.BytesIO()
            # write PNG in file-object
            # img.save(file_object, 'PNG')
            # print(type(npimg))
            # imgg = plt.imshow(npimg)
            # print(imgg)

            # return redirect(request.url)
            filename = "D:\My Programs\Projects\Gender Classifier\image.png"
            return redirect(url_for('preview'))


    return render_template("uploadImage.html")


if __name__ == "__main__":
    app.run(debug = True)
