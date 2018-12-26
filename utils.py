# -*- coding: utf-8 -*-
# @Time    : 18-11-29 下午10:49
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : Utils.py
# @Software: PyCharm Community Edition

import os
from PIL import Image
import torchvision.transforms as transforms


# 把image resize到target_weight, target_high的长度
def image_resize(image, target_weight, target_high):
    return image.resize((int(target_weight), int(target_high)), Image.ANTIALIAS)


#  把image resize到边长为target_side长的正方形
#  等比例扩到最大边为target_side-padding，然后再其周围使用填充padding长度白边
def image_resize_scale(image, target_side, padding):
    (origin_w, origin_h) = image.size
    target_image = Image.new("RGBA", (target_side, target_side), (255, 255, 255))
    if origin_w >= origin_h:
        # 宽窄
        target_w = int(target_side - 2 * padding)
        mul = target_w / origin_w
        target_h = int(mul * origin_h)
        image = image_resize(image, target_w, target_h)
        target_image.paste(image, (padding, int((target_side - target_h) / 2)))
    else:
        # 短长
        target_h = target_side - 2 * padding
        mul = target_h / origin_h
        target_w = int(origin_h * mul)
        image = image_resize(image, target_w, target_h)
        target_image.paste(image, (int((target_side - target_w) / 2), padding))
    return target_image


# 两个图片的纵向拼接
def image_merge_horizontal(image1, image2):
    w1, h1 = image1.size
    w2, h2 = image2.size
    h = (h1, h2)[h1 < h2]
    image = Image.new("RGB", (w1 + w2, h))
    image.paste(image1, (0, int((h - h1) / 2)))
    image.paste(image2, (w1, int((h - h2) / 2)))
    return image


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


def image_2_tensor(pil_image):
    return transforms.ToTensor()(pil_image)


def tensor_2_image(pil_tensor):
    return transforms.ToPILImage()(pil_tensor)


import pickle


def save_pickle(path, content):
    file = open(path, 'wb')
    pickle.dump(content, file)
    file.close()


def load_pickle(path):
    with open(path, 'rb')as file:
        content = pickle.load(file)
    return content
