'''
@Description: 
@version: 
@Author: MaxCentaur
@Date: 2018-11-20 21:06:01
@LastEditors: MaxCentaur
@LastEditTime: 2018-11-20 21:30:58
'''
import os
import sys
from PIL import Image, ImageDraw, ImageFont
charSetComplete = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
    'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
    'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
]
def getList(dir):
    def f(x):
        return os.path.join(dir,x)
    return list(map(f,os.listdir(dir)))
def generateImage(string,fontPath):
    (_, extension) = os.path.splitext(fontPath)
    if extension == '.ttf' or extension == '.TTF'or extension == '.otf':
        font = ImageFont.truetype(fontPath,80)
        image = Image.new('RGBA',(font.getsize(string)),(255,255,255))
        charDraw = ImageDraw.Draw(image)
        charDraw.text((0,0), string, (0,0,0), font=font)
        del charDraw
        image.save(os.path.splitext(fontPath)[0]+".png")

def generate():
    string = ' '.join(charSetComplete)
    dataDir = os.path.join(os.path.split(os.path.abspath(os.sys.argv[0]))[0],"CandidateFont")
    fontList = getList(dataDir)
    for each in fontList:
        generateImage(string,each)
if __name__ == "__main__":
    generate()