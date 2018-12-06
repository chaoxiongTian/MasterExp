# -*- coding: utf-8 -*-
"""
1. 投影算法
2. 按照0点分割不开的使用三分之一领域最小值的方案进行分割.
"""
__author__ = 'big_centaur'

from PIL import Image
from cfs import convert_binarization
from projection import get_project_segment_info
from projection import remove_extra_info
from projection import save_segment_info


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
    if len(tmp_list) == 0:  #没有找到波谷 直接返回中间位置
        return middle
    if len(tmp_list) == 1:  #没有找到波谷 直接返回中间位置
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

def fix_segment_use_2(edge, segment_info):
    """
    按照阈值重新分割
    """
    new_edge = []
    for i, (start, end) in enumerate(edge):
        width = end - start
        # 通过阈值 计算应该分为几份.
        if width < 58:
            print("按照一份分割")
            tmp_edge = [edge[i]]
            print(tmp_edge)
        else:
            print("按照二份分割")
            code_num = 2
            tmp_edge = get_segment_edge(edge[i], segment_info[i], code_num)
            print(tmp_edge)
        new_edge = new_edge + tmp_edge
    # print(new_edge)
    return new_edge
def fix_segment_use_3(edge, segment_info):
    """
    按照阈值重新分割
    """
    new_edge = []
    for i, (start, end) in enumerate(edge):
        width = end - start
        # 通过阈值 计算应该分为几份.
        if width < 53:
            print("按照一份分割")
            tmp_edge = [edge[i]]
            print(tmp_edge)
        elif width < 103:
            print("按照二份分割")
            code_num = 2
            tmp_edge = get_segment_edge(edge[i], segment_info[i], code_num)
            print(tmp_edge)
        else:
            print("按照三份分割")
            code_num = 3
            tmp_edge = get_segment_edge(edge[i], segment_info[i], code_num)
            print(tmp_edge)
        new_edge = new_edge + tmp_edge
    # print(new_edge)
    return new_edge
def fix_segment_use_4(edge, segment_info):
    """
    按照阈值重新分割
    """
    new_edge = []
    for i, (start, end) in enumerate(edge):
        width = end - start
        # 通过阈值 计算应该分为几份.
        if width < 62:
            print("按照一份分割")
            tmp_edge = [edge[i]]
            print(tmp_edge)
        elif width < 97:
            print("按照二份分割")
            code_num = 2
            tmp_edge = get_segment_edge(edge[i], segment_info[i], code_num)
            print(tmp_edge)
        elif width < 139:
            print("按照三份分割")
            code_num = 3
            tmp_edge = get_segment_edge(edge[i], segment_info[i], code_num)
            print(tmp_edge)
        else:
            print("按照四份分割")
            code_num = 4
            tmp_edge = get_segment_edge(edge[i], segment_info[i], code_num)
            print(tmp_edge)
        new_edge = new_edge + tmp_edge
    # print(new_edge)
    return new_edge
def fix_segment_use_5(edge, segment_info):
    """
    按照阈值重新分割
    """
    new_edge = []
    for i, (start, end) in enumerate(edge):
        width = end - start
        # 通过阈值 计算应该分为几份.
        if width < 66:
            print("按照一份分割")
            tmp_edge = [edge[i]]
            print(tmp_edge)
        elif width < 111:
            print("按照二份分割")
            code_num = 2
            tmp_edge = get_segment_edge(edge[i], segment_info[i], code_num)
            print(tmp_edge)
        elif width < 154:
            print("按照三份分割")
            code_num = 3
            tmp_edge = get_segment_edge(edge[i], segment_info[i], code_num)
            print(tmp_edge)
        elif width < 215:
            print("按照四份分割")
            code_num = 4
            tmp_edge = get_segment_edge(edge[i], segment_info[i], code_num)
            print(tmp_edge)
        else:
            print("按照五份分割")
            code_num = 5
            tmp_edge = get_segment_edge(edge[i], segment_info[i], code_num)
            print(tmp_edge)
        new_edge = new_edge + tmp_edge
    # print(new_edge)
    return new_edge

def get_segment_edge(each_edge, segment_info, code_num):
    """
    按照指定长度 传多来的投影值进行分割.
    """
    # print('原始的边' + str(each_edge))
    # print('原始的点' + str(segment_info))
    # draw_list = [segment_info[i][2] for i in range(len(segment_info))]
    # draw(draw_list)
    # 根据边的信息找波谷
    trough_list = find_min_point(segment_info)
    # print('找出来的波谷' + str(trough_list))
    # 从波谷列表中找到指定区域中最小的布谷
    start, end = each_edge
    width = end - start
    unit_length = width / code_num
    edge = []
    index_list = [trough_list[0][0]]
    for i in range(code_num - 1):
        tmp_point = find_area_min_trough(
            trough_list, (i + 1) * unit_length + start - unit_length / 3,
            (i + 1) * unit_length + start,
            (i + 1) * unit_length + start + unit_length / 3)
        index_list.append(tmp_point)
    index_list = index_list + [trough_list[-1][0]]
    # print(index_list)
    for i in range(1, len(index_list)):
        edge.append([index_list[i - 1], index_list[i]])
    # print(edge)
    return edge
def fix_segment_wiki(edge, segment_info):
    """
    按照阈值重新分割
    """
    new_edge = []
    for i, (start, end) in enumerate(edge):
        width = end - start
        # 通过阈值 计算应该分为几份.
        if width < 36:
            print("按照一份分割")
            tmp_edge = [edge[i]]
            print(tmp_edge)
        elif width < 61:
            print("按照两份分割")
            code_num = 2
            tmp_edge = get_segment_edge(edge[i], segment_info[i], code_num)
            print(tmp_edge)
        elif width < 87:
            print("按照三份分割")
            code_num = 3
            tmp_edge = get_segment_edge(edge[i], segment_info[i], code_num)
            print(tmp_edge)
        elif width < 112:
            print("按照四份分割")
            code_num = 4
            tmp_edge = get_segment_edge(edge[i], segment_info[i], code_num)
            print(tmp_edge)
        elif width < 141:
            print("按照五份分割")
            code_num = 5
            tmp_edge = get_segment_edge(edge[i], segment_info[i], code_num)
            print(tmp_edge)
        elif width < 165:
            print("按照六份分割")
            code_num = 6
            tmp_edge = get_segment_edge(edge[i], segment_info[i], code_num)
            print(tmp_edge)
        elif width < 187:
            print("按照七份分割")
            code_num = 7
            tmp_edge = get_segment_edge(edge[i], segment_info[i], code_num)
            print(tmp_edge)
        elif width < 211:
            print("按照八份分割")
            code_num = 8
            tmp_edge = get_segment_edge(edge[i], segment_info[i], code_num)
            print(tmp_edge)
        else:
            print("按照九份分割")
            code_num = 9
            tmp_edge = get_segment_edge(edge[i], segment_info[i], code_num)
            print(tmp_edge)
        new_edge = new_edge + tmp_edge
    print(new_edge)
    return new_edge
def fix_segment_sina(edge, segment_info):
    """
    按照阈值重新分割
    """
    new_edge = []
    for i, (start, end) in enumerate(edge):
        width = end - start
        # 通过阈值 计算应该分为几份.
        if width < 26:
            print("按照一份分割")
            tmp_edge = [edge[i]]
            print(tmp_edge)
        elif width < 40:
            print("按照两份分割")
            code_num = 2
            tmp_edge = get_segment_edge(edge[i], segment_info[i], code_num)
            print(tmp_edge)
        elif width < 56:
            print("按照三份分割")
            code_num = 3
            tmp_edge = get_segment_edge(edge[i], segment_info[i], code_num)
            print(tmp_edge)
        elif width < 68:
            print("按照四份分割")
            code_num = 4
            tmp_edge = get_segment_edge(edge[i], segment_info[i], code_num)
            print(tmp_edge)
        else:
            print("按照五份分割")
            code_num = 5
            tmp_edge = get_segment_edge(edge[i], segment_info[i], code_num)
            print(tmp_edge)
        new_edge = new_edge + tmp_edge
    print(new_edge)
    return new_edge
def fix_segment_sina_tmp(edge, segment_info):
    """
    按照阈值重新分割
    """
    new_edge = []
    for i, (start, end) in enumerate(edge):
        width = end - start
        # 通过阈值 计算应该分为几份.
        if width < 62:
            print("按照一份分割")
            tmp_edge = [edge[i]]
            print(tmp_edge)
        if width < 115:
            print("按照二份分割")
            code_num = 2
            tmp_edge = get_segment_edge(edge[i], segment_info[i], code_num)
            print(tmp_edge)
        else:
            print("按照三份分割")
            code_num = 3
            tmp_edge = get_segment_edge(edge[i], segment_info[i], code_num)
            print(tmp_edge)
        new_edge = new_edge + tmp_edge
    print(new_edge)
    return new_edge
def fix_segment_ebay(edge, segment_info):
    """
    按照阈值重新分割
    """
    new_edge = []
    for i, (start, end) in enumerate(edge):
        width = end - start
        # 通过阈值 计算应该分为几份.
        if width < 29:
            print("按照一份分割")
            tmp_edge = [edge[i]]
            print(tmp_edge)
        elif width < 50:
            print("按照两份分割")
            code_num = 2
            tmp_edge = get_segment_edge(edge[i], segment_info[i], code_num)
            print(tmp_edge)
        elif width < 72:
            print("按照三份分割")
            code_num = 3
            tmp_edge = get_segment_edge(edge[i], segment_info[i], code_num)
            print(tmp_edge)
        elif width < 87:
            print("按照四份分割")
            code_num = 4
            tmp_edge = get_segment_edge(edge[i], segment_info[i], code_num)
            print(tmp_edge)
        elif width < 103:
            print("按照五份分割")
            code_num = 5
            tmp_edge = get_segment_edge(edge[i], segment_info[i], code_num)
            print(tmp_edge)
        else:
            print("按照六份分割")
            code_num = 6
            tmp_edge = get_segment_edge(edge[i], segment_info[i], code_num)
            print(tmp_edge)
        new_edge = new_edge + tmp_edge
    # print(new_edge)
    return new_edge
def fix_segment_jd(edge, segment_info):
    """
    按照阈值重新分割
    """
    new_edge = []
    for i, (start, end) in enumerate(edge):
        width = end - start
        # 通过阈值 计算应该分为几份.
        if width < 56:
            print("按照一份分割")
            tmp_edge = [edge[i]]
            print(tmp_edge)
        elif width < 90:
            print("按照两份分割")
            code_num = 2
            tmp_edge = get_segment_edge(edge[i], segment_info[i], code_num)
            print(tmp_edge)
        elif width < 136:
            print("按照三份分割")
            code_num = 3
            tmp_edge = get_segment_edge(edge[i], segment_info[i], code_num)
            print(tmp_edge)
        else:
            print("按照四份分割")
            code_num = 4
            tmp_edge = get_segment_edge(edge[i], segment_info[i], code_num)
            print(tmp_edge)
        new_edge = new_edge + tmp_edge
    # print(new_edge)
    return new_edge
def fix_segment_jd_2(edge, segment_info):
    """
    按照阈值重新分割
    """
    new_edge = []
    for i, (start, end) in enumerate(edge):
        width = end - start
        # 通过阈值 计算应该分为几份.
        if width < 54:
            print("按照一份分割")
            tmp_edge = [edge[i]]
            print(tmp_edge)
        else:
            print("按照二份分割")
            code_num = 2
            tmp_edge = get_segment_edge(edge[i], segment_info[i], code_num)
            print(tmp_edge)
        new_edge = new_edge + tmp_edge
    # print(new_edge)
    return new_edge
def fix_segment_alipay(edge, segment_info):
    """
    按照阈值重新分割
    """
    new_edge = []
    for i, (start, end) in enumerate(edge):
        width = end - start
        # 通过阈值 计算应该分为几份.
        if width < 26:
            print("按照一份分割")
            tmp_edge = [edge[i]]
            print(tmp_edge)
        elif width < 36:
            print("按照两份分割")
            code_num = 2
            tmp_edge = get_segment_edge(edge[i], segment_info[i], code_num)
            print(tmp_edge)
        elif width < 59:
            print("按照三份分割")
            code_num = 3
            tmp_edge = get_segment_edge(edge[i], segment_info[i], code_num)
            print(tmp_edge)
        else:
            print("按照四份分割")
            code_num = 4
            tmp_edge = get_segment_edge(edge[i], segment_info[i], code_num)
            print(tmp_edge)
        new_edge = new_edge + tmp_edge
    # print(new_edge)
    return new_edge
def fix_segment_weibo(edge, segment_info):
    """
    按照阈值重新分割
    """
    new_edge = []
    for i, (start, end) in enumerate(edge):
        width = end - start
        # 通过阈值 计算应该分为几份.
        if width < 38:
            print("按照一份分割")
            tmp_edge = [edge[i]]
            print(tmp_edge)
        elif width < 54:
            print("按照两份分割")
            code_num = 2
            tmp_edge = get_segment_edge(edge[i], segment_info[i], code_num)
            print(tmp_edge)
        elif width < 74:
            print("按照三份分割")
            code_num = 3
            tmp_edge = get_segment_edge(edge[i], segment_info[i], code_num)
            print(tmp_edge)
        else:
            print("按照四份分割")
            code_num = 4
            tmp_edge = get_segment_edge(edge[i], segment_info[i], code_num)
            print(tmp_edge)
        new_edge = new_edge + tmp_edge
    # print(new_edge)
    return new_edge



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
    edge, segment_info = remove_extra_info(edge, segment_info, 3)
    # 4. 对使用投影值为0 不能分割的情况使用 区域内最小值的方案.
    # 解释:假设一个字符的长度为0-20 两个字符是20-40,那么当一个分割块的长度为35的时候则认为两个字符粘连,则对区域进行等分,然后等分长度的三分之一领域内找到的极值 作为分割点.
    edge = fix_segment_use_2(edge, segment_info)
    # 5. 保存分割信息(先处理投影有0的部分)
    # print(edge)
    save_segment_info(image, edge, sava_folder)


def main():
    """
    :return: null
    """
    file_path = '/home/tianchaoxiong/LinuxData/paper/experiment/segment/4_live/cnn_pro/dataset/test_38/images_otsu/0.png'
    sava_folder = '/home/tianchaoxiong/LinuxData/paper/experiment/segment/4_live/cnn_pro/dataset/test_38/se_op/ceshj/'
    projection(file_path, sava_folder)


if __name__ == '__main__':
    main()
