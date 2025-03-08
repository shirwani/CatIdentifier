from utils import *
from flask import Flask, render_template, request
import requests
import pickle
import numpy as np
from PIL import Image
from io import BytesIO
import json
import os
import sys

dev = False
if len(sys.argv) > 1:
    if sys.argv[1] == '-dev' or sys.argv[1] == '--dev':
        dev = True

cfg = get_configs(dev)
model_file          = cfg['model']['file']
icon_img            = cfg['flask-app']['icon_img']
default_img_url     = cfg['flask-app']['default_img_url']
test_images_folder  = cfg['flask-app']['test_images_folder']
num_px              = cfg['image']['num_px']
classes             = cfg['classes']

model = os.getenv("MODEL", model_file)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def run():

    test_images = get_jpeg_files(test_images_folder)

    return render_template("getUserInput.html",
                           default_img_url=default_img_url,
                           icon_img=icon_img,
                           model=model,
                           test_images=test_images)

############
# Get result
############
@app.route('/result', methods=['GET', 'POST'])
def identify():

    with open("models/"+model, 'rb') as modelfile:
        data = pickle.load(modelfile)
    parameters = data['parameters']

    img_url = request.json

    try:
        img_data = requests.get(img_url).content
    except:
        print("BAD_URL: " + img_url)
        return render_template("imageError.html")

    image = img_to_matrix(BytesIO(img_data), num_px)
    print(f"image.shape: {image.shape}")
    image = image.reshape((1, -1)).T / 255.
    print(f"image.shape: {image.shape}")

    print(image)

    my_prediction, my_accuracy = predict(image, 1, parameters)
    print(f"my_prediction: {my_prediction}")
    print(f"my_accuracy: {my_accuracy}")
    print("Accuracy: {}%".format(round(my_accuracy * 100)))
    y = str(np.squeeze(my_prediction))
    obj = classes[int(np.squeeze(my_prediction))]
    return render_template("showResult.html", prediction=y, obj=obj, img_url=img_url)


if __name__ == '__main__':
    port = cfg['flask-app']['port']
    app.run(debug=True, port=port)
