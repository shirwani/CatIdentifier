from utils import *
import pickle
import h5py
import json
import sys

l = logger()

def L_layer_model(X, Y, layers_dims, learning_rate, num_iterations, print_cost=False):
    costs = []  # keep track of cost
    parameters = initialize_parameters_deep(layers_dims)
    for i in range(0, num_iterations):
        AL, caches = L_model_forward(X, parameters)
        cost = compute_cost(AL, Y)
        grads = L_model_backward(AL, Y, caches)
        parameters = update_parameters(parameters, grads, learning_rate)

        # Print the cost every 10 iterations
        if i % 10 == 0 or i == num_iterations:
            l.log("[{}] Cost after iteration {}/{}: {}".format(get_timestamp(), i, num_iterations, np.squeeze(cost)))
            if print_cost:
                costs.append(cost)
    # Final cost
    l.log("[{}] Final cost after {} iterations: {}".format(get_timestamp(), num_iterations, np.squeeze(cost)))

    return parameters, costs


if __name__ == '__main__':
    dev = False
    if len(sys.argv) > 1:
        if sys.argv[1] == '-dev' or sys.argv[1] == '--dev':
            dev = True

    cfg = get_configs(dev)
    data_file       = cfg['training']['data_file']
    learning_rate   = cfg['training']['learning_rate']
    num_iterations  = cfg['training']['num_iterations']
    log_file        = cfg['training']['log_file']
    num_px          = cfg['image']['num_px']
    layers          = cfg['model']['layers']

    dataset = h5py.File(data_file, "r")
    x_orig = np.array(dataset["x"][:])
    y_orig = np.array(dataset["y"][:])
    x = x_orig.reshape(x_orig.shape[0], -1).T / 255.
    y = np.reshape(y_orig, (1, y_orig.shape[0]))

    n_x = num_px * num_px * 3
    layers_dims = [n_x] + layers
    print(f"Layers: {layers_dims}")

    l.set_logfile(log_file)
    l.log("[{}] Initiating training".format(get_timestamp()))

    parameters, costs = L_layer_model(x, y, layers_dims, learning_rate, num_iterations, print_cost=True)
    #plot_costs(costs, learning_rate)

    d = dict()
    d['parameters'] = parameters
    model = 'm_' + get_date_time_str() + '.pkl'
    with open("models/" + model , 'wb') as file:
        pickle.dump(d, file)

    l.log("[{}] Done training".format(get_timestamp()))
