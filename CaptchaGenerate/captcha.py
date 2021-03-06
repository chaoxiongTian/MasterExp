# -*- coding: utf-8 -*-
# @Time    : 18-11-29 下午10:49
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : Captcha.py
# @Software: PyCharm Community Edition

from captcha_utils import *

MUL = 4  # 制作验证码的时候，为了保证图片的清晰度。先制作原图MUL倍大小的图片，然后再缩小回需要的大小

"""
       为满足项目需求，本方法在生成验证码时是成对生成的。这对验证码需要保证同样的扭曲程度和同样的旋转角度。
       如果生成一张有背景的验证码，那么就会生成一张去除干扰信息的验证码
       如果生成一张字符粘连的验证码，那么就会生成一张字符之间没有粘连的验证码。
       如果生成一张有背景且字符粘连的验证码，那么就会生成一张没有背景且字符未粘连的验证码。

       所以调用的诸多方法中都会返回两个Image，或者两组Images，其含义就是两个对应的Image，或者两组对应的Images。
       比如image和image_clean  images和Images_clean
"""


# 把一组字符的Image对象粘贴到背景的Iamge对象上面。
def default_paste(captcha, bg_image, bg_image_clean, images, images_clean):
    # 每两个字符之间的距离的step，有个验证码字符之间是随机的，所以在此基础上添加一个数据数组。
    step_randoms = []
    for i in range(len(images)):
        step_randoms.append(random.randint(-captcha.step_random_range, captcha.step_random_range))

    offset_y_randoms = []
    for i in range(len(images)):
        offset_y_randoms.append(random.randint(-captcha.offset_y_range, captcha.offset_y_range))
    # TODO：目的（把char的Image对象粘贴到对象背景上粘连上去）

    # 1. 预估images+step和step_randoms需要的长度，若背景image对象不够长，先调整背景image长度。
    start_rio = abs(random.randint(captcha.start_x - captcha.start_x_random_range,
                                   captcha.start_x + captcha.start_x_random_range))
    target_width = pre_calc(start_rio, captcha.step, images, step_randoms)
    if target_width > captcha.captcha_width:
        # 重新调整背景的大小
        bg_image = bg_image.resize((target_width, captcha.captcha_high), Image.ANTIALIAS)

    target_width_clean = pre_calc(start_rio, captcha.step_stretch, images_clean, step_randoms)
    if target_width_clean > captcha.captcha_width:
        bg_image_clean = bg_image_clean.resize((target_width_clean, captcha.captcha_high), Image.ANTIALIAS)

    # 2. 开始粘贴 为了保证一致，对于含有背景和没有背景的一起粘贴。
    offset_x = start_rio
    offset_y = 0
    offset_x_clean = start_rio
    offset_y_clean = 0
    for i in range(len(images)):
        char_w, char_h = images[i].size
        char_w_clean, char_h_clean = images_clean[i].size
        bg_image.paste(images[i],
                       (offset_x, int((captcha.captcha_high - char_h) / 2) + offset_y_randoms[i]),
                       images[i]
                       )
        bg_image_clean.paste(images_clean[i],
                             (offset_x_clean, int((captcha.captcha_high - char_h_clean) / 2) + offset_y_randoms[i]),
                             images_clean[i]
                             )
        offset_x = offset_x + char_w + captcha.step + step_randoms[i]
        offset_x_clean = offset_x_clean + char_w_clean + captcha.step_stretch + step_randoms[i]
    bg_image = bg_image.resize((captcha.captcha_width, captcha.captcha_high), Image.ANTIALIAS)
    bg_image_clean = bg_image_clean.resize((captcha.captcha_width, captcha.captcha_high), Image.ANTIALIAS)
    return bg_image, bg_image_clean


#  根据label生成验证码  扭曲，旋转和干扰信息都是缺省调用。
def generate_captcha(captcha, label, feature):
    (fun_paste,  # 粘贴函数 默认为None则调用default_paste
     # None
     inter_line, draw_feature,  # 干扰线函数，干扰线特征
     # None,None
     wave, get_wave_feature,  # 波浪函数，波浪特征
     # None,None
     list_1, list_2,  # 扭曲特征
     # (0,0), (0,0)
     flag, rotate_start, rotate_end,  # 旋转特征(flag 表示字符都是0,一个方向还是1多个方向)
     # 0,0,0
     noise_number, noise_width, noise_color  # 干扰线特征
     # 0, 0, (0,0,0)
     ) = feature
    # 1. 生成两张对象的背景
    bg_image, bg_image_clean = captcha.get_captcha_bg()
    # 2. 生成两组对应的Images
    images, images_clean = captcha.get_char_images(label)
    # 对两组Images同事进行旋转
    if flag == 1:
        rotate_start = rotate_end = random.randint(rotate_start, rotate_end)
    images, images_clean = rotate_images(images, images_clean, rotate_start, rotate_end)
    # 对两组Images同事进行扭曲
    images, images_clean = warp_images(images, images_clean, list_1, list_2)
    if fun_paste is None:
        fun_paste = default_paste
    image, image_clean = fun_paste(captcha, bg_image, bg_image_clean, images, images_clean)
    image = zoom_down_mul(image, captcha.mul)
    image_clean = zoom_down_mul(image_clean, captcha.mul)
    image = add_noise(image, noise_number, noise_width, noise_color)
    if inter_line is not None:
        image = inter_line(image, draw_feature)
    if wave is not None:
        image = wave(image, get_wave_feature())
        image_clean = wave(image_clean, get_wave_feature())
    return image, image_clean


class Captcha(object):
    def __init__(self,
                 captcha_width,  # 验证码宽
                 captcha_high,  # 验证按高
                 have_bg,  # 是否有背景
                 bg_folder,  # 有背景的话，背景路径

                 font_folder,  # 字体路径，多种字体直接全部读出来
                 font_color,  # 指定颜色(处理之后都需要二值化，所以可不用随机颜色)
                 font_size,  # 字体基准大小
                 font_size_random_range,  # 字体随机范围
                 font_bg_color=None,

                 start_x=0,  # 第一个字符在验证码中开始位置
                 start_x_random_range=0,  # 开始位置随机在start_x的一个区间
                 offset_y_range=0,  # 粘连字符的时候在Y轴上的一个随机区间。
                 step=10,  # 每两个之间的距离
                 step_stretch=10,  # 保证不粘连时，每两个字符之间的距离
                 step_random_range=0,  # 每两个字符之距离的随机值
                 font_folder_clean="null",  # 对照转换的验证码中的字体位置（未传参表示同一种）（用于空心到实心的转换）
                 bg_color=(255, 255, 255),  # 没有背景时，验证码的背景色
                 mul=MUL,
                 contours=False
                 ):

        self.mul = mul
        self.captcha_width = captcha_width * self.mul
        self.captcha_high = captcha_high * self.mul
        self.have_bg = have_bg
        self.bg_folder = bg_folder
        self.bg_color = bg_color
        self.start_x = start_x * self.mul
        self.start_x_random_range = start_x_random_range * self.mul
        self.step = step * self.mul
        self.step_stretch = step_stretch * self.mul
        self.step_random_range = step_random_range * self.mul
        self.offset_y_range = offset_y_range * self.mul
        self.font_folder = font_folder
        self.font_bg_color = font_bg_color
        self.contours = contours

        if font_folder_clean.__eq__("null"):  # 没有传入参数，就说明用的同一种字体
            self.font_folder_clean = font_folder
        else:
            self.font_folder_clean = font_folder_clean

        self.font_color = font_color
        self.font_size = font_size * self.mul
        self.font_size_random_range = font_size_random_range * self.mul

        print(self)  # 打印类信息

    # 定制打印
    def __str__(self):
        return ("Captcha info\n-----------\n(captcha_width: %s)" % self.captcha_width
                + "\n(captcha_higt: %s)" % self.captcha_high
                + '\n(have_bg: %s)' % self.have_bg
                + '\n(bg_folder: %s)' % self.bg_folder
                + '\n(start_x: %s)' % self.start_x
                + '\n(step: %s)' % self.step
                + '\n\nchar info\n-----------\n(font_color:' + str(self.font_color) + ")"
                + '\n(font_folder: %s)' % self.font_folder
                + '\n(font_size: %s)' % self.font_size
                + '\n(font_size_random_range: %s)' % self.font_size_random_range + "\n-----------\n")

    # 拿到两个对应的背景
    def get_captcha_bg(self):
        """根据参数返回两个Image，一个是含有背景的，一个是去除背景的"""
        if self.have_bg:
            # 有背景的话，随机取出一个背景。
            bg_image_path = random.choice(get_internal_path(self.bg_folder))
            bg_image = Image.open(bg_image_path)
            bg_image = bg_image.resize((self.captcha_width, self.captcha_high), Image.ANTIALIAS)
            bg_image_clean = Image.new('RGBA', (self.captcha_width, self.captcha_high), (255, 255, 255))
            return bg_image, bg_image_clean
        else:
            # 生成一个新的白底背景 
            bg_image = Image.new('RGBA', (self.captcha_width, self.captcha_high), self.bg_color)
            bg_image_clean = Image.new('RGBA', (self.captcha_width, self.captcha_high), (255, 255, 255))
            return bg_image, bg_image_clean

    # 拿到两组对应的Images
    def get_char_images(self, label):
        """根据labels生成 char的Image对象列表"""

        images = []  # 生成一组字符的Image对象
        images_clean = []  # 对应的没有干扰信息的字符的Image对象
        for each in label:
            # 确定字体的大小
            font_size = random.randint(self.font_size - self.font_size_random_range,
                                       self.font_size + self.font_size_random_range)
            # 确定字体的路径
            font_path = random.choice(get_internal_path(self.font_folder))
            font_path_clean = random.choice(get_internal_path(self.font_folder_clean))
            # 生成
            images.append(generate_char_images(each, font_path, font_size, self.font_color, self.font_bg_color))
            images_clean.append(generate_char_images(each, font_path_clean, font_size))
        return images, images_clean
