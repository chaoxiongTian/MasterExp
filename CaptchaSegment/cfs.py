# -*- coding: utf-8 -*-
"""
1. cfs分割算法
"""
__author__ = 'MaxCentaur'
from out_utils import *
from segment_utils import convert_binary


# 判断某个像素点是否已经被遍历过
def is_collected(connected_blocks, p_x, p_y):
    for each in connected_blocks:
        for iter_x, iter_y in each:
            if iter_x == p_x and iter_y == p_y:
                return True
    return False


# 有一个点获取相联通的所有坐标
def get_block(pix_data, p_x, p_y, value=127):
    block = []
    try:
        background = pix_data[p_x, p_y]
        if background == value:
            return  # 起始点的颜色已经填充
        pix_data[p_x, p_y] = value
    except (ValueError, IndexError):
        return  # seed point outside image
    edge = [(p_x, p_y)]
    block.append([p_x, p_y])
    while edge:
        new_edge = []
        for (iter_x, iter_y) in edge:
            for (tmp_x, tmp_y) in ((iter_x + 1, iter_y), (iter_x - 1, iter_y),
                                   (iter_x, iter_y + 1), (iter_x, iter_y - 1)):
                try:
                    pixel = pix_data[tmp_x, tmp_y]
                except IndexError:
                    pass
                else:
                    if pixel == background:
                        pix_data[tmp_x, tmp_y] = value
                        block.append([tmp_x, tmp_y])
                        new_edge.append((tmp_x, tmp_y))
        edge = new_edge
    return block


# 返回block的信息，（宽，x轴开始的位置，高，轴开始的位置）
def get_block_info(block):
    block_w, w_min_begin_point = get_boundary(block, 0)
    block_h, h_min_begin_point = get_boundary(block, 1)
    return block_w, w_min_begin_point, block_h, h_min_begin_point


# 判断一个连通域是否合法
def block_check(block, min_block_size, min_w=1, min_h=1):
    """
    不合法的条件
    1. 宽小于min_w个像素，
    2. 高小于min_h个像素，
    3. 整理小于min_block_size个像素。
    """
    block_w, _, block_h, _ = get_block_info(block)
    if block_w <= min_w or block_h <= min_h or len(block) <= min_block_size:
        return False
    else:
        return True


# 遍历像素点 获取联通快
def get_connected_blocks(im, min_block_size=10):
    pix_data = im.load()
    (image_w, image_h) = im.size
    connected_blocks = []
    for iter_x in range(image_w):
        for iter_y in range(image_h):
            if pix_data[iter_x, iter_y] == 0:
                # 遍历的时候找到黑色像素,判断是否已经收集在connected_blocks中,
                if is_collected(connected_blocks, iter_x, iter_y):
                    # 若在跳过.
                    pass
                else:
                    # 若不在,按照这个点开始 连通域遍历.
                    block = get_block(pix_data, iter_x, iter_y)  # 此算法可做颜色填充算法
                    # TODO:这里最好做一个block_check()函数 而非一个长度。
                    # if len(block) > min_block_size:
                    #     connected_blocks.append(block)
                    if block_check(block, min_block_size):
                        connected_blocks.append(block)
    return connected_blocks


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


def save_blocks(blocks, save_folder, file_name, padding=1):
    target_name_srefix = os.path.join(save_folder, file_name)
    for i, each_block in enumerate(blocks):
        # 获取每个区块的长宽 和长宽的其实起始位置
        block_w, w_min_begin_point, block_h, h_min_begin_point = get_block_info(each_block)
        im_bg = Image.new('RGB', (block_w + padding, block_h + padding), (255, 255, 255))
        im = convert_binary(im_bg, 220)
        pix_data = im.load()
        for x, y in each_block:
            pix_data[x - w_min_begin_point, y - h_min_begin_point] = 0
        im.save(target_name_srefix + '-' + str(i) + ".png")


#  连通域分割算法
def cfs(file_path):
    # 1. 二值化
    image = convert_binary(Image.open(file_path), threshold=220)

    # 2. 根据二值化之后的像素点，获取相连的块
    connected_blocks = get_connected_blocks(image)
    print("block num is : %d" % len(connected_blocks))

    # 3. 保存 联通块
    save_blocks(connected_blocks, get_file_folder(file_path), get_file_name(file_path))


def main():
    target_folder = os.path.join(data_folder, "cfs")
    make_folder(target_folder)
    image_path = os.path.join(target_folder, "0.png")
    cfs(image_path)


if __name__ == '__main__':
    main()
