# -*- coding: utf-8 -*-
# @Time    : 18-12-25 下午4:01
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : generate_train_test_data.py
# @Software: PyCharm

import shutil
from out_utils import *


def get_has_num(folder):
    return len(os.listdir(folder))


def generate(folder, paths, labels):
    for i, each in enumerate(labels):
        tar_folder = os.path.join(folder, str(each))
        make_folder(tar_folder)
        has_num = get_has_num(tar_folder)
        shutil.copy(paths[i], os.path.join(tar_folder, str(has_num) + '.png'))
        print(paths[i] + ' have save complete')


if __name__ == '__main__':
    source_root = '/home/tianchaoxiong/LinuxData/paper/experiment/segment/1_JD/cnn_pro/datasets/train/se_op'
    source_image_folder = os.path.join(source_root, 'train_sets_resize')
    source_labels_path = os.path.join(source_root, 'train_labels.txt')
    image_num = 10000
    target_data_set = '/home/tianchaoxiong/LinuxData/code/pythonpro/MasterExp/IdentifiNetwork/data_sets'
    target_mode = 'train'
    target_folder = os.path.join(target_data_set, 'jd', target_mode)
    make_folder(target_folder)
    labels = open(source_labels_path, 'r', encoding="utf-8").read().strip().split('#')
    if len(labels) < image_num:
        image_num = len(labels)
    labels = labels[:image_num]
    image_paths = [os.path.join(source_image_folder, str(i) + '.png') for i in range(image_num)]

    # Image.open(image_paths[0]).show()
    # print(labels[0])
    # Image.open(image_paths[-1]).show()
    # print(labels[-1])
    generate(target_folder, image_paths, labels)
