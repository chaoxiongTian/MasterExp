# -*- coding: utf-8 -*-
# @Time    : 18-12-10 下午8:10
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : segment_cfs.py
# @Software: PyCharm


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


# 得到起始位置，和跨度大小
def get_boundary(block, axis):
    s2b = sorted(block, key=lambda x: x[axis])
    return s2b[-1][axis] - s2b[0][axis], s2b[0][axis]


# 返回block的信息，（宽，x轴开始的位置，高，轴开始的位置）
def get_block_info(block):
    block_w, w_begin = get_boundary(block, 0)
    block_h, h_begin = get_boundary(block, 1)
    return block_w, w_begin, block_h, h_begin


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


# block 转为 image
def blocks_2_images(blocks, padding=1):
    images = []
    for i, each_block in enumerate(blocks):
        # 获取每个区块的长宽 和长宽的其实起始位置
        block_w, w_begin, block_h, h_begin = get_block_info(each_block)
        im_bg = Image.new('RGB', (block_w + padding, block_h + padding), (255, 255, 255))
        im = convert_binary(im_bg, 220)
        pix_data = im.load()
        for x, y in each_block:
            pix_data[x - w_begin, y - h_begin] = 0
        images.append(im)
    return images


# 对有重叠的block进行修正
def correct_blocks(blocks):
    # 计算重叠度
    def get_overlap_rate(block1, block2):
        # 1, 找出list1,list2 再垂直方向上的起始和终止位置.
        w1, w_begin1, _, _ = get_block_info(block1)
        w2, w_begin2, _, _ = get_block_info(block2)
        # 2. 根据区间找到重合率
        rate = get_rate(w_begin1, w1 + w_begin1, w_begin2, w2 + w_begin2)
        return rate

    def get_rate(start1, end1, start2, end2):
        if start2 > end1 or start1 > end2:
            return 0
        if start1 > start2 and end1 < end2:
            return 1
        if start2 > start1 and end2 < end1:
            return 1
        len_min = ((end1 - start1)
                   if (end1 - start1) < (end2 - start2) else (end2 - start2)) + 1
        return (min(abs(end1 - start2), abs(end2 - start1)) + 1) / len_min

    # 根据重合率进行修正
    def combine_block(threshold=0.3):
        switch = 0
        new_blocks = []
        for j in range(len(blocks)):
            if j == len(blocks) - 1:
                block = blocks[j]
                if switch == 0:
                    new_blocks.append(block)
                break
            if overlaps[j] >= threshold:
                block = blocks[j] + blocks[j + 1]
                new_blocks.append(block)
                switch = 1
            else:
                if switch == 1:
                    switch = 0
                else:
                    block = blocks[j]
                    new_blocks.append(block)

        return new_blocks

    overlaps = []  # 重叠度（前一个和后一个的重叠度）
    for i in range(len(blocks) - 1):
        overlaps.append(get_overlap_rate(blocks[i], blocks[i + 1]))

    blocks = combine_block()
    return blocks


def save_images(images, folder, file_name):
    target_name_srefix = os.path.join(folder, file_name)
    for i, each in enumerate(images):
        each.save(target_name_srefix + '-' + str(i) + ".png")


def cfs(file_path):
    # 1. 二值化
    image = convert_binary(Image.open(file_path), threshold=220)

    # 2. 根据二值化之后的像素点，获取相连的块
    connected_blocks = get_connected_blocks(image)
    print("block num is : %d" % len(connected_blocks))

    # 3. 对类似于 i 上面的哪一点进行修复（计算两个block在竖直方向的重合率）
    connected_blocks = correct_blocks(connected_blocks)
    connected_blocks = correct_blocks(connected_blocks)

    # 4. 把联通快转为images
    images = blocks_2_images(connected_blocks)
    return images

    # 5. 保存
    # save_images(images, get_file_folder(file_path), get_file_name(file_path))
