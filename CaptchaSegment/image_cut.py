# -*- coding: utf-8 -*-
"""
1. 使用分割算法案进行分割
"""
__author__ = 'big_centaur'

import os
# from cfs_dropfall import cfs_dropfall
from cfs_update1 import cfs
# from projection_update1 import projection
# from dropfall import dropfall


def recurve_2(folder1, folder2):
    """
    遍历folder1 并拷贝文件到folder2
    :param folder1: 遍历位置
    :param folder2: 存储位置
    :return:
    """
    if not os.path.exists(folder2):
        os.makedirs(folder2)
    for i, file in enumerate(os.listdir(folder1)):
        source_file = os.path.join(folder1, file)
        target_file = os.path.join(folder2, file)
        if os.path.isfile(source_file):
            (_, extension) = os.path.splitext(source_file)
            (path, _) = os.path.splitext(target_file)
            if extension == '.jpg' or extension == '.png':
                # do something
                print("%s processing  %d." % (source_file,i))
                cfs(source_file, path)

        else:
            recurve_2(source_file, target_file)


def main():
    """
    入口函数
    """
    root_1 = '/home/tianchaoxiong/LinuxData/paper/experiment/segment/11_sina/pix_pro/results_3/op/error'
    root_2 = '/home/tianchaoxiong/LinuxData/paper/experiment/segment/11_sina/pix_pro/results_3/op/error_se_cfs'
    recurve_2(root_1, root_2)
    # path = '/home/tianchaoxiong/LinuxData/paper/experiment/segment/wiki/Wiki_200/61.png'
    # cfs(path, 'data/')


if __name__ == '__main__':
    main()
