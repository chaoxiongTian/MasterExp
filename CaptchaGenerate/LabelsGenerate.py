'''
@Description: 1. 随机生成指定为的验证码,用#号隔开
@version: 
@Author: MaxCentaur
@Date: 2018-11-14 17:38:30
@LastEditors: MaxCentaur
@LastEditTime: 2018-11-15 16:03:24
'''
import os
import sys
import random
from CaptchaLabel import CaptchaLabel
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir)))
from Utils import Utils

# TODO：
def getCharList():
    charSetComplete = [
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
        'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
        'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ]
    charSetLive = [
        '3', '4', '5', '6',
        'd','p','s','y',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
        'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ]
    charSetSohu = [
        '2', '3', '4', '5', '6', '7', '8', '9',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'm', 'n', 'p',
        'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y'
    ]
    charSetEBay = [
        '2', '3', '4', '5', '6', '7', '8', '9',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'M', 'N',
        'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ]
    charSetBaidu = [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
        'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y'
    ]
    charSet360 = [
        '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'm', 'n', 'p', 'q',
        'r', 's', 'u', 'v', 'w', 'x', 'y', 'z',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'M', 'N', 'P', 'Q',
        'R', 'S', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ]
    charSetJd = [
        '3', '4', '5', '6', '8',
        'A', 'B', 'C', 'E', 'F', 'H', 'K', 'M', 'N', 'R', 'S', 'T', 'U', 'V',
        'W', 'X', 'Y'
    ]
    charSetWeibo = [
        '2', '3', '4', '6', '7', '8', '9',
        'A', 'B', 'C', 'E', 'F', 'H', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'R',
        'S', 'T', 'V', 'W', 'X', 'Y', 'Z'
    ]
    charSetEbay = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    charSetSina = [
        '2', '3', '4', '5', '6', '7', '8',
        'a', 'b', 'c', 'd', 'e', 'f', 'h', 'k', 'm', 'n', 'p', 'q', 's', 'u',
        'v', 'w', 'x', 'y', 'z',
        'A', 'B', 'C', 'E', 'F', 'G', 'H', 'K', 'M', 'N', 'P', 'Q', 'R', 'S',
        'U', 'V', 'W', 'X', 'Y', 'Z'
    ]
    return charSetComplete

def generate(charList,captchaNumber,captchaLen):
    label = CaptchaLabel(charList,captchaLen)
    labels = []
    for _ in range(1000):
        labels.append(label.getLabel())
    return '#'.join(labels)
def main():
#     创建文件夹
    dataDir = os.path.join(os.path.split(os.path.abspath(os.sys.argv[0]))[0],"data/labels")
    utils = Utils()
    utils.makeDir(dataDir)

    charList = getCharList()
    captchaNumber = 10000
    captchaLen= 6
    labels = generate(charList,captchaNumber,captchaLen)
    utils.saveStringFile(os.path.join(dataDir,"labels.txt"),labels)

if __name__ == '__main__':
    main()
