# -*- coding: utf-8 -*-
# @Time    : 19-1-8 上午10:18
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : find_range.py
# @Software: PyCharm

from out_utils import *
from segment_cfs import cfs


def main():
    source_folder = '/home/tianchaoxiong/LinuxData/data/MasterExpData/after/qq_2/qq_200/qq_pix2pix/test_latest/images'
    target_folder = source_folder+'_range'
    make_folder(target_folder)
    image_paths = get_internal_path(source_folder)
    images = list()
    for i, each in enumerate(image_paths):
        images.extend(cfs(Image.open(each)))
        print('num. {} has segment'.format(str(i)))
    images_info = []
    for each in images:
        images_info.append((each, each.size[0]))
    images_info = sorted(images_info, key=lambda x: x[1])
    for i, (each, _) in enumerate(images_info):
        target_path = os.path.join(target_folder, str(i) + '.png')
        print(target_path)
        each.save(target_path)


if __name__ == '__main__':
    main()
