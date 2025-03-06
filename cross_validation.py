from utils import *
import pickle
import h5py

if __name__ == '__main__':
    print("Doing model cross-validation...")

    data_file = 'datasets/cv.h5'
    dataset = h5py.File(data_file, "r")
    x_orig = np.array(dataset["x"][:])
    y = np.array(dataset["y"][:])
    x = x_orig.reshape(x_orig.shape[0], -1).T / 255.

    print(y)

    with open("models/model.pkl", 'rb') as file:
        data = pickle.load(file)
    parameters = data['parameters']

    my_prediction, my_accuracy = predict(x, y, parameters)
    print(my_prediction.astype(int)[0])
    print("Accuracy: {}%".format(round(my_accuracy * 100)))
