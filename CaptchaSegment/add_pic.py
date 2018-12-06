# -*- coding: utf-8 -*-
"""
1. 打开一张图片 再某个位置粘贴一些东西
"""
from PIL import Image


def add_image(image_path, target_x, target_y):
    """
    在image的 target位置粘贴白色的小图片
    """
    image = Image.open(image_path)
    small_image = Image.new('RGB', (30, 30), (255, 255, 255))
    image.paste(small_image, (target_x, target_y))
    image.save(image_path)


def main():
    """
    入口
    """
    image_path = '/home/tianchaoxiong/LinuxData/paper/experiment/segment/11_sina/net/results_3/images_otsu/0.png'
    add_image(image_path, 256 - 30, 0)


if __name__ == '__main__':
    main()