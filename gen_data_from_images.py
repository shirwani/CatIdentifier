import glob
import h5py
from utils import *

cfg = get_configs()
num_px = cfg['image']['num_px']

def load_img_files(folder_path, x, y, y_val):
    jpg_files = glob.glob(os.path.join(folder_path, '*.*'), recursive=False)

    i = 0
    for jpg_file in jpg_files:
        i += 1
        if i > 10000:
            continue
        try:
            img = img_to_matrix(jpg_file, num_px)
            x.append(img)
            y.append(y_val)
        except:
            print(jpg_file)

    return x, y


def create_data_file(mode, pos_examples, neg_examples):
    print(f"\nCreating {mode} set...\n")
    x = []
    y = []
    x, y = load_img_files(pos_examples, x, y, 1)
    x, y = load_img_files(neg_examples, x, y, 0)
    x = np.array(x)
    y = np.array(y)
    print("x.shape: " + str(x.shape))
    print("y.shape: " + str(y.shape))

    with h5py.File('datasets/'+ mode +'.h5', 'w') as file:
        file.create_dataset('x', data=x)
        file.create_dataset('y', data=y)

    load_back_and_check_data(mode)


def load_back_and_check_data(mode):
    print(f"\nLoading back {mode} set...\n")

    dataset = h5py.File('datasets/' + mode + '.h5', "r")
    x = np.array(dataset["x"][:])
    y = np.array(dataset["y"][:])
    print("x.shape: " + str(x.shape))
    print("y.shape: " + str(y.shape))
    print("y: " + str(y))


if __name__ == '__main__':
    create_data_file('train', 'datasets/images/train/positive', 'datasets/images/train/negative')
    create_data_file('cv',    'datasets/images/cv/positive',    'datasets/images/cv/negative')
    create_data_file('test',  'datasets/images/test/positive',  'datasets/images/test/negative')
