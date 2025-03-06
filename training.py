from utils import *
import pickle
import h5py

l = logger('training.log')

def L_layer_model(X, Y, layers_dims, learning_rate=0.0075, num_iterations=3000, print_cost=False):
    costs = []  # keep track of cost
    parameters = initialize_parameters_deep(layers_dims)
    for i in range(0, num_iterations):
        AL, caches = L_model_forward(X, parameters)
        cost = compute_cost(AL, Y)
        grads = L_model_backward(AL, Y, caches)
        parameters = update_parameters(parameters, grads, learning_rate)

        # Print the cost every 100 iterations
        if print_cost and i % 100 == 0 or i == num_iterations - 1:
            l.log("[{}] Cost after iteration {}: {}".format(get_timestamp(), i, np.squeeze(cost)))
        if i % 100 == 0 or i == num_iterations:
            costs.append(cost)

    return parameters, costs


if __name__ == '__main__':
    data_file = 'datasets/train.h5'
    dataset = h5py.File(data_file, "r")
    x_orig = np.array(dataset["x"][:])
    y_orig = np.array(dataset["y"][:])
    x = x_orig.reshape(x_orig.shape[0], -1).T / 255.
    y = np.reshape(y_orig, (1, y_orig.shape[0]))

    num_px = 64
    n_x = num_px * num_px * 3
    layers_dims = [n_x, 1000, 500, 25, 1]
    learning_rate = 0.0075
    num_iterations = 1000

    l.log("[{}] Initiating training".format(get_timestamp()))

    parameters, costs = L_layer_model(x, y, layers_dims, learning_rate, num_iterations, print_cost=True)
    #plot_costs(costs, learning_rate)

    d = dict()
    d['parameters'] = parameters
    d['num_px'] = num_px

    with open("models/model.pkl", 'wb') as file:
        pickle.dump(d, file)

    l.log("[{}] Done training".format(get_timestamp()))
