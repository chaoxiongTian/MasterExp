# -*- coding: utf-8 -*-
"""
1. 滴水算法分割算法
2. 更改分割之后出现白色部分
"""
__author__ = 'big_centaur'
import shutil
from itertools import groupby
from PIL import Image
from cfs import convert_binarization
from projection import get_project_segment_info
from projection import remove_extra_info



def get_nearby_pix_value(img_pix, x, y, j):
    """获取临近5个点像素数据"""
    try:
        if j == 1:
            return 0 if img_pix[x - 1, y + 1] == 0 else 1
        elif j == 2:
            return 0 if img_pix[x, y + 1] == 0 else 1
        elif j == 3:
            return 0 if img_pix[x + 1, y + 1] == 0 else 1
        elif j == 4:
            return 0 if img_pix[x + 1, y] == 0 else 1
        else:  #j == 5
            return 0 if img_pix[x - 1, y] == 0 else 1
    except IndexError:
        return 0


def get_end_route(img, start_x, height):
    """获取滴水路径"""
    left_limit = 0
    right_limit = img.size[0] - 1
    end_route = []
    cur_p = (start_x, 0)  #第一个位置
    last_p = cur_p
    end_route.append(cur_p)
    while cur_p[1] < (height - 1):
        sum_n = 0
        max_w = 0
        next_x = cur_p[0]
        next_y = cur_p[1]
        pix_img = img.load()
        for i in range(1, 6):
            cur_w = get_nearby_pix_value(pix_img, cur_p[0], cur_p[1], i) * (
                6 - i)
            sum_n += cur_w
            if max_w < cur_w:
                max_w = cur_w
        if sum_n == 0:
            # 如果全黑则看惯性
            max_w = 4
        if sum_n == 15:
            max_w = 6
        if max_w == 1:
            next_x = cur_p[0] - 1
            next_y = cur_p[1]
        elif max_w == 2:
            next_x = cur_p[0] + 1
            next_y = cur_p[1]
        elif max_w == 3:
            next_x = cur_p[0] + 1
            next_y = cur_p[1] + 1
        elif max_w == 5:
            next_x = cur_p[0] - 1
            next_y = cur_p[1] + 1
        elif max_w == 6:
            next_x = cur_p[0]
            next_y = cur_p[1] + 1
        elif max_w == 4:
            if next_x > cur_p[0]:
                # 向右
                next_x = cur_p[0] + 1
                next_y = cur_p[1] + 1
            if next_x < cur_p[0]:
                next_x = cur_p[0]
                next_y = cur_p[1] + 1
            if sum_n == 0:
                next_x = cur_p[0]
                next_y = cur_p[1] + 1
        else:
            raise Exception("get end route error")
        if last_p[0] == next_x and last_p[1] == next_y:
            if next_x < cur_p[0]:
                max_w = 5
                next_x = cur_p[0] + 1
                next_y = cur_p[1] + 1
            else:
                max_w = 3
                next_x = cur_p[0] - 1
                next_y = cur_p[1] + 1
        last_p = cur_p
        if next_x > right_limit:
            next_x = right_limit
            next_y = cur_p[1] + 1
        if next_x < left_limit:
            next_x = left_limit
            next_y = cur_p[1] + 1
        cur_p = (next_x, next_y)
        end_route.append(cur_p)
    return end_route


def do_split(gary_image, source_image, starts, filter_ends):
    """
    具体实行切割
    : param starts: 每一行的起始点 tuple of list
    : param ends: 每一行的终止点
    """
    left = starts[0][0]
    top = starts[0][1]
    right = filter_ends[0][0]
    bottom = filter_ends[0][1]
    pixdata = source_image.load()
    for i in range(len(starts)):
        left = min(starts[i][0], left)
        top = min(starts[i][1], top)
        right = max(filter_ends[i][0], right)
        bottom = max(filter_ends[i][1], bottom)
    width = right - left + 1
    height = bottom - top + 1
    image = Image.new('RGB', (int(width), int(height)), (255, 255, 255))
    for i in range(height):
        start = starts[i]
        end = filter_ends[i]
        for x in range(start[0], end[0] + 1):
            if pixdata[x, start[1]] == 0:
                # image.putpixel((x - left, start[1] - top), (0, 0, 0))
                image.putpixel((x - left, start[1] - top),
                               gary_image.load()[x, start[1]])
    return image


def drop_fall(image, img, start_list, save_dir):
    """
    采用滴水切割 根据res 对image_threshold进行切割
    :param image_threshold:
    :param res:[point,width][切割点,切割的宽度]
    :return:
    """
    num_code = len(start_list)
    images = []
    width, height = img.size
    # 开始滴水算法
    next_start_route = []
    for i in range(len(start_list) - 1):
        start_x = start_list[i + 1][0]
        if i == 0:
            start_route = []
            for y in range(height):
                start_route.append((0, y))
        else:
            start_route = next_start_route
        end_route = get_end_route(img, start_x, height)
        filter_end_route = [
            max(list(k)) for _, k in groupby(end_route, lambda x: x[1])
        ]  # 注意这里groupby
        try:
            img1 = do_split(image, img, start_route, filter_end_route)
            img1.save(save_dir + "-" + str(i) + ".png")
        except IndexError:
            pass

        next_start_route = list(
            map(lambda x: (x[0] + 1, x[1]), filter_end_route))

    # 最后一个
    start_route = next_start_route
    end_route = []
    for y in range(height):
        end_route.append((width - 1, y))
    img2 = do_split(image, img, start_route, end_route)
    img2.save(save_dir + "-" + str(num_code - 1) + '.png')
    return images

from projection_update1 import fix_segment_use_2
def dropfall(file_path, sava_folder):
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
    # 5. 使用滴水算法进行分割
    print('分割的边' + str(edge))
    if len(edge) == 1:
        # 直接复制
        shutil.copy(file_path, sava_folder+ '.png')
    else:
        drop_fall(image, image, edge, sava_folder)


def main():
    """
    :return: 入口
    """
    file_path = '/home/tianchaoxiong/LinuxData/code/pro_collect/production/data/-0.png'
    sava_folder = '../data/'
    dropfall(file_path, sava_folder)


if __name__ == '__main__':
    main()
