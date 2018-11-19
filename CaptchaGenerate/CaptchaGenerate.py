'''
@Description: 
@version: 
@Author: MaxCentaur
@Date: 2018-11-19 17:24:50
@LastEditors: MaxCentaur
@LastEditTime: 2018-11-19 21:58:13
'''
import os
import random
from Captcha import Captcha
dataDir = os.path.join(os.path.split(os.path.abspath(os.sys.argv[0]))[0],"data")
def main():
    # 构造captcha
    captcha = Captcha(
                width = 150,           # 验证码宽
                higt = 38,            # 验证按高
                fontColorRandom = False, # 颜色是否随机
                fontColor = (0,0,0),       # 指定颜色
                fontPathDir = os.path.join(dataDir,"font","captcha"),# 字体路径，多种字体直接全部读出来
                fontSize = 32,        # 字体基准大小
                fontRandomRange = 0, # 字体随机范围
                haveBg = False,          # 是否有背景
                bgPathDri = os.path.join(dataDir,"bg","jd"),       # 有背景的话，背景路径
                label= "abcd"            # 验证码内容
    )
    # captcha.generateCaptcha(os.path.join(dataDir,"captcha","captcha"))
    labelPath = os.path.join(dataDir,"labels","labels.txt")
    labelsList = open(
        labelPath, 'r', encoding="utf-8").read().strip().split("#")
        # 循环生成
    captchaDir = os.path.join(dataDir,"captcha","captcha")
    for i, each in enumerate(labelsList):
        captchaPath = os.path.join(captchaDir, str(i) + '.png')
        print(captchaPath)
        captcha.generateCaptcha(each,captchaPath)
if __name__ == "__main__":
    main()