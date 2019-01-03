# -*- coding: utf-8 -*-
# @Time    : 18-11-29 下午10:49
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : CaptchaGenerate.py
# @Software: PyCharm Community Edition

from options import Options
from generate_unit import *

opt = Options().parse()


switch = {
    'megaupload': generate_megaupload,
    'blizzard': generate_blizzard,
    'authorize': generate_authorize,
    'captcha': generate_captcha,
    'nih': generate_nih,
    'reddit': generate_reddit,
    'digg': generate_digg,
    'baidu': generate_baidu,
    'qq': generate_qq
}

if __name__ == "__main__":
    label_path = os.path.join(data_folder, "labels", opt.captcha + "_" + opt.labels + "_labels.txt")
    labels = open(label_path, 'r', encoding="utf-8").read().strip().split("#")

    captcha_save_folder = os.path.join(data_folder, "captcha", opt.captcha)
    save_folder = os.path.join(captcha_save_folder, opt.tar)
    make_folders(save_folder)

    switch[opt.captcha](labels, save_folder)
