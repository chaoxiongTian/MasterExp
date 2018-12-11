# -*- coding: utf-8 -*-
# @Time    : 18-12-6 下午9:52
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : segment_projection
# @Software: PyCharm

from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from segment_utils import *


# 画出像素直方图 point_list 为纵坐标统计的像素值
def draw(point_list):
    print(point_list)
    plt.figure(figsize=(12, 6))
    plt.plot(point_list, label='projection_x')
    my_x_ticks = np.arange(0, len(point_list), 5)
    plt.xticks(my_x_ticks)
    a_x = plt.gca()
    for tick in a_x.xaxis.get_major_ticks():
        tick.label1.set_fontsize(fontsize=5)
    plt.show()


# 统计纵坐标像素值
def get_vertical_counts(image):
    pix_data = image.load()
    image_w, image_h = image.size
    result = []
    for iter_x in range(image_w):
        black = 0
        for iter_y in range(image_h):
            if pix_data[iter_x, iter_y] == 0:
                black += 1
        result.append(black)
    return result


# 对投影统计值进行预处理 由[num1,num2,num3]变为[[index1,frequent1,num1],[index2,frequent2,num2]]
def preprocessed(vertical_counts):
    count = 1
    num = vertical_counts[0]
    result = []

    for i in range(1, len(vertical_counts)):
        if vertical_counts[i] != vertical_counts[i - 1]:
            result.append([i - 1, count, num])
            num = vertical_counts[i]
            count = 1
        else:
            count += 1

    result.append([len(vertical_counts) - 1, count, num])
    return result


# 找到波谷是0的位置，按照这个位置进行划分。
def find_zero_point(segments):
    # 微调开始和终止位置
    segments[0][1] = 1
    if segments[-1][2] == 0:
        tmp = segments[-1][1]
        segments[-1][0] = segments[-1][0] - tmp + 1
        segments[-1][1] = 1

    # 找num = 0
    (index, frequent, num) = segments[0]
    boundary = [[0, index, frequent, num]]
    for i, (index, frequent, num) in enumerate(segments):
        if num == 0 and i != 0 and i != len(segments) - 1:
            boundary.append([i, index, frequent, num])
    (index, frequent, num) = segments[-1]
    boundary.append([len(segments) - 1, index, frequent, num])
    # print(boundary)

    edge = []
    edge_info = []
    for i in range(1, len(boundary)):
        start = boundary[i - 1][1]
        end = boundary[i][1] - boundary[i][2] + 1
        edge.append([start, end])
        tmp = segments[boundary[i - 1][0]:boundary[i][0]]
        if i == (len(boundary) - 1):
            tmp = segments[boundary[i - 1][0]:boundary[i][0] + 1]
        edge_info.append(tmp)
    return edge, edge_info


# 获得分割区间
def get_project_segment_info(image):
    # 1.获得垂直投影值
    vertical_counts = get_vertical_counts(image)
    # draw(vertical_project)  # 画出折线图
    print("image width is %d " % len(vertical_counts))

    # 2.对竖直方向的像素统计值进行预处理
    segments = preprocessed(vertical_counts)

    # 3.找0的位置进行分割.
    edge, wave_info = find_zero_point(segments)

    return edge, wave_info


def segment(image, x_1, y_1, x_2, y_2):
    """
    图片拷贝函数
    """
    box = (x_1, y_1, x_2, y_2)
    region = image.crop(box)
    return region


def get_images(image, edge):
    images = []
    [_, height] = image.size
    for i, [start, end] in enumerate(edge):
        images.append(segment(image, start, 0, end, height))
    return images


# 长度过于窄的直接进行清理。
def correct_segments(edge, wave_info, threshold=15):
    edge_back = edge.copy()
    new_edge = []
    new_segment_info = []
    for i, (start, end) in enumerate(edge_back):
        if end - start <= threshold:
            pass
        else:
            new_edge.append(edge[i])
            new_segment_info.append(wave_info[i])
    return new_edge, new_segment_info


def find_min_point(segment_info):
    """
    根据规整的数值找到波谷 第一个和最有一个默认  其他的大于前一个小于后一个就算波谷
    """
    trough_list = [segment_info[0]]
    for i in range(1, len(segment_info) - 1):
        if segment_info[i -
                        1][2] > segment_info[i][2] and segment_info[i +
                                                                    1][2] > segment_info[i][2]:
            trough_list.append(segment_info[i])
    trough_list.append(segment_info[-1])
    return trough_list


def find_area_min_trough(trough_list, start, middle, end):
    """
    找出 start到end 中波谷的最小值,若找不到直接返回middle
    """
    start, middle, end = int(start), int(middle), int(end)
    tmp_list = []
    for index, _, num in trough_list:
        if start < index < end:
            tmp_list.append([index, num])
    # print(tmp_list)
    if len(tmp_list) == 0:  # 没有找到波谷 直接返回中间位置
        return middle
    if len(tmp_list) == 1:  # 没有找到波谷 直接返回中间位置
        return tmp_list[0][0]
    # 从收集到的tmp_list中找出最小的 波谷的位置,若有相等的返回离middle比较近的位置.
    index_t, num_t = tmp_list[0]
    for i in range(1, len(tmp_list)):
        index, num = tmp_list[i]
        if num_t < num:
            pass
        elif num_t > num:
            index_t, num_t = index, num
        else:
            if abs(index_t - middle) > abs(index - middle):
                index_t, num_t = index, num
            else:
                pass
    return index_t


# 对部分区域按照 期望分割的数量 进行分割
def get_sub_edge(each_edge, wave_info, tar_num):
    if tar_num == 1:
        return [each_edge]

    # 根据边的信息找波谷 troughs集合
    troughs = find_min_point(wave_info)

    # 从波谷列表中找到指定区域中最小的布谷
    start, end = each_edge
    width = end - start  # 区域长度
    unit_length = width / tar_num  # 单元长度
    edge = []
    index_list = [troughs[0][0]]  # 第一个加入
    for i in range(tar_num - 1):
        tmp_point = find_area_min_trough(
            troughs, (i + 1) * unit_length + start - unit_length / 3,
                     (i + 1) * unit_length + start,
                     (i + 1) * unit_length + start + unit_length / 3)
        index_list.append(tmp_point)
    index_list = index_list + [troughs[-1][0]]  # 最后一个加入

    for i in range(1, len(index_list)):
        edge.append([index_list[i - 1], index_list[i]])

    return edge


# 根据先验条件 对部分 区域再进行分割。
def re_segment(edge, wave_info, pre_conditions):
    def get_tar_num(key):
        for j, each in enumerate(pre_conditions):
            if key < each:
                return j + 1
        return len(pre_conditions) + 1

    new_edge = []
    for i, (start, end) in enumerate(edge):
        width = end - start
        # 根据先验条件得到预分割的份数。
        tar_num = get_tar_num(width)

        new_edge = new_edge + get_sub_edge(edge[i], wave_info[i], tar_num)
    return new_edge


def projection(file_path):
    image = convert_binary(Image.open(file_path))
    edge, wave_info = get_project_segment_info(image)
    # 长度小于阈值的块进行去除
    edge, wave_info = correct_segments(edge, wave_info)

    # TODO： 此处 根据先验条件 对过于大的区间再进行分割。
    # 比如
    # 长度在30之内认为必然只存在一个字符
    # 长度在30-60之间必然存在两个字符
    # 长度在60-90之间必然存在三个字符
    # 长度大于90 则认为四个字符
    #
    # 多个字符的处理方式是：在等分点的左右指定范围内找最小的波谷。

    pre_conditions = [30, 60, 90]  # 0-30(切一份)，30-60(切两份),60-90(切三分),>90(切四份)
    edge = re_segment(edge, wave_info, pre_conditions)

    images = get_images(image, edge)
    return images
