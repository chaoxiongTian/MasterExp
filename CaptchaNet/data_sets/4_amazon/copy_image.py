# -*- coding: utf-8 -*-
# @Time    : 19-1-26 下午12:51
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : copy_image.py
# @Software: PyCharm
import os
import sys
import random


def save_string_2_file(file_path, file_content):
    f = open(file_path, 'w')
    f.write(file_content)
    f.close()


source_file_suffix = '.png'
target_file_suffix = '.png'


def get_random(new_list, num):
    random.shuffle(new_list)
    return new_list[:num]


def get_order(new_list, num):
    return new_list[:num]


def main():
    commands = sys.argv
    if len(commands) == 1:
        raise RuntimeError("在python xx.py 后面加上文件夹")
    folder, label, num, flag = commands[1], commands[2], int(commands[3]), commands[4]
    print("target folder : {}".format(folder))
    print("target label : {}".format(label))
    print("target num : {}".format(num))
    print("random or order : {}".format(flag))

    image_paths = [os.path.join(folder, str(i) + source_file_suffix) for i in range(len(os.listdir(folder)))]
    labels = open(label, 'r').read().strip().split('#')
    if len(image_paths) != len(labels) or num > len(labels):
        raise RuntimeError("dataset num have error")
    print('data_set num is :{}'.format(len(labels)))

    new_list = list()
    for i in range(len(image_paths)):
        new_list.append((image_paths[i], labels[i]))

    if flag == 'random':
        new_list = get_random(new_list, num)
    elif flag == 'order':
        new_list = get_order(new_list, num)
    else:
        raise ValueError("user input error ")

    target_folder = str(num) + '_' + folder
    new_label_path = str(num) + '_' + label
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    target_labels = list()
    import shutil
    for i, (path, label) in enumerate(new_list):
        print('source path', path)
        print('target path', os.path.join(target_folder, str(i) + target_file_suffix))
        shutil.copy(path, os.path.join(target_folder, str(i) + target_file_suffix))
        target_labels.append(label)
        print("num {} is complete".format(str(i)))
    save_string_2_file(new_label_path, '#'.join(target_labels))


if __name__ == '__main__':
    main()
