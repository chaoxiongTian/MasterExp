'''
@Description: 
@version: 
@Author: MaxCentaur
@Date: 2018-11-19 17:24:50
@LastEditors: MaxCentaur
@LastEditTime: 2018-11-28 17:35:50
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
                haveBg = False,          # 是否有背景
                bgPathDri = os.path.join(dataDir,"bg","jd"),       # 有背景的话，背景路径
                fontColor = (0,0,0),       # 指定颜色
                fontPathDir = os.path.join(dataDir,"font","captcha"),# 字体路径，多种字体直接全部读出来
                fontSize = 32,        # 字体基准大小
                fontRandomRange = 0, # 字体随机范围
                
    )
    labelPath = os.path.join(dataDir,"labels","labels.txt")
    labelsList = open(
        labelPath, 'r', encoding="utf-8").read().strip().split("#")
    captchaDir = os.path.join(dataDir,"captcha","captcha")
    for i, each in enumerate(labelsList):
        captchaPath = os.path.join(captchaDir, str(i) + '.png')
        print(captchaPath)
        captcha.generateCaptcha(each,captchaPath)
def Blizzard():
    # 构造captcha
    captcha = Captcha(
                width = 150,           # 验证码宽
                higt = 30,            # 验证按高
                haveBg = False,          # 是否有背景
                bgPathDri = os.path.join(dataDir,"bg","Blizzard"),       # 有背景的话，背景路径
                startX = 0,      # 第一个字符的开始位置
                step = 10,       # 每个字符之间的距离
                fontPathDir = os.path.join(dataDir,"font","Blizzard"),     # 字体路径，多种字体直接全部读出来
                fontColor = (0,0,0),       # 指定颜色(处理之后都需要二值化，所以可不用随机颜色)
                fontSize = 32,        # 字体基准大小
                fontRandomRange = 0  # 字体随机范围
    )
    labelPath = os.path.join(dataDir,"labels","labelsBlizzard.txt")
    labelsList = open(
        labelPath, 'r', encoding="utf-8").read().strip().split("#")
    captchaDir = os.path.join(dataDir,"captcha","Blizzard")
    print("generate %d captcha in %s\n" % (len(labelsList),captchaDir))
    for i, each in enumerate(labelsList):
        captchaPath = os.path.join(captchaDir, str(i) + '.png')
        captcha.generateCaptcha(each,captchaPath)
        print("Nub.%d in complete"%i)
if __name__ == "__main__":
    Blizzard()