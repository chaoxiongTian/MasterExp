# -*- coding: utf-8 -*-
# @Time    : 18-12-10 下午8:10
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : segment_image.py
# @Software: PyCharm

from cfs import cfs
from out_utils import *


def main():
    target_folder = os.path.join(data_folder, "cfs")
    make_folder(target_folder)
    images = cfs(os.path.join(target_folder, "1.png"))
    images[0].show()


if __name__ == '__main__':
    main()
