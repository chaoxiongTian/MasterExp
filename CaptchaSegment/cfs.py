# -*- coding: utf-8 -*-
"""
1. cfs分割算法
"""
__author__ = 'MaxCentaur'
from PIL import Image


def convert_binarization(image, threshold):
    """
    :param image: 需要进行二值化的图片
    :return: 二值化之后的图片
    """
    (image_w, image_h) = image.size
    pixdata = image.load()
    for iter_y in range(image_h):
        for iter_x in range(image_w):
            if pixdata[iter_x, iter_y] < threshold:
                pixdata[iter_x, iter_y] = 0
            else:
                pixdata[iter_x, iter_y] = 255
    return image


def traverse_image(string, image):
    """
    遍历image
    :param image:  需要遍历的image
    :return: null
    """
    print("%s" % string)
    pixdata = image.load()
    (image_w, image_h) = image.size
    for iter_y in range(image_h):
        for iter_x in range(image_w):
            if pixdata[iter_x, iter_y] == 255:
                print(0, end='')
            elif pixdata[iter_x, iter_y] == 0:
                print(1, end='')
        print(end='\n')


def is_collected(black_block_list, falg_x, falg_y):
    """
    判断 falg_x 和 falg_y 是否已经收集再black_block_list中.
    black_block_list 是一个三维数组 [[[x1,y1],[x2,y2],[x3,y3]],[[x1,y1],[x2,y2],[x3,y3]]]这种形式
    :param black_block_list: 需要遍历的三维数组
    :param falg_x: 查找的x
    :param falg_y: 查找的y
    :return: 是否包含
    """
    for each in black_block_list:
        for iter_x, iter_y in each:
            if iter_x == falg_x and iter_y == falg_y:
                return True
    return False


def get_connect_pixdata(image, flag_x, flag_y, value):
    """
    根据提供的 flag_x,flag_y对像素相同的连通域进行遍历
    :param image: 需要遍历的image
    :param flag_x: 遍历的起始点
    :param flag_y: 遍历的起始点
    :param value: 用来填充的颜色
    :return: 黑色色块列表
    """
    block = []
    pixdata = image.load()
    try:
        background = pixdata[flag_x, flag_y]
        if background == value:
            return  # 起始点的颜色已经填充
        pixdata[flag_x, flag_y] = value
    except (ValueError, IndexError):
        return  # seed point outside image
    edge = [(flag_x, flag_y)]
    block.append([flag_x, flag_y])
    while edge:
        newedge = []
        for (iter_x, iter_y) in edge:
            for (tmp_s, tmp_t) in ((iter_x + 1, iter_y), (iter_x - 1, iter_y),
                                   (iter_x, iter_y + 1), (iter_x, iter_y - 1)):
                try:
                    pixel = pixdata[tmp_s, tmp_t]
                except IndexError:
                    pass
                else:
                    if pixel == background:
                        pixdata[tmp_s, tmp_t] = value
                        block.append([tmp_s, tmp_t])
                        newedge.append((tmp_s, tmp_t))
        edge = newedge
    return block


def get_black_block(image):
    """
    使用连通域算法 根据二值化之后的图片 得到黑色块的列表
    :param image: 需要遍历的image
    :return: 黑色色块列表
    """
    pixdata = image.load()
    (image_w, image_h) = image.size
    black_block_list = []
    for iter_x in range(image_w):
        for iter_y in range(image_h):
            if pixdata[iter_x, iter_y] == 0:
                # 遍历的时候找到黑色像素,判断是否已经收集在black_block_list中,若在跳过,不在则用这个点开始遍历和他联通的部分.
                if is_collected(black_block_list, iter_x, iter_y):
                    pass
                else:
                    # 按照这个点开始 连通域遍历.
                    block = get_connect_pixdata(image, iter_x, iter_y,
                                                127)  # 此算法可做颜色填充算法
                    if len(block) > 10:
                        black_block_list.append(block)
    return black_block_list


def get_boundary(block, axit):
    """
    得到区块的长和宽 和长宽起始的位置
    :param block: 存储的位置
    :param axit: 宽是0 长是1
    :return: 宽和宽的起始位置 或者长和长的起始位置
    """
    s2b_list = sorted(block, key=lambda x: x[axit])
    b2s_list = sorted(block, key=lambda x: x[axit], reverse=True)
    return b2s_list[0][axit] - s2b_list[0][axit], s2b_list[0][axit]


def get_block_info(block):
    """
    得到block的长宽和长的最小开始坐标和宽的最小开始坐标
    :param block: block 形式为[[x1,y1],[x2,y2],[x3,y3]]
    :return: block_w,w_min_begin_point,block_h,h_min_begin_point
    """
    block_w, w_min_begin_point = get_boundary(block, 0)
    block_h, h_min_begin_point = get_boundary(block, 1)
    return block_w, w_min_begin_point, block_h, h_min_begin_point


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
        im_origin = Image.new('RGB', (block_w + 1, block_h + 1),
                              (255, 255, 255))
        image_threshold_new = convert_binarization(im_origin.convert("L"), 220)
        pixdata_new = image_threshold_new.load()
        for tmp_m, tmp_n in each_block:
            pixdata_new[tmp_m - w_min_begin_point,
                        tmp_n - h_min_begin_point] = 0
        image_threshold_new.save(sava_folder + '-' + str(i) + ".png")
        # print(sava_folder + '-' + str(i) + ".png" + ' saved...')
    return 0


def cfs(file_path, sava_folder):
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
    # 4. 保存色块
    save_segmented_image_list(segmented_pixel_list, sava_folder)


def main():
    """
    :return: 入口
    """
    file_path = '/media/tianchaoxiong/BIG_CENTAUR/图1/3_5.png'
    sava_folder = '/media/tianchaoxiong/BIG_CENTAUR/图1/'
    cfs(file_path, sava_folder)


if __name__ == '__main__':
    main()
