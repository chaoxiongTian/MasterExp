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


def main():
    source_folder = '/home/tianchaoxiong/LinuxData/data/MasterExpData/after/qq/results_85/images'
    target_folder = source_folder + '_cfs_drop'
    make_folder(target_folder)
    image_paths = get_internal_path(source_folder)

    for each in image_paths:
        # 连通域分割
        # images = cfs(Image.open(each))
        # 投影分割
        # images = projection(Image.open(each), pre_conditions=[67, 106, 134])
        # 滴水分割
        # images = drop(Image.open(each), pre_conditions=[67, 106, 134])
        # 连通域+投影
        # images = cfs_projection(Image.open(each), pre_conditions=[67, 106, 134])
        # 连通域+滴水
        images = cfs_drop(Image.open(each), pre_conditions=[67, 106, 134])
        save_images(images, target_folder, get_file_name(each))
        print(each, "is Complete")


if __name__ == '__main__':
    main()
