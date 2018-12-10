# -*- coding: utf-8 -*-
# @Time    : 18-11-29 下午10:49
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : Utils.py
# @Software: PyCharm Community Edition

import os
from PIL import Image


# 把image resize到target_weight, target_high的长度
def image_resize(image, target_weight, target_high):
    return image.resize((int(target_weight), int(target_high)), Image.ANTIALIAS)


def make_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)


def make_folders(*args):
    for each in args:
        make_folder(each)


def save_string_2_file(file_path, file_content):
    f = open(file_path, 'w')
    f.write(file_content)
    f.close()


# 得到folder文件夹下所有文件的绝对路径
def get_internal_path(folder):
    """os.path.abspath会出现错误（abspath使用的是getwd获取运行路径）"""

    def f(x):
        return os.path.join(folder, x)

    return list(map(f, os.listdir(folder)))


def get_file_name(complete_name):
    return os.path.splitext(os.path.split(complete_name)[1])[0]
