# -*- coding: utf-8 -*-
"""
1. cfs分割算法
2. update1:添加i,j的点修复函数 修复方案:更具垂直方向的重合率,若多余0.6和对两个连续的区块进行合并.
"""
__author__ = 'big_centaur'
from PIL import Image
from cfs import convert_binarization
from cfs import get_black_block
from cfs import save_segmented_image_list


def get_boundary_start_end(block, axit):
    """
    得到区块的长和宽 和长宽起始的位置
    :param block: 存储的位置
    :param axit: 宽是0 长是1
    :return: 宽的起始位置和结束位置
    """
    s2b_list = sorted(block, key=lambda x: x[axit])
    return s2b_list[0][axit], s2b_list[-1][axit]


def get_rate(start1, end1, start2, end2):
    """
    获取(start1, end1),(start2, end2)的重合率
    """
    if (start2 > end1 or start1 > end2):
        return 0
    if (start1 > start2 and end1 < end2):
        return 1
    if (start2 > start1 and end2 < end1):
        return 1
    len_min = ((end1 - start1)
               if (end1 - start1) < (end2 - start2) else (end2 - start2)) + 1
    return (min(abs(end1 - start2), abs(end2 - start1)) + 1) / len_min


def get_overlape_rate(block1, block2):
    """
    返回 list1 和list2 垂直方向的重合率 list1形式为[[x1,y1],[x2,y2],[x3,y3]]
    """
    # 1, 找出list1,list2 再垂直方向上的其实和终止位置.
    start1, end1 = get_boundary_start_end(block1, 0)
    start2, end2 = get_boundary_start_end(block2, 0)
    # 2. 根据区间找到重合率
    rate = get_rate(start1, end1, start2, end2)
    # print("rate = %d"%rate)
    return rate


def get_block_overlape_rate(segmented_image_list):
    """
    计算连续的两个联通的区块再垂直方向的重合率
    :param segmented_image_list: 需要计算的blocklist
    :return: 长度减一的list
    """
    overlape_list = []
    for i in range(len(segmented_image_list) - 1):
        # print('tmp i is :'+str(i))
        overlape_list.append(
            get_overlape_rate(segmented_image_list[i],
                              segmented_image_list[i + 1]))
    # print("here is :")
    # print(overlape_list)
    if len(overlape_list) == 0:
        return overlape_list
    tmp_list = [overlape_list[0]]
    for i in range(1, len(overlape_list)):
        if overlape_list[i - 1] > 0.4:
            tmp_list.append(0)
        else:
            tmp_list.append(overlape_list[i])
    return tmp_list


def combine_block(segmented_image_list, overlape_rate_list, threshold):
    """
    合并垂直方向重合率比较大的block
    :param segmented_image_list: block list
    :param overlape_rate_list: 重合率
    :return: 修改之后的segmented_image_list信息
    """
    switch = 0
    # print(overlape_rate_list)
    segmented_image_list_new = []
    for i in range(len(segmented_image_list)):
        if i == len(segmented_image_list) - 1:
            tmp_list = segmented_image_list[i]
            if switch == 0:
                segmented_image_list_new.append(tmp_list)
            break
        if overlape_rate_list[i] >= threshold:
            tmp_list = segmented_image_list[i] + segmented_image_list[i + 1]
            segmented_image_list_new.append(tmp_list)
            switch = 1
        else:
            if switch == 1:
                switch = 0
            else:
                tmp_list = segmented_image_list[i]
                segmented_image_list_new.append(tmp_list)

    return segmented_image_list_new


def fix_segented_image(segmented_image_list):
    """
    对切分出来的连通域 进行一点修补,比如把 i 的小点加上
    :param segmented_image_list: 连通域pixel坐标信息
    :return: 修改之后的segmented_image_list信息
    """
    # 1:计算连续的两个联通的区块再垂直方向的重合率
    overlape_rate_list = get_block_overlape_rate(segmented_image_list)
    # print(overlape_rate_list)
    # 2:对重合率大于0.4的区块进行合并.
    segmented_image_list = combine_block(segmented_image_list,
                                         overlape_rate_list, 0.3)
    return segmented_image_list


def cfs(file_path, sava_folder):
    """
    连通域分割算法
    :param file_path: image存储路劲
    :param sava_folder: 存储路径
    :return: 分割之后的数组
    """
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
    
    (path, _) = os.path.splitext(file_path)
    sava_folder =sava_folder+str(path).split('/')[-1]
    save_segmented_image_list(segmented_pixel_list, sava_folder)

import os
def cfs_no_save(file_path):
    """
    连通域分割算法
    :param file_path: image存储路劲
    :param sava_folder: 存储路径
    :return: 分割之后的数组
    """
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
    return segmented_pixel_list,len(segmented_pixel_list)

def cfs_folder(folder_path,sava_folder):
    for i, file in enumerate(os.listdir(folder_path)):
        source_file = os.path.join(folder_path, file)
        cfs(source_file, sava_folder)
def main():
    """
    :return: 入口
    """
    file_path = '/media/tianchaoxiong/BIG_CENTAUR/图1/3_5.png'
    sava_folder = '/media/tianchaoxiong/BIG_CENTAUR/图1/'
    # file_path = '/home/tianchaoxiong/LinuxData/paper/experiment/segment/4_live/cnn_pro/dataset/ceshi/0.png'
    # folder_path = '/home/tianchaoxiong/LinuxData/paper/experiment/segment/4_live/cnn_pro/dataset/ceshi'
    # sava_folder = '/home/tianchaoxiong/LinuxData/paper/experiment/segment/4_live/cnn_pro/dataset/ceshi_2/'
    # cfs_folder(folder_path,sava_folder)
    cfs(file_path, sava_folder)


if __name__ == '__main__':
    main()
