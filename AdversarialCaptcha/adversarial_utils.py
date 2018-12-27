# -*- coding: utf-8 -*-
# @Time    : 18-12-21 下午10:37
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : adversarial_utils.py
# @Software: PyCharm

import argparse
import torch
from pathlib import Path

import os

from torch import nn
from torch.autograd import Variable


def find_classes(folder):
    classes = [d for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d))]
    classes.sort()
    class_to_idx = {classes[i]: i for i in range(len(classes))}
    idx_to_class = {j: classes[j] for j in range(len(classes))}
    return classes, class_to_idx, idx_to_class


def is_image_file(filename):
    IMG_EXTENSIONS = [
        '.jpg', '.JPG', '.jpeg', '.JPEG',
        '.png', '.PNG', '.ppm', '.PPM', '.bmp', '.BMP',
    ]
    return any(filename.endswith(extension) for extension in IMG_EXTENSIONS)


# 获得loader的数据顺序
def make_dataset(folder, class_to_idx):
    images = []
    for target in os.listdir(folder):
        d = os.path.join(folder, target)
        if not os.path.isdir(d):
            continue
        for root, _, fnames in sorted(os.walk(d)):
            for fname in fnames:
                if is_image_file(fname):
                    path = os.path.join(root, fname)
                    item = (path, target, class_to_idx[target])
                    images.append(item)
    return images


class One_Hot(nn.Module):
    # from :
    # https://lirnli.wordpress.com/2017/09/03/one-hot-encoding-in-pytorch/
    def __init__(self, depth):
        super(One_Hot, self).__init__()
        self.depth = depth
        self.ones = torch.sparse.torch.eye(depth)

    def forward(self, X_in):
        X_in = X_in.long()
        return Variable(self.ones.index_select(0, X_in.data))

    def __repr__(self):
        return self.__class__.__name__ + "({})".format(self.depth)


def cuda(tensor, is_cuda):
    if is_cuda:
        return tensor.cuda()
    else:
        return tensor


def str2bool(v):
    # codes from : https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse

    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def print_network(net):
    num_params = 0
    for param in net.parameters():
        num_params += param.numel()
    print(net)
    print('Total number of parameters: %d' % num_params)


def rm_dir(dir_path, silent=True):
    p = Path(dir_path).resolve()
    if (not p.is_file()) and (not p.is_dir()):
        print('It is not path for file nor directory :', p)
        return

    paths = list(p.iterdir())
    if (len(paths) == 0) and p.is_dir():
        p.rmdir()
        if not silent: print('removed empty dir :', p)

    else:
        for path in paths:
            if path.is_file():
                path.unlink()
                if not silent: print('removed file :', path)
            else:
                rm_dir(path)
        p.rmdir()
        if not silent: print('removed empty dir :', p)


def where(cond, x, y):
    """
    code from :
        https://discuss.pytorch.org/t/how-can-i-do-the-operation-the-same-as-np-where/1329/8
    """
    cond = cond.float()
    return (cond * x) + ((1 - cond) * y)


# 返回 预分类的类别
def return_y_dim(folder):
    return len(os.listdir(os.path.join(folder, 'train')))
