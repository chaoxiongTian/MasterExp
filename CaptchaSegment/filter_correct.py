# -*- coding: utf-8 -*-
"""
1. 过滤出cfs算法 切分之后数量正确的和数量不正确的 对不正确的使用算法进行再次分割
"""
__author__ = 'big_centaur'
import os
import shutil
from cfs_update1 import cfs_no_save
from cfs_update1 import save_segmented_image_list
from cfs_dropfall import cfs_dropfall
from cfs import get_block_info

def mkdir(path):
    """
    判断文件夹是不是存在,不存在创建
    """
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        pass

def is_onechar(w_list,flag):
    for each in w_list:
        if int(each)>int(flag):
            return False
        else:
            pass
    return True

def get_segmented_list(segmented_pixel_list):
    w_list = []
    for i, each_block in enumerate(segmented_pixel_list):
        # 获取每个区块的长宽 和长宽的其实起始位置
        block_w, _, _, _ = get_block_info(each_block)
        w_list.append(block_w)
    return w_list

def recurve_2(folder1, folder2, folder3, folder4):
    """
    遍历folder1 并拷贝文件到folder2
    :param folder1: 遍历位置
    :param folder2: 存储位置1
    :param folder3: 存储位置2
    :param folder4: 存储位置3
    :return:
    """
    # mkdir(folder2)
    # mkdir(folder3)
    mkdir(folder4)
    for i,file in enumerate(os.listdir(folder1)):
        print('processing %d '%i)
        source_file1 = os.path.join(folder1, file)
        target_file2 = os.path.join(folder2, file)
        target_file3 = os.path.join(folder3, file)
        target_file4 = os.path.join(folder4, file)
        if os.path.isfile(source_file1):
            (path, extension) = os.path.splitext(source_file1)
            index = str(path).split('/')[-1]
            target_file4 = os.path.join(folder4, index)
            if extension == '.jpg' or extension == '.png':
                # do something
                print("%s processing %d" % (source_file1,i))
                segmented_pixel_list, num = cfs_no_save(source_file1)
                if num == 6:
                    save_segmented_image_list(segmented_pixel_list, target_file4)
                    # shutil.copy(source_file1, target_file2)
                    # 对每个区块的长度也进行过滤
                    # w_list = get_segmented_list(segmented_pixel_list) # 每个区块都必须小于39
                    # if is_onechar(w_list,39):
                    #     shutil.copy(source_file1, target_file2)
                    #     # save_segmented_image_list(segmented_pixel_list, target_file4)
                    pass
                else:
                    # shutil.copy(source_file1, target_file3)
                    # save_segmented_image_list(segmented_pixel_list, target_file4)
                    # cfs_dropfall(source_file1, target_file4)
                    pass

        else:
            recurve_2(source_file1, target_file2, target_file3, target_file4)


def main():
    """
    :return: 入口
    """
    import time
    start = time.clock()
    image_floder = '/home/tianchaoxiong/LinuxData/paper/experiment/segment/3_ebay/cnn_pro/datasets/train_2/B/'
    root_1 = image_floder+'train_otsu'  # 源文件位置
    root_2 = image_floder+'se_op/correct'  # 切分数量正确的位置
    root_3 = image_floder+'se_op/error'  # 切分数量不正确的位置
    root_4 = image_floder+'se_op/se_result'  # 最后的存储位置
    recurve_2(root_1, root_2, root_3,
              root_4)  # root1 为原始文件夹, root2 为正确分割的文件夹, root3 为防止不能真确分割的文件夹
    end = time.clock()
    print('Running time: %s Seconds'%(end-start))
if __name__ == '__main__':
    main()
