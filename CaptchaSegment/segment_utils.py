# -*- coding: utf-8 -*-
# @Time    : 18-12-7 下午4:55
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : segment_utils.py
# @Software: PyCharm

from utils import *


#  转灰度
def convert_gray(im):
    return im.convert("L")


# 转二值化
def convert_binary(im, threshold=127):
    im = convert_gray(im)
    (image_w, image_h) = im.size
    pix_data = im.load()
    for iter_y in range(image_h):
        for iter_x in range(image_w):
            if pix_data[iter_x, iter_y] < threshold:
                pix_data[iter_x, iter_y] = 0
            else:
                pix_data[iter_x, iter_y] = 255
    return im


# 把像素按照0和1的形式打印出来（此操作必须先二值化） （0表示白色 1表示黑色）
def image_traverse(im):
    pix_data = im.load()
    (image_w, image_h) = im.size
    for iter_y in range(image_h):
        for iter_x in range(image_w):
            if pix_data[iter_x, iter_y] == 255:
                print(0, end='')
            elif pix_data[iter_x, iter_y] == 0:
                print(1, end='')
        print(end='\n')


# 按照宽度排序 重新命名
def sort_rename_images(source_folder, target_folder):
    make_folder(target_folder)
    image_paths = get_internal_path(source_folder)
    images_info = []
    for each in image_paths:
        image = Image.open(each)
        images_info.append([image, image.size[0]])
    images_info = sorted(images_info, key=lambda x: x[1])
    for i, (each, _) in enumerate(images_info):
        target_path = os.path.join(target_folder, str(i) + '.png')
        print(target_path)
        each.save(target_path)

# source_folder = '/home/tianchaoxiong/LinuxData/data/MasterExpData/after/qq/results_85/images_cfs'
# target_folder = source_folder + '_range'
# sort_rename_images(source_folder, target_folder)
