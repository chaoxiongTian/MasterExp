# -*- coding: utf-8 -*-
# @Time    : 18-12-11 下午5:14
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : segment_drop.py
# @Software: PyCharm

from itertools import groupby
from segment_utils import *
from segment_projection import get_edge


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
        else:  # j == 5
            return 0 if img_pix[x - 1, y] == 0 else 1
    except IndexError:
        return 0


def get_end_route(img, start_x, height):
    """获取滴水路径"""
    left_limit = 0
    right_limit = img.size[0] - 1
    end_route = []
    cur_p = (start_x, 0)  # 第一个位置
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


def do_split(source_image, starts, filter_ends):
    """
    具体实行切割
    : param starts: 每一行的起始点 tuple of list
    : param ends: 每一行的终止点
    """
    # TODO: 这里的starts 可能是空，导致分割出错。
    left = abs(starts[0][0])
    top = abs(starts[0][1])
    right = abs(filter_ends[0][0])
    bottom = abs(filter_ends[0][1])
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
                image.putpixel((x - left, start[1] - top), (0, 0, 0))
    return image


def drop_segment(im, start_list):
    images = []
    width, height = im.size
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
        end_route = get_end_route(im, start_x, height)
        filter_end_route = [
            max(list(k)) for _, k in groupby(end_route, lambda x: x[1])
        ]  # 注意这里groupby
        try:
            img1 = do_split(im, start_route, filter_end_route)
            images.append(img1)
        except IndexError:
            pass

        next_start_route = list(
            map(lambda x: (x[0] + 1, x[1]), filter_end_route))

    # 最后一个
    start_route = next_start_route
    end_route = []
    for y in range(height):
        end_route.append((width - 1, y))
    img2 = do_split(im, start_route, end_route)
    images.append(img2)
    return images


def drop(image, pre_conditions=(30, 60, 90)):
    w, h = image.size
    if pre_conditions[0] > w:
        return [image]
    new_image, edge = get_edge(image, pre_conditions)
    if len(edge) == 1:
        return [new_image]
    images = drop_segment(new_image, edge)
    return images
