# -*- coding: utf-8 -*-
# @Time    : 18-12-6 下午9:52
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : organize_sort_folder.py.py
# @Software: PyCharm
"""
1. 投影算法
"""
__author__ = 'big_centaur'
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from cfs import convert_binarization


def draw(point_list):
    """
    画出图像
    """
    plt.figure(figsize=(12, 6))
    plt.plot(point_list, label='projection_x')
    my_x_ticks = np.arange(0, len(point_list), 5)
    plt.xticks(my_x_ticks)
    fontsize = 5
    a_x = plt.gca()
    for tick in a_x.xaxis.get_major_ticks():
        tick.label1.set_fontsize(fontsize)
    plt.show()


def get_vertical_project_list(image):
    """
    对 image 进行垂直投影,得到统计值
    :param image: 需要处理的图片
    :return: 统计值的list
    """
    pixdata = image.load()
    image_w, image_h = image.size
    result = []
    for iter_x in range(image_w):
        black = 0
        for iter_y in range(image_h):
            if pixdata[iter_x, iter_y] == 0:
                black += 1
        result.append(black)
    return result


def adjust_project_data(vertical_pro_list):
    """
    调整收集到的投影信息
    [num1,num2,num3] 变为[[index1,frequent1,num1],[index2,frequent2,num2]]的形式
    :param vertical_pro_list: 垂直投影的到的数组
    :return: 调整之后数组
    """
    count = 1
    num = vertical_pro_list[0]
    result = []

    for i in range(1, len(vertical_pro_list)):
        if vertical_pro_list[i] != vertical_pro_list[i - 1]:
            result.append([i - 1, count, num])
            num = vertical_pro_list[i]
            count = 1
        else:
            count += 1

    result.append([len(vertical_pro_list) - 1, count, num])
    return result
    # return [[2, 3, 0], [3, 1, 1], [6, 3, 2], [9, 3, 3], [14, 5, 0], [18, 4, 3],
    #         [22, 4, 2], [26, 4, 0]]


def find_zero_point(adjusted_result):
    """
    根据提供的[[index1,frequent1,num1],[index2,frequent2,num2]]投影信息,找出有0的地方
    :param adjusted_result: 需要处理的数组
    :return: 分割信息的数组
    """
    # print("adjusted_result len = %d "%len(adjusted_result))
    # 微调开始和终止位置
    adjusted_result[0][1] = 1
    if adjusted_result[-1][2] == 0:
        tmp = adjusted_result[-1][1]
        adjusted_result[-1][0] = adjusted_result[-1][0] - tmp + 1
        adjusted_result[-1][1] = 1
    # print(adjusted_result)
    # 找num = 0
    (index, frequent, num) = adjusted_result[0]
    boundary = [[0, index, frequent, num]]
    for i, (index, frequent, num) in enumerate(adjusted_result):
        if num == 0 and i != 0 and i != len(adjusted_result) - 1:
            boundary.append([i, index, frequent, num])
    (index, frequent, num) = adjusted_result[-1]
    boundary.append([len(adjusted_result) - 1, index, frequent, num])
    # print(boundary)

    edge = []
    edge_info = []
    for i in range(1, len(boundary)):
        start = boundary[i - 1][1]
        end = boundary[i][1] - boundary[i][2] + 1
        edge.append([start, end])
        tmp = adjusted_result[boundary[i - 1][0]:boundary[i][0]]
        if i == (len(boundary) - 1):
            tmp = adjusted_result[boundary[i - 1][0]:boundary[i][0] + 1]
        edge_info.append(tmp)
    # print(edge)
    # print(edge_info)
    return edge, edge_info


def get_project_segment_info(image):
    """
    把image 进行投影找出分割信息
    :param image: 需要处理的图片
    :return: 分割信息的数组
    """
    # 1.获得垂直投影值
    vertical_project_list = get_vertical_project_list(image)
    draw(vertical_project_list)
    print("image width is %d " % len(vertical_project_list))
    # 2.对收集到的统计值进行预处理 由[num1,num2,num3] 变为[[index1,frequent1,num1],[index2,frequent2,num2]]的形式
    adjusted_result = adjust_project_data(vertical_project_list)
    # 3.找0的位置进行分割.
    edge, segment_info = find_zero_point(adjusted_result)
    return edge, segment_info


def segment(image, x_1, y_1, x_2, y_2):
    """
    图片拷贝函数
    """
    box = (x_1, y_1, x_2, y_2)
    region = image.crop(box)
    return region


def save_segment_info(image, edge, sava_folder):
    """
    根据分割信息,image进行保存
    :param image: 需要处理的图片
    :param edge: 分割信息
    :return: 无
    """
    [_, height] = image.size
    for i, [start, end] in enumerate(edge):
        tmp = (segment(image, start, 0, end, height))
        tmp.save(sava_folder + '-' + str(i) + ".png")


def remove_extra_info(edge, segment_info, threshold):
    """
    对宽度小于threshold个像素的点进行去除
    """
    edge_back = edge.copy()
    print(edge)
    new_edge = []
    new_segment_info = []
    for i, (start, end) in enumerate(edge_back):
        if end - start <= threshold:
            # del edge[i]
            # del segment_info[i]
            pass
        else:
            new_edge.append(edge[i])
            new_segment_info.append(segment_info[i])
    return new_edge, new_segment_info


def projection(file_path, sava_folder):
    """
    投影分割算法
    :param file_path: image存储路劲
    :param sava_folder: 存储位置
    :return: 分割之后的数组 [[开始纵坐标,持续的长度],[开始纵坐标,持续的长度],[开始纵坐标,持续的长度]]
    """
    image = Image.open(file_path)
    # 1. 转为灰度图像
    image = image.convert('L')
    # 2. 二值化图像
    threshold = 220
    image = convert_binarization(image, threshold)
    # 3. 获取分割信息
    edge, segment_info = get_project_segment_info(image)
    # 3-1. 长度小于阈值的块进行去除
    edge, segment_info = remove_extra_info(edge, segment_info, 15)
    print(edge)
    # 4. 保存分割信息(先处理投影有0的部分)
    save_segment_info(image, edge, sava_folder)


def main():
    """
    :return: 入口
    """
    file_path = '/media/tianchaoxiong/BIG_CENTAUR/图1/3_5-2.png'
    sava_folder = '/home/tianchaoxiong/LinuxData/paper/experiment/segment/4_live/cnn_pro/dataset/test_38/se_op/ceshj/'
    projection(file_path, sava_folder)


if __name__ == '__main__':
    main()

