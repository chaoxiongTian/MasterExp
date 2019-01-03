# -*- coding: utf-8 -*-
# @Time    : 18-12-20 下午5:05
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : save_mnist_image.py
# @Software: PyCharm

import torchvision
from out_utils import *
from torchvision import transforms


def download_each(target_folder, data, label):
    # 往 train或者test的目录下面创建1 2 3 之类的文件夹 然后再将对应的图片存入。
    # TODO: 1 看对应类别文件是否存在  2 计算其中数据 3 存入
    # print(target_folder, label, i)
    target_folder = os.path.join(target_folder, str(label))
    make_folder(target_folder)

    items_num = len(os.listdir(target_folder))
    image = tensor_2_image(data).convert('L')
    image.save(os.path.join(target_folder, str(items_num) + '.jpg'))


def cus_download(target_folder, index, image_tensor):
    image_path = os.path.join(target_folder, str(index) + '.png')
    print(image_path, 'is saved .')
    tensor_2_image(image_tensor).convert('L').save(image_path)


def download_data(target_folder, data, num, flag):
    labels = []
    for i in range(num):
        if flag == 'train':
            save_data = data.train_data[i].unsqueeze(dim=0)
            label = data.train_labels[i].item()
        else:
            save_data = data.test_data[i].unsqueeze(dim=0)
            label = data.test_labels[i].item()
        # pytorch dataloader的形式保存文件
        # download_each(target_folder, save_data, label)
        cus_download(target_folder, i, save_data)
        labels.append(str(label))
    labels_path = os.path.join(target_folder, flag + '_labels.txt')
    save_string_2_file(labels_path, '#'.join(labels))


def download(train_data, test_data, train_num, test_num):
    target_train_folder = os.path.join(data_folder, "train")
    target_test_folder = os.path.join(data_folder, "test")
    make_folders(target_train_folder, target_test_folder)

    download_data(target_train_folder, train_data, train_num, 'train')
    download_data(target_test_folder, test_data, test_num, 'test')


def main():
    train_data = torchvision.datasets.MNIST('./data_sets/mnist/', True, transforms.Compose(transforms.ToTensor()),
                                            False)
    test_data = torchvision.datasets.MNIST('./data_sets/mnist/', False, transforms.Compose(transforms.ToTensor()),
                                           False)
    train_num = 1000
    test_num = 100
    download(train_data, test_data, train_num, test_num)


if __name__ == '__main__':
    main()
