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
        each.save(target_name_srefix + '-' + str(i) + ".png")


def main():
    source_folder = '/home/tianchaoxiong/LinuxData/code/pythonpro/MasterExp/CaptchaSegment/data/qq'
    target_folder = source_folder + '_cfs_pro'
    make_folder(target_folder)

    for each in get_internal_path(source_folder):
        # 连通域分割
        # images = cfs(Image.open(each))
        # 投影分割
        # images = projection(Image.open(each), pre_conditions=[67, 106, 134])
        # 滴水分割
        # images = drop(Image.open(each), pre_conditions=[67, 106, 134])
        # 连通域+投影
        images = cfs_projection(Image.open(each), pre_conditions=[61, 182, 183])
        # 连通域+滴水
        # images = cfs_drop(Image.open(each), pre_conditions=[67, 106, 134])
        save_images(images, target_folder, get_file_name(each))
        print("images num is : %d" % len(images))
        print(each, "is Complete")


if __name__ == '__main__':
    main()
