# -*- coding: utf-8 -*-
"""
1. 删除,重新命名文件夹
"""
__author__ = 'big_centaur'
import os
def main():
    root = '/home/tianchaoxiong/LinuxData/paper/experiment/segment/3_ebay/cnn_pro/datasets/test/images'
    commond = 'cd '+root
    os.system(commond)
    commond = 'rm *captcha.png'
    os.system(commond)

if __name__ == '__main__':
    main()
