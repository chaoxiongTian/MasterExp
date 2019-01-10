# -*- coding: utf-8 -*-
# @Time    : 18-12-10 下午8:10
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : segment_image.py
# @Software: PyCharm

import os
from out_utils import *
from segment_cfs import cfs
from segment_projection import projection
from segment_drop import drop
from segment_synthesis import cfs_drop
from segment_synthesis import cfs_projection
from seg_options import Options


# 字符分割的预设距离
def get_cond(cond):
    condition = list()
    if str(cond).strip() == '':
        return None
    for each in str(cond).strip().split(','):
        try:
            condition.append(int(each))
        except RuntimeError as e:
            print(e, 'conditions input error')
    return condition


# 合并两个相连的和最小的元素
def combine_min_images(images):
    if len(images) == 1:
        return images
    # 两张image和并成一张
    sums = list()
    for i in range(len(images) - 1):
        sums.append(images[i].size[0] + images[i + 1].size[0])
    min_index = list.index(sums, min(sums))
    # images[min_index + 1] = images[min_index + 1] + images[min_index]
    # 把两个和最小的image进行合并.
    images[min_index + 1] = image_merge_horizontal(images[min_index], images[min_index + 1])
    del images[min_index]
    return images


# 把长度大于captcha_len的images中相邻最小的image合并,知道len(images)==captcha_len
def combine_images(images):
    while len(images) != captcha_len:
        images = combine_min_images(images)
    return images


# 把长度最大的按照两份重新分割.
def re_segment_max(image):
    return cfs_projection(image, [image.size[0]])


# 返回黑色像素的个数
def get_pix(image):
    pix_data = image.load()
    image_w, image_h = image.size
    count = 0
    for iter_x in range(image_w):
        for iter_y in range(image_h):
            if pix_data[iter_x, iter_y] == 0:
                count += 1
    return count


def get_len_max_image(images):
    max_w = images[0].size[0]
    max_index = 0
    for i in range(1, len(images)):
        if images[i].size[0] > max_w:
            max_w = images[i].size[0]
            max_index = i
        elif images[i].size[0] == max_w:
            # print(get_pix(images[i]), get_pix(images[max_index]))
            if get_pix(images[i]) > get_pix(images[max_index]):
                max_index = i
    return max_index


def re_segment(images):
    max_index = get_len_max_image(images)
    new_images = list()
    for i, each in enumerate(images):
        if i != max_index:
            new_images.append(each)
        else:
            sub_images = re_segment_max(images[max_index])
            new_images = new_images + sub_images
    return new_images


def correct(images, label):
    if len(images) < captcha_len - 1:
        return None, ''
    elif len(images) == captcha_len - 1:
        # 找出最大的 强制使用 分割算法 按照两份 进行分割.
        return re_segment(images), list(label)
    elif len(images) == captcha_len:
        return images, list(label)
    else:  # 对 images中相邻的两个最小的image进行拼接.
        # 此处应该是循环拼接,知道image的数量和captcha的数量相等为止.
        return combine_images(images), list(label)


# 超参数
opt = Options().parse()
folder = os.path.join(data_folder, opt.captcha, opt.use)
if opt.use == 'cnn':
    sour_folder = os.path.join(folder, 'images')
    tar_folder = os.path.join(folder, 'train')
    labels_path = os.path.join(folder, opt.captcha+'_train_5000_labels.txt')
    tar_labels_path = os.path.join(folder, 'train_labels.txt')

elif opt.use == 'seg':
    sour_folder = os.path.join(folder, opt.tar, 'images')
    tar_folder = os.path.join(folder, opt.tar, 'test')
    labels_path = os.path.join(folder, opt.captcha+'_test_200_labels.txt')
    tar_labels_path = os.path.join(folder, opt.tar, 'test_labels.txt')
else:
    raise RuntimeError('use input error ,only cnn or seg')
make_folder(tar_folder)
if not os.path.exists(labels_path):
    raise RuntimeError('{} should have labels file'.format(labels_path))
labels = open(labels_path, 'r', encoding="utf-8").read().strip().split("#")
captcha_len = len(labels[0])
pre_conditions = get_cond(opt.cond)


def segment(image_path, condition):
    label = (labels[int(get_file_name(image_path))])
    if opt.use == 'cnn':
        # 用cfs进行分割，不修正。
        images = cfs(Image.open(image_path))
        if len(images) != captcha_len:
            images = []
            label = ''
    else:
        # 用cfs结合其他分割算法分割，需要修正。
        images = cfs_projection(Image.open(image_path), pre_conditions=condition)
        # TODO:按照验证码中字符的个数对分割字符做一个修正.
        # 1. 若分割出来的 image数量小于验证码中字符数量，直接舍去。
        # 2. 若分割出来的 image数量大于验证码中字符数量，找到最小的两个部分进行合并。
        images, label = correct(images, label)
    return images, label


def main():
    new_images = list()
    new_labels = list()
    for each in get_internal_path(sour_folder):
        # TODO:对于训练集 使用cfs进行分割，若分割长度和验证码长度不用直接舍弃。对于测试集使用多种分割算法分割，然后修正。
        part_images, part_labels = segment(each, pre_conditions)
        if part_images is not None and len(part_images) == captcha_len :
            new_images.extend(part_images)
            new_labels.extend(part_labels)
            print(each, "is Complete")

    # 保存图片和labels
    save_string_2_file(tar_labels_path, '#'.join(new_labels))
    for i, each in enumerate(new_images):
        print("{} is save in {}".format(str(i), tar_folder))
        image_resize_scale(each, 28, 2).save(os.path.join(tar_folder, str(i) + '.png'))


if __name__ == '__main__':
    main()
