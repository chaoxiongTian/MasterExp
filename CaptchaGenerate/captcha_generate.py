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
    'megaupload': generate_megaupload,  # 4
    'blizzard': generate_blizzard,  # 6
    'authorize': generate_authorize,  # 5
    'captcha_net': generate_captcha_net,  # 5
    'nih': generate_nih,  # 5
    'reddit': generate_reddit,  # 6
    'digg': generate_digg,  # 5
    'baidu': generate_baidu,  # 4
    'qq': generate_qq,  # 4
    'sina_2014': generate_sina_2014,  # 5
    'recaptcha_2011': generate_recaptcha_2011,  # 8

    'amazon': generate_amazon,  # 6
    'yahoo': generate_yahoo,  # 7

    'recaptcha_2013': generate_recaptcha_2013,  # 6
    'baidu_2013': generate_baidu_2013,  # 4
    'baidu_2011': generate_baidu_2011,  # 4
    'cnn': generate_cnn,  # 5
    'paypal': generate_paypal,  # 5
}


def save_images(ims, ims_clean, folder, single_folder, padding=20):
    for i in range(len(ims)):
        if opt.origin_captcha:
            # im = image_resize_scale(ims[i], 256, padding)
            ims[i].save(os.path.join(folder, str(i) + '.png'))
        else:
            im = image_resize_scale(ims[i], 256, padding)
            im_clean = image_resize_scale(ims_clean[i], 256, padding)
            if single_folder is not None:
                im_clean.save(os.path.join(single_folder, str(i) + '.png'))
            image_merge_horizontal(im, im_clean).save(os.path.join(folder, str(i) + '.png'))
        print("Nub.{} in saved".format(str(i)))


def generate(captcha, labels, feature):
    ims = list()
    ims_clean = list()
    for i, each in enumerate(labels):
        image, image_clean = generate_captcha(captcha, each, feature)
        if captcha.contours and not opt.origin_captcha:
            image = outline(image)
        ims.append(image)
        ims_clean.append(image_clean)
        print("Nub.%d in generated" % i)
    return ims, ims_clean


def main():
    label_path = os.path.join(data_folder, "labels", opt.captcha + "_" + opt.labels + "_labels.txt")
    labels = open(label_path, 'r', encoding="utf-8").read().strip().split("#")

    captcha_save_folder = os.path.join(data_folder, "captcha", opt.captcha)
    save_folder = os.path.join(captcha_save_folder, opt.tar)
    make_folders(save_folder)

    single_char_folder = None
    if opt.single_char:
        single_char_folder = os.path.join(captcha_save_folder, 'clean')
        make_folders(single_char_folder)

    captcha, feature = switch[opt.captcha](opt.captcha)
    images, images_clean = generate(captcha, labels, feature)

    save_images(images, images_clean, save_folder, single_char_folder)


if __name__ == "__main__":
    main()
