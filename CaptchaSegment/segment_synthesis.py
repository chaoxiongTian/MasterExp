# -*- coding: utf-8 -*-
# @Time    : 18-12-11 下午7:46
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : segment_cfs_drop.py
# @Software: PyCharm
from PIL import Image
from segment_cfs import cfs
from segment_drop import drop
from segment_projection import projection


def cfs_projection(file_path, pre_conditions=(30, 60, 90)):
    images = cfs(file_path)
    new_images = []
    for each in images:
        new_images = new_images + projection(each, pre_conditions)
    return new_images


def cfs_drop(file_path, pre_conditions=(30, 60, 90)):
    images = cfs(file_path)
    new_images = []
    for each in images:
        new_images = new_images + drop(each, pre_conditions)
    return new_images


# file_path = '/home/tianchaoxiong/LinuxData/data/MasterExpData/after/qq/results_85/images/56.png'
# images = cfs_drop(Image.open(file_path), pre_conditions=[67, 106, 134])
# for each in images:
#     each.show()
