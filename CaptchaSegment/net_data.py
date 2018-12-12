# -*- coding: utf-8 -*-
# @Time    : 18-12-10 下午8:10
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : segment_image.py
# @Software: PyCharm

from out_utils import *
from segment_cfs import cfs
from segment_projection import projection
from segment_drop import drop
from segment_synthesis import cfs_drop
from segment_synthesis import cfs_projection


def save_images(images, folder, file_name):
    target_name_srefix = os.path.join(folder, file_name)
    for i, each in enumerate(images):
        each.save(target_name_srefix + '-' + str(i) + ".jpg")


# 合并两个相连的和最小的元素
def combine_min_images(images):
    # 两张image和并成一张
    sums = []
    for i in range(len(images) - 1):
        sums.append(images[i].size[0] + images[i + 1].size[0])
    min_index = list.index(sums, min(sums))
    # images[min_index + 1] = images[min_index + 1] + images[min_index]
    # 把两个和最小的image进行合并.
    images[min_index + 1] = image_merge_horizontal(images[min_index], images[min_index + 1])
    del images[min_index]
    return images


# 把长度大于captcha_len的images中相邻最小的image合并,知道len(images)==captcha_len
def combine_images(images, captcha_len):
    while len(images) != captcha_len:
        images = combine_min_images(images)
    return images


# 把长度最大的那出来重新分割.
def re_segment_max(image):
    pre_conditions = [image.size[0]]
    images = cfs_projection(image, pre_conditions)
    return images


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
            print(get_pix(images[i]), get_pix(images[max_index]))
            if get_pix(images[i]) > get_pix(images[max_index]):
                max_index = i
    return max_index


def re_segment(images):
    max_index = get_len_max_image(images)
    print(max_index)
    new_images = []
    for i, each in enumerate(images):
        if i != max_index:
            new_images.append(each)
        else:
            sub_images = re_segment_max(images[max_index])
            new_images = new_images + sub_images
    return new_images


def correct(images, label):
    captcha_len = len(label)
    if len(images) < captcha_len:
        # 找出最大的 强制使用 分割算法 按照两份 进行分割.
        return re_segment(images), list(label)
    elif len(images) == captcha_len:
        return images, list(label)
    else:  # 对 images中相邻的两个最小的image进行拼接.
        # 此处应该是循环拼接,知道image的数量和captcha的数量相等为止.
        return combine_images(images, captcha_len), list(label)


def main():
    source_folder = '/home/tianchaoxiong/LinuxData/data/MasterExpData/after/qq/less/images'
    target_folder = '/'.join(source_folder.split('/')[:-1])
    images_folder = os.path.join(target_folder, 'train_set')
    labels_save_path = os.path.join(target_folder, 'train_labels.txt')
    make_folder(images_folder)
    # print(images_folder, labels_folder)

    labels_path = '/home/tianchaoxiong/LinuxData/data/MasterExpData/after/qq/less/qq_test_labels.txt'
    labels = open(labels_path, 'r', encoding="utf-8").read().strip().split("#")

    new_images = []
    new_labels = []

    for each in get_internal_path(source_folder):
        # 连通域分割
        # images = cfs(Image.open(each))
        # 投影分割
        # images = projection(Image.open(each), pre_conditions=[67, 106, 134])
        # 滴水分割
        # images = drop(Image.open(each), pre_conditions=[67, 106, 134])
        # 连通域+投影
        images = cfs_projection(Image.open(each), pre_conditions=[67, 106, 134])
        # 连通域+滴水
        # images = cfs_drop(Image.open(each), pre_conditions=[67, 106, 134])

        # TODO:按照验证码中字符的个数对分割字符做一个修正.
        # 1. 若分割出来的 image数量小于验证码中字符数量，直接舍去。
        # 2. 若分割出来的 image数量大于验证码中字符数量，找到最小的两个部分进行合并。
        images, label = correct(images, labels[int(get_file_name(each))])
        print(len(images))
        new_images = new_images + images
        new_labels = new_labels + label
        # save_images(images, target_folder, get_file_name(each))
        print(each, "is Complete")

    # 保存图片和labels
    save_string_2_file(labels_save_path, '#'.join(new_labels))
    for i, each in enumerate(new_images):
        print(i, "is save")
        image_resize_scale(each, 28, 2).save(os.path.join(images_folder, str(i) + '.png'))


if __name__ == '__main__':
    main()
