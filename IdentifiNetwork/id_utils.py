# -*- coding: utf-8 -*-
# @Time    : 18-12-25 上午9:49
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : id_utils.py
# @Software: PyCharm

import argparse
from out_utils import *
from torchvision import datasets
import torch.utils.data as Data


# 返回data_loader
def return_loader(options):
    data_set = options.data_set_folder
    name = options.model_name
    batch_size = options.batch_size
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Gray()
    ])
    loader = dict()
    train_folder = os.path.join(os.path.dirname(__file__), data_set, name, 'train')
    test_folder = os.path.join(os.path.dirname(__file__), data_set, name, 'test')
    train_data = datasets.ImageFolder(root=train_folder, transform=transform)
    test_data = datasets.ImageFolder(root=test_folder, transform=transform)
    train_loader = Data.DataLoader(train_data, batch_size=batch_size, shuffle=True)
    test_loader = Data.DataLoader(test_data, batch_size=batch_size, shuffle=False)
    loader['train'] = train_loader
    loader['test'] = test_loader
    return loader


# 返回 预分类的类别
def return_y_dim(folder):
    return len(os.listdir(os.path.join(folder, 'train')))


# 一般的tensor转为cuda的tensor
def cuda(tensor, is_cuda):
    if is_cuda:
        return tensor.cuda()
    else:
        return tensor


# 把str转为bool
def str2bool(v):
    # codes from : https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse

    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_set_folder', type=str, default='data_sets')
    parser.add_argument('--model_name', type=str, default='d_mnist')
    parser.add_argument('--batch_size', type=int, default=64)
    args = parser.parse_args()
    data_loader = return_loader(args)
    train_loader = data_loader['train']
    test_loader = data_loader['test']

    print('train data shape')
    for i, (image, labels) in enumerate(train_loader):
        if i == 1:
            break
        print(image.size())
        print(labels.size())
    print('test data shape')
    for i, (image, labels) in enumerate(test_loader):
        if i == 1:
            break
        print(image.size())
        print(labels.size())
