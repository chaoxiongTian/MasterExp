# -*- coding: utf-8 -*-
"""
1. 对cfs分割之后的结果使用滴水算法再次进行分割
"""
__author__ = 'big_centaur'
import os
from PIL import Image
from cfs import convert_binarization
from cfs import get_black_block
from cfs import get_block_info
from cfs_update1 import fix_segented_image



def sava_block(block_w, w_min_begin_point, block_h, h_min_begin_point, block,
               save_path):
    """
    对每个区块进行存储
    """
    im_origin = Image.new('RGB', (block_w + 1, block_h + 1), (255, 255, 255))
    image_threshold_new = convert_binarization(im_origin.convert("L"), 220)
    pixdata_new = image_threshold_new.load()
    for tmp_m, tmp_n in block:
        pixdata_new[tmp_m - w_min_begin_point, tmp_n - h_min_begin_point] = 0
    image_threshold_new.save(save_path)
    print(save_path + ' saved...')


def compare_and_save(index, block_w, w_min_begin_point, block_h,
                     h_min_begin_point, each_block, sava_folder):
    """
    先比较长宽,再进行存储.若长度为一个字符,则直接存储.若长度大于一个字符,则暂时存储,之后通过滴水算法进行切分.
    """
    width = block_w
    # 通过阈值 计算应该分为几份.
    if width < 58:  # sina #tmp2
        print("按照一份分割")
        save_path = sava_folder + '-' + str(index) + ".png"
        sava_block(block_w, w_min_begin_point, block_h, h_min_begin_point,
                   each_block, save_path)
    else:
        print("按照多份分割")
        save_path = sava_folder + '-' + str(index) + ".png"
        tmp_folder = os.path.dirname(save_path) + '/' + 'tmp'
        if not os.path.exists(tmp_folder):
            os.makedirs(tmp_folder)
        tmp_path = tmp_folder + '/' + save_path.split('/')[-1]
        sava_block(block_w, w_min_begin_point, block_h, h_min_begin_point,
                   each_block, tmp_path)
        from projection_update1 import projection
        from dropfall import dropfall
        dropfall(tmp_path, sava_folder + '-' + str(index))


def save_segmented_image_list(segmented_image_list, sava_folder):
    """
    :param segmented_image_list: 需要存储的list
    :param sava_folder: 存储的位置
    :return:
    """
    for i, each_block in enumerate(segmented_image_list):
        # 获取每个区块的长宽 和长宽的其实起始位置
        block_w, w_min_begin_point, block_h, h_min_begin_point = get_block_info(
            each_block)
        # 先判断长度,再根据长度进行存储. 若为1直接存储.若大于1,暂时存储,再使用滴水算法进行分割.

        compare_and_save(i, block_w, w_min_begin_point, block_h,
                         h_min_begin_point, each_block, sava_folder)


def cfs_dropfall(file_path, sava_folder):
    """
    连通域分割算法
    :param file_path: image存储路劲
    :param sava_folder: 存储位置
    :return: 分割之后的数组
    """
    image = Image.open(file_path)
    # 1. 转为灰度图像
    image = image.convert('L')
    # 2. 二值化图像
    threshold = 220
    image = convert_binarization(image, threshold)
    # traverse_image("image_binarizat", image)
    # 3. 获取色块
    segmented_pixel_list = get_black_block(image)
    print("block length is : %d" % len(segmented_pixel_list))
    # 4. 对一些特殊的情况进行修补
    segmented_pixel_list = fix_segented_image(segmented_pixel_list)
    # 5. 保存色块
    save_segmented_image_list(segmented_pixel_list, sava_folder)


def main():
    """
    :return: null
    """
    file_path = '/home/tianchaoxiong/LinuxData/paper/experiment/chaoxiong/wiki/use_to_train_data3/result/result_200/2.png'
    sava_folder = '../data/2'
    cfs_dropfall(file_path, sava_folder)


if __name__ == '__main__':
    main()
