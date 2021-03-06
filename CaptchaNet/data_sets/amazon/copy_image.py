# -*- coding: utf-8 -*-
# @Time    : 18-12-27 下午7:49
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : ceshi.py
# @Software: PyCharm

import sys


def save_string_2_file(file_path, file_content):
    f = open(file_path, 'w')
    f.write(file_content)
    f.close()


def main():
    commands = sys.argv
    if len(commands) == 1:
        raise RuntimeError("在python xx.py 后面加上文件夹")
    folder, label, num = commands[1], commands[2], commands[3]
    print("target folder : {}".format(folder))
    print("target label : {}".format(label))
    print("target num : {}".format(num))
    import os
    image_paths = [os.path.join(folder, str(i) + '.png') for i in range(len(os.listdir(folder)))]
    labels = open(label, 'r').read().strip().split('#')

    new_list = list()
    for i in range(len(image_paths)):
        new_list.append((image_paths[i], labels[i]))
    import random
    random.shuffle(new_list)
    num = int(num)
    if num < len(new_list):
        new_list = new_list[:num]
    else:
        raise RuntimeError("input num bigger than num image num")
    target_folder = str(num) + '_' + folder
    new_label_path = str(num) + '_' + label
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    target_labels = list()
    import shutil
    for i, (path, label) in enumerate(new_list):
        shutil.copy(path, os.path.join(target_folder, str(i) + '.png'))
        target_labels.append(label)
        print("num {} is complete".format(str(i)))
    save_string_2_file(new_label_path, '#'.join(target_labels))


if __name__ == '__main__':
    main()
