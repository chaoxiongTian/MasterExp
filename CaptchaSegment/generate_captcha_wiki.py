# -*- coding: utf-8 -*-
"""
1. 再cfs的基础上生成wiki的验证码
"""
__author__ = 'big_centaur'
import os
import random
import shutil
from PIL import Image
from cfs import convert_binarization
from cfs import get_black_block
from cfs import save_segmented_image_list
from cfs import get_block_info
from cfs_update1 import fix_segented_image
from image_resize import image_resize

def mkdir(path):
    """
    判断文件夹是不是存在,不存在创建
    """
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        pass


def save_wiki_captcha(segmented_image_list, sava_folder_1, sava_folder_2,
                      image):
    """
    block_w, w_min_begin_point,
    :param segmented_image_list: 需要存储的list
    :param sava_folder: 存储的位置
    :return:
    """
    (image_w, image_h) = image.size
    im_origin = Image.new('RGB', (image_w, image_h), (255, 255, 255))
    image_threshold_new = convert_binarization(im_origin.convert("L"), 220)
    offset_info = [
        get_block_info(each_block) for each_block in segmented_image_list
    ]
    start = offset_info[0][1]
    start_2 = offset_info[0][1]
    step = 1
    step_2 = 4
    # 计算距离
    offset_each = []
    sum_w = start
    for each in offset_info:
        off = random.randint(0, 3)
        offset_each.append(off)
        sum_w = sum_w + each[0] + step_2 + off
    if sum_w > image_w:
        image_threshold_new = image_threshold_new.resize((sum_w, image_h),
                                                         Image.ANTIALIAS)
    image_threshold_new_2 = image_threshold_new.copy()
    pixdata_new = image_threshold_new.load()
    pixdata_new_2 = image_threshold_new_2.load()
    for i, each_block in enumerate(segmented_image_list):
        for tmp_m, tmp_n in each_block:
            pixdata_new[start + (tmp_m - offset_info[i][1]), tmp_n] = 0
            pixdata_new_2[start_2 + (tmp_m - offset_info[i][1]), tmp_n] = 0
        start = start + offset_info[i][0] + step + offset_each[i]
        start_2 = start_2 + offset_info[i][0] + step_2 + offset_each[i]
    # image_threshold_new.save(sava_folder_1)
    image_resize(image_threshold_new, sava_folder_1, 256)
    # image_threshold_new_2.save(sava_folder_2)
    image_resize(image_threshold_new_2, sava_folder_2, 256)


def create_wiki_captcha(file_path, sava_folder_1, sava_folder_2):
    """
    连通域分割算法
    :param file_path: image存储路劲
    :param sava_folder: 存储路径
    :return: 分割之后的数组
    """
    file_name = file_path.split('/')[-1]
    image = Image.open(file_path)
    # 1. 转为灰度图像
    image = image.convert('L')
    # 2. 二值化图像
    threshold = 220
    image = convert_binarization(image, threshold)
    # traverse_image("image_binarizat", image)
    segmented_pixel_list = get_black_block(image)
    print("block length is : %d" % len(segmented_pixel_list))
    # 对一些特殊的情况进行修补
    segmented_pixel_list = fix_segented_image(segmented_pixel_list)
    segmented_pixel_list = fix_segented_image(segmented_pixel_list)
    # segmented_pixel_list 得到的色块数组
    save_wiki_captcha(segmented_pixel_list,
                      os.path.join(sava_folder_1, file_name),
                      os.path.join(sava_folder_2, file_name), image)


def get_image_name(folder):
    """
    返回所有文件的绝对路径
    """
    file_name_list = []
    for file in os.listdir(folder):
        file_name_list.append(os.path.join(folder, file))
    return file_name_list


def main():
    """
    :return: 入口
    """
    file_folder = '/home/tianchaoxiong/LinuxData/paper/experiment/segment/9_wiki/pix_pro/dataset_update/se_op/image_6040_order'
    sava_folder_1 = '/home/tianchaoxiong/LinuxData/paper/experiment/segment/9_wiki/pix_pro/dataset_update/se_op/train/A/train'
    sava_folder_2 = '/home/tianchaoxiong/LinuxData/paper/experiment/segment/9_wiki/pix_pro/dataset_update/se_op/train/B/train'
    mkdir(sava_folder_1)
    mkdir(sava_folder_2)
    for i, each in enumerate(get_image_name(file_folder)):
        print(i)
        create_wiki_captcha(each, sava_folder_1, sava_folder_2)


if __name__ == '__main__':
    main()
