import os
import glob
import shutil
import random
import string
from PIL import Image
from utils import *


def copy_image_files(src_dir, dst_dir, num):
    cfg = get_configs()
    num_px = cfg['image']['num_px']

    image_files = glob.glob(os.path.join(src_dir, '*.j*g'), recursive=False)
    print(src_dir, len(image_files))

    if len(image_files) > num:
        image_files = random.sample(image_files, num)

    i = 0
    for f in image_files:
        i += 1
        if i > num:
            break

        src_file = os.path.basename(f)
        file_extension = '.jpeg'
        dst_file = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10)) + file_extension

        src = os.path.join(src_dir, src_file)
        dst = os.path.join(dst_dir, dst_file)

        image = Image.open(src)
        image = image.resize((num_px, num_px))
        image.save(dst)


def cleanup_images_folder():

    try:
        shutil.rmtree(os.path.join(os.getcwd(), 'datasets/images/train/positive'))
        shutil.rmtree(os.path.join(os.getcwd(), 'datasets/images/train/negative'))
        shutil.rmtree(os.path.join(os.getcwd(), 'datasets/images/cv/positive'))
        shutil.rmtree(os.path.join(os.getcwd(), 'datasets/images/cv/negative'))
        shutil.rmtree(os.path.join(os.getcwd(), 'datasets/images/test/positive'))
        shutil.rmtree(os.path.join(os.getcwd(), 'datasets/images/test/negative'))
    except:
        pass

    os.makedirs(os.path.join(os.getcwd(), 'datasets/images/train/positive'))
    os.makedirs(os.path.join(os.getcwd(), 'datasets/images/train/negative'))
    os.makedirs(os.path.join(os.getcwd(), 'datasets/images/cv/positive'))
    os.makedirs(os.path.join(os.getcwd(), 'datasets/images/cv/negative'))
    os.makedirs(os.path.join(os.getcwd(), 'datasets/images/test/positive'))
    os.makedirs(os.path.join(os.getcwd(), 'datasets/images/test/negative'))


def copy_examples(mode, pos, neg):
    pos_examples = [
        'cat'
    ]
    neg_examples = [
        'butterfly',
        'chicken',
        'cow',
        'dog',
        'elephant',
        'horse',
        'sheep',
        'spider',
        'squirrel'
    ]

    for ex in pos_examples:
        srcdir = '/Users/macmini/Downloads/archives/animals/' + ex
        dstdir = '/Users/macmini/PycharmProjects/DeepObjectClassifier/datasets/images/' + mode + '/positive'
        copy_image_files(srcdir, dstdir, pos)

    for ex in neg_examples:
        srcdir = '/Users/macmini/Downloads/archives/animals/' + ex
        dstdir = '/Users/macmini/PycharmProjects/DeepObjectClassifier/datasets/images/' + mode + '/negative'
        copy_image_files(srcdir, dstdir, neg)


if __name__ == '__main__':
    cleanup_images_folder()
    copy_examples('train', pos=9000, neg=200)
    copy_examples('cv',    pos=100,  neg=20)
    copy_examples('test',  pos=100,  neg=20)
