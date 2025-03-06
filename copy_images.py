import os
import glob
import shutil
import random
import string


def copy_image_files(src_dir, dst_dir, num):
    image_files = glob.glob(os.path.join(src_dir, '*.j*g'), recursive=False)
    print(src_dir, len(image_files))

    if len(image_files) > num:
        image_files = random.sample(image_files, num)

    for f in image_files:
        src_file = os.path.basename(f)
        file_extension = os.path.splitext(f)[1]
        dst_file = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10)) + file_extension

        src = os.path.join(src_dir, src_file)
        dst = os.path.join(dst_dir, dst_file)

        shutil.copy2(src, dst)

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
    copy_examples('train', pos=9000, neg=1000)
    copy_examples('cv',    pos=500, neg=20)
    copy_examples('test',  pos=500, neg=20)
