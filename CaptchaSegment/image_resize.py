# -*- coding: utf-8 -*-
"""
1. resize 扩大到一定之后用白色补充
"""
__author__ = 'big_centaur'

import os
from PIL import Image


def image_resize_scale(source_image, width, hight):
    """
    等比例扩大之后,再对另一边用白色填充
    """
    # image = Image.open(source)
    image = source_image
    (w, h) = image.size
    if w >= h:
        # 宽窄
        origin_w = w
        origin_h = h
        target_w = width
        target_h = width / origin_w * origin_h
        image = source_image.resize((int(target_w), int(target_h)),
                                          Image.ANTIALIAS)
        image_warp = Image.new('RGB', (width, hight), (255, 255, 255))
        tmp = (hight - int(target_h)) / 2
        image_warp.paste(image, (0, int(tmp)))
    else:
        # 短长
        origin_w = w
        origin_h = h
        target_w = hight / origin_h * origin_w
        target_h = hight
        image = source_image.resize((int(target_w), int(target_h)),
                                          Image.ANTIALIAS)
        image_warp = Image.new('RGB', (width, hight), (255, 255, 255))
        tmp = (width - int(target_w)) / 2
        image_warp.paste(image, (int(tmp), 0))
    return image_warp


def add_white_round(image, side_length):
    """
    再image的周围填充一圈白色
    """
    (w, h) = image.size
    padding_w = int((side_length - w) / 2)
    padding_h = int((side_length - h) / 2)
    image_bg = Image.new('RGB', (side_length, side_length), (255, 255, 255))
    image_bg.paste(image, (padding_w, padding_h))
    return image_bg

def image_resize(source_image, target_file, side_length):
    """
    对图片进行resize
    1:先扩大到 一定大小,为了防止网络生成的越界,再四边进行白色填充
    """
    padding = 50 # wiki_mini_
    # padding = 30 # jd 360
    # padding = 60 # sina
    # padding = 70 # wiki
    # padding = 63 # wiki_new
    # padding = 66 # wiki_or
    image = image_resize_scale(source_image, side_length - padding,
                               side_length - padding)
    image = add_white_round(image, side_length)
    image.save(target_file)



def recurve_opt_two(root_1, root_2):
    """
    递归处理root_1中的文件,然后按照同样的目录放在root_2中.
    :param root_1: 源文件夹
    :param root_2: 目标文件夹
    :return:
    """
    if not os.path.exists(root_2):
        os.makedirs(root_2)
    for file in os.listdir(root_1):
        source_file = os.path.join(root_1, file)
        target_file = os.path.join(root_2, file)
        if os.path.isfile(source_file):
            (path, extension) = os.path.splitext(source_file)
            if extension == '.jpg' or extension == '.png':
                # do something
                print("%s processing ." % source_file)
                source_image = Image.open(source_file)
                image_resize(source_image, target_file, 256)
                # image_resize_scale(source_image,28,28).save(target_file)

        else:
            recurve_opt_two(source_file, target_file)


def main():
    root_1 = '/home/tianchaoxiong/LinuxData/paper/experiment/segment/6_google/google_184_change_size_otsu'
    root_2 = root_1+'_resize'
    recurve_opt_two(root_1, root_2)


if __name__ == '__main__':
    main()
