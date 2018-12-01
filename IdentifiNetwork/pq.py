# -*- coding: utf-8 -*-
# @Time    : 18-11-30 下午10:04
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : pq.py
# @Software: PyCharm Community Edition

import tensorflow as tf
# 导入命令行解析模块
import argparse
import sys

FLAGS = None


def main(_):
    print(sys.argv[0])


if __name__ == "__main__":  # 用这种方式保证了，如果此文件被其他文件import的时候，不会执行main中的代码
    # # 创建对象
    # parse = argparse.ArgumentParser()
    # # 增加命令行
    # parse.add_argument('--dataDir', type=str, default='\\tmp\\tensorflow\\mnist\\inputData',
    #                    help='Directory for string input data')
    # FLAGS, unparsed = parse.parse_known_args()
    tf.app.run(main=main)  # 解析命令行参数，调用main函数 main(sys.argv)
