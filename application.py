from utils import *
from flask import Flask, render_template, request
import requests
import pickle
import numpy as np
from PIL import Image
from io import BytesIO

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def run():
    icon_img = "http://zakishirwani.com/ai/cats/static/images/cat-icon4.jpg"
    default_img_url = "http://zakishirwani.com/ai/cats/static/images/1000_F_97589769_t45CqXyzjz0KXwoBZT9PRaWGHRk5hQqQ.jpg"
    return render_template("getUserInput.html", default_img_url=default_img_url, icon_img=icon_img)


@app.route('/result', methods=['GET', 'POST'])
def identify():
    with open("models/model.pkl", 'rb') as file:
        data = pickle.load(file)

    parameters = data['parameters']
    num_px = data['num_px']

    classes = ["not a cat", "cat"]

    img_url = request.json

    try:
        img_data = requests.get(img_url).content
        image = Image.open(BytesIO(img_data))
        image = np.array(image.resize((num_px, num_px)))
        image = image.reshape((1, num_px * num_px * 3)).T / 255.
        my_prediction = predict(image, 1, parameters)
        y = str(np.squeeze(my_prediction))
        obj = classes[int(np.squeeze(my_prediction))]
        return render_template("showResult.html", prediction=y, obj=obj, img_url=img_url)
    except:
        print("BAD_URL: " + img_url)
        return render_template("imageError.html")

if __name__ == '__main__':
    app.run(debug=True, port=5004)
