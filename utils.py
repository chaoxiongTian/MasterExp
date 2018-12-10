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


# 创建一个文件夹
def make_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)


# 创建一组文件夹
def make_folders(*args):
    for each in args:
        make_folder(each)


# 把string保存到指定的文件中
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


def get_file_folder(complete_name):
    return os.path.split(complete_name)[0]


def get_file_suffix(complete_name):
    return os.path.splitext(complete_name)[-1]


# 由文件路径获得文件名
def get_file_path_info(complete_name):
    return get_file_folder(complete_name), get_file_name(complete_name), get_file_suffix(complete_name)
