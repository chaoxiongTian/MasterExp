# -*- coding: utf-8 -*-
"""
1. 找到字符的区域
"""
__author__ = 'big_centaur'

import os
import shutil
from PIL import Image

folder = '/home/tianchaoxiong/LinuxData/paper/experiment/segment/1_JD/cnn_pro/datasets/test/se_op/se_result'
folder2 = folder+'_tmp'
if not os.path.exists(folder2):
    os.makedirs(folder2)
images_path = []
for i, each in enumerate(os.listdir(folder)):
    source_path = os.path.join(folder, each)
    # images.append([Image.open(source_path), Image.open(source_path).size[0]])
    images_path.append([source_path, Image.open(source_path).size[0]])
images_path = sorted(images_path, key=lambda x: x[1])
for i, (each, _) in enumerate(images_path):
    target_path = os.path.join(folder2, str(i) + '.png')
    print(each)
    print(target_path)
    shutil.copy(each, target_path)
