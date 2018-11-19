'''
@Description: 工具类
@version: 1.0
@Author: MaxCentaur
@Date: 2018-11-14 22:59:38
@LastEditors: MaxCentaur
@LastEditTime: 2018-11-19 22:45:03
'''
import os
import random
from PIL import Image, ImageDraw, ImageFont
dataDir = os.path.join(os.path.split(os.path.abspath(os.sys.argv[0]))[0],"data")
class CharUtit(object):
    def __init__(self,
        fontList,
        fontSize,
        fontRandomRange,
        fontColor
    ):
        self.char = ""
        self.fontList = fontList
        self.fontSize = fontSize
        self.fontColor = fontColor
        self.fontRandomRange = fontRandomRange
    def generateChar(self,char):
        self.char = char
        fontPath = random.choice(self.fontList)
        fontSize = random.randint(self.fontSize-self.fontRandomRange,self.fontSize+self.fontRandomRange)
        font = ImageFont.truetype(fontPath,fontSize)
        # print("charW, charH:"+str(font.getsize(char)))
        charImage = Image.new('RGBA',(font.getsize(char)),(255,255,255))
        charDraw = ImageDraw.Draw(charImage)
        # TODO: 这里的Draw.text存在问题，需要修改。
        charDraw.text((0,-5), self.char, (0,0,0), font=font)
        # saveDir = os.path.join(dataDir,"captcha","ceshi.jpg")
        # charImage.save(saveDir)
        # charImage.show()
        return charImage
        
class Captcha(object):
    def __init__(self,
            width,           # 验证码宽
            higt,            # 验证按高
            fontColorRandom, # 颜色是否随机
            fontColor,       # 指定颜色
            fontPathDir,     # 字体路径，多种字体直接全部读出来
            fontSize,        # 字体基准大小
            fontRandomRange, # 字体随机范围
            haveBg,          # 是否有背景
            bgPathDri,       # 有背景的话，背景路径
            label ="abcd"            # 验证码内容
            ):
        self.width = width
        self.higt = higt
        self.fontColorRandom = fontColorRandom
        self.fontColor = fontColor
        self.fontPathDir = fontPathDir
        self.fontSize = fontSize
        self.fontRandomRange = fontRandomRange
        self.haveBg = haveBg
        self.bgPathDri =bgPathDri
        self.label = label
    
    def getList(self,dir):
            def f(x):
                return os.path.join(dir,x)
            return list(map(f,os.listdir(dir)))
    
    def getCaptchaBg(self):
        if(self.haveBg):
            # 有背景的话，随机取出一个背景。
            bgImagePath = random.choice(self.getList(self.bgPathDri))
            bgImage = Image.open(bgImagePath)
        else:
            # 生成一个shitang新的白底背景 
            bgImage = Image.new('RGBA', (self.width,  self.higt), (255,255,255))
        return bgImage
    
    def pasteCharImageList(self,bgImage,charImageList,startX=0,step=10):
        # 把生成好的字符图片粘连上去
        # 预估调整 1.开始位置startX； 2，间距offsetX
        preCalc = startX
        for i in range(len(charImageList)-1):
            eachW = charImageList[i].size[0]
            preCalc = preCalc+eachW+step
        preCalc = preCalc+charImageList[-1].size[0]
        # print("预估长度："+str(preCalc))
        # 计算预估长度和背景图片的大小
        bgImageW,bgImageH = bgImage.size
        if(preCalc>bgImageW): 
            # 重新调整背景的大小
            bgImage = bgImage.resize((preCalc,bgImageH),Image.ANTIALIAS)
        # 开始粘贴
        offsetX = startX;offsetY = 0
        for each in charImageList:
            charW,charH = each.size;mask = each
            bgImage.paste(each,(offsetX,int((bgImageH-charH)/2)),mask)
            offsetX = offsetX+charW+step
        bgImage = bgImage.resize((bgImageW,bgImageH),Image.ANTIALIAS)
        return bgImage
    def warpCharImage(self,charImageList, list1=(0.1, 0.3), list2=(0.2, 0.4)):
        def warpImage(im_char, list1, list2):
            (w, h) = im_char.size
            dx = w * random.uniform(list1[0], list1[1])
            dy = h * random.uniform(list2[0], list2[1])
            x1 = int(random.uniform(-dx, dx))
            y1 = int(random.uniform(-dy, dy))
            x2 = int(random.uniform(-dx, dx))
            y2 = int(random.uniform(-dy, dy))
            w2 = w + abs(x1) + abs(x2)
            h2 = h + abs(y1) + abs(y2) 
                # 变量data是一个8元组(x0, y0, x1, y1, x2, y2, x3, y3)，它包括源四边形的左下，左上，右上和右下四个角。
            data = (
                x1,
                y1,
                -x1,
                h2 - y2,
                w2 + x2,
                h2 + y2,
                w2 - x2,
                -y1,
            )
            im_char = im_char.resize((w2, h2))
            im_char_1 = im_char.transform((int(w), int(h)), Image.QUAD, data)
            return im_char_1           
        for i in range(len(charImageList)):
            charImageList[i] = warpImage(charImageList[i],list1,list2)
        return charImageList
    def rotateCharImage(self,charImageList,start=-20, end=20):
        def rotateImage(im_char, start, end):
            im_char = im_char.crop(im_char.getbbox())
            im_char = im_char.rotate(
                random.uniform(start, end), Image.BILINEAR, expand=1)
            return im_char
        for i in range(len(charImageList)):
            charImageList[i] = rotateImage(charImageList[i],start,end)
        return charImageList

    def generateCaptcha(self,label,savePath):
        self.label = label
        bgImage = self.getCaptchaBg()#生成背景
        charImage = CharUtit(
            fontList =  self.getList(self.fontPathDir),
            fontSize = self.fontSize,
            fontRandomRange = self.fontRandomRange,
            fontColor = self.fontColor
        )
        # 生成一组字符图片
        charImageList = []
        for each in (self.label):
            charImageList.append(charImage.generateChar(each))
        # 对图片进行旋转
        charImageList = self.rotateCharImage(charImageList)
        # 对图片进行扭曲
        charImageList = self.warpCharImage(charImageList)
        image = self.pasteCharImageList(bgImage,charImageList)
        # image.show()
        image.save(savePath)
    
        
# # 构造captcha
# captcha = Captcha(
#             width = 150,           # 验证码宽
#             higt = 38,            # 验证按高
#             fontColorRandom = False, # 颜色是否随机
#             fontColor = (0,0,0),       # 指定颜色
#             fontPathDir = os.path.join(dataDir,"font","captcha"),# 字体路径，多种字体直接全部读出来
#             fontSize = 32,        # 字体基准大小
#             fontRandomRange = 0, # 字体随机范围
#             haveBg = False,          # 是否有背景
#             bgPathDri = os.path.join(dataDir,"bg","jd"),       # 有背景的话，背景路径
#             label= "abcd"            # 验证码内容
# )
# captcha.generateCaptcha(os.path.join(dataDir,"captcha","captcha"))
