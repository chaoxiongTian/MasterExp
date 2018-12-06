from pdb import set_trace as st
import os
import numpy as np
import cv2
import argparse

# 调用方式 python datasets/combine_A_and_B.py --fold_A /path/to/data/A --fold_B /path/to/data/B --fold_AB /path/to/data

parser = argparse.ArgumentParser('create image pairs')
parser.add_argument('--fold_A', dest='fold_A', help='input directory for image A',
                    type=str, default='../dataset/50kshoes_edges')
parser.add_argument('--fold_B', dest='fold_B', help='input directory for image B',
                    type=str, default='../dataset/50kshoes_jpg')
parser.add_argument('--fold_AB', dest='fold_AB', help='output directory', type=str,
                    default='../dataset/test_AB')
parser.add_argument('--num_imgs', dest='num_imgs', help='number of images', type=int,
                    default=1000000)
parser.add_argument('--use_AB', dest='use_AB', help='if true: (0001_A, 0001_B) to (0001_AB)',
                    action='store_true')
args = parser.parse_args()

for arg in vars(args):
    print('[%s] = ' % arg, getattr(args, arg))

splits = os.listdir(args.fold_A)
# splits 是一个fold_A文件夹下文件名的list
for sp in splits:
    # 分别输出文件夹下所有文件
    img_fold_A = os.path.join(args.fold_A, sp)  # 把fold_A 和sp 拼接起来的路径
    img_fold_B = os.path.join(args.fold_B, sp)
    img_list = os.listdir(img_fold_A)
    # img_list 包含 img_fold_A 目录下的所有文件
    # 只有文件名称  不是路径吗
    if args.use_AB:
        # 缩小img_list的范围 让他只包含有_A的文件文件名
        img_list = [img_path for img_path in img_list if '_A.' in img_path]

    num_imgs = min(args.num_imgs, len(img_list))
    # sp文件夹的名称  num_imgs 默认或者文件个数最小的哪一个
    print('split = %s, use %d/%d images' % (sp, num_imgs, len(img_list)))

    img_fold_AB = os.path.join(args.fold_AB, sp)
    if not os.path.isdir(img_fold_AB):
        os.makedirs(img_fold_AB)
    print('split = %s, number of images = %d' % (sp, num_imgs))
    for n in range(num_imgs):
        name_A = img_list[n]
        path_A = os.path.join(img_fold_A, name_A)
        if args.use_AB:
            name_B = name_A.replace('_A.', '_B.')
        else:
            name_B = name_A
        path_B = os.path.join(img_fold_B, name_B)
        if os.path.isfile(path_A) and os.path.isfile(path_B):
            name_AB = name_A
            if args.use_AB:
                name_AB = name_AB.replace('_A.', '.')  # remove _A
            path_AB = os.path.join(img_fold_AB, name_AB)
            im_A = cv2.imread(path_A, cv2.IMREAD_COLOR)
            im_B = cv2.imread(path_B, cv2.IMREAD_COLOR)
            im_AB = np.concatenate([im_A, im_B], 1)
            cv2.imwrite(path_AB, im_AB)
