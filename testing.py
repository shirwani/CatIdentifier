from utils import *
import pickle
import h5py
import json

if __name__ == '__main__':
    print("Initiating testing")

    cfg = get_configs()
    data_file = cfg['testing']['data_file']
    model = cfg['model']['file']

    print(f"Model: {model}")

    dataset = h5py.File(data_file, "r")

    x_orig = np.array(dataset["x"][:])
    y = np.array(dataset["y"][:])
    x = x_orig.reshape(x_orig.shape[0], -1).T / 255.

    print(f"x_orig.shape: {x_orig.shape}")
    print(f"x.shape: {x.shape}")

    print(x)

    with open("models/"+model, 'rb') as file:
        data = pickle.load(file)

    parameters = data['parameters']

    my_prediction, my_accuracy = predict(x, y, parameters)
    print(my_prediction.astype(int)[0])
    print("Accuracy: {}%".format(round(my_accuracy * 100)))
