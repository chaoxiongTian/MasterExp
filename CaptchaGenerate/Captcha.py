'''
@Description: 
@version: 
@Author: MaxCentaur
@Date: 2018-11-28 17:24:10
@LastEditors: MaxCentaur
@LastEditTime: 2018-11-28 17:24:46
'''
'''
@Description: 工具类
@version: 1.0
@Author: MaxCentaur
@Date: 2018-11-14 22:59:38
@LastEditors: MaxCentaur
@LastEditTime: 2018-11-28 17:34:48
'''
import os
import random
from PIL import Image, ImageDraw, ImageFont
dataDir = os.path.join(os.path.split(os.path.abspath(os.sys.argv[0]))[0],"data")
'''
@msg: 字符类
'''
class CharUtit(object):
    '''
    @msg: 构造函数
    '''
    def __init__(self,
        fontList,        # 字体路径列表
        fontSize,        # 字体大小
        fontRandomRange, # 字体随机的区间
        fontColor        # 字体的颜色 （此处 因为多数都进行二值化，所以不存在随机颜色）
    ):
        self.fontList = fontList
        self.fontSize = fontSize
        self.fontColor = fontColor
        self.fontRandomRange = fontRandomRange
    '''
    @msg: 字符生成函数
    '''
    def generateChar(self,char):
        fontPath = random.choice(self.fontList) # 选字体
        fontSize = random.randint(self.fontSize-self.fontRandomRange,self.fontSize+self.fontRandomRange) # 选大小
        # 构造字体对象
        font = ImageFont.truetype(fontPath,fontSize)
        # 构造Image对象
        charImage = Image.new('RGBA',(font.getsize(char)),(255,255,255))
        charDraw = ImageDraw.Draw(charImage)
        # TODO: 这里的Draw.text存在问题，需要修改。
        charDraw.text((0,-5), char, (0,0,0), font=font)
        del charDraw
        # saveDir = os.path.join(dataDir,"captcha","ceshi.jpg")
        # charImage.save(saveDir)
        # charImage.show()
        return charImage

'''
@msg: 验证码类
'''
class Captcha(object):
    '''
    @msg: 验证码的构造函数
    '''
    def __init__(self,
            width,           # 验证码宽
            higt,            # 验证按高
            haveBg,          # 是否有背景
            bgPathDri,       # 有背景的话，背景路径
            fontPathDir,     # 字体路径，多种字体直接全部读出来
            fontColor,       # 指定颜色(处理之后都需要二值化，所以可不用随机颜色)
            fontSize,        # 字体基准大小
            fontRandomRange, # 字体随机范围
            startX = 0,      # 第一个字符的开始位置
            step = 10        # 每个字符之间的距离
            ):
        self.width = width
        self.higt = higt
        self.haveBg = haveBg
        self.bgPathDri =bgPathDri
        self.startX =startX
        self.step = step
        self.fontPathDir = fontPathDir
        self.fontColor = fontColor
        self.fontSize = fontSize
        self.fontRandomRange = fontRandomRange
        # 打印类信息
        print(self)
    '''
    @msg: 定制打印
    '''
    def __str__(self):
        return ("Captcha info\n-----------\n(width: %s)" % self.width
                  +"\n(higt: %s)" % self.higt
                  +'\n(haveBg: %s)' % self.haveBg
                  +'\n(bgPathDri: %s)' % self.bgPathDri
                  +'\n(startX: %s)' % self.startX
                  +'\n(step: %s)' % self.step
                  +'\n\nchar info\n-----------\n(fontColor:'+str(self.fontColor)+")"
                  +'\n(fontPathDir: %s)' % self.fontPathDir
                  +'\n(fontSize: %s)' % self.fontSize
                  +'\n(fontRandomRange: %s)' % self.fontRandomRange+"\n-----------\n")
    
    '''
    @msg: 返回dir文件夹下所有文件的绝对路径，若使用 os.path.abspath会出现错误（abspath使用的是getwd获取运行路径）。
    '''
    def getList(self,dir):
            def f(x):
                return os.path.join(dir,x)
            return list(map(f,os.listdir(dir)))
    
    '''
    @msg: 根据初始化参数生成背景Image
    '''
    def getCaptchaBg(self):
        if(self.haveBg):
            # 有背景的话，随机取出一个背景。
            bgImagePath = random.choice(self.getList(self.bgPathDri))
            bgImage = Image.open(bgImagePath)
        else:
            # 生成一个shitang新的白底背景 
            bgImage = Image.new('RGBA', (self.width,  self.higt), (255,255,255))
        return bgImage
    
    '''
    @msg: 对char的Image对象进行扭曲
    '''
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
    '''
    @msg: 对char的Image对象进行旋转
    '''
    def rotateCharImage(self,charImageList,start=-20, end=20):
        def rotateImage(im_char, start, end):
            im_char = im_char.crop(im_char.getbbox())
            im_char = im_char.rotate(
                random.uniform(start, end), Image.BILINEAR, expand=1)
            return im_char
        for i in range(len(charImageList)):
            charImageList[i] = rotateImage(charImageList[i],start,end)
        return charImageList

    '''
    @msg: 添加干扰点
    '''
    def addNoise(self,image,noiseNumber=100,width=2,noiseColor=(0,0,0)):
        draw = ImageDraw.Draw(image)
        w, h = image.size
        while noiseNumber:
            x1 = random.randint(0, w)
            y1 = random.randint(0, h)
            draw.ellipse(((x1, y1), (x1 + width, y1 + width)), fill=noiseColor)
            noiseNumber -= 1
        del draw
        return image  

    '''
    @msg: 根据labels生成 char的Image对象列表
    '''
    def generateCharImageList(self,label):
        charImage = CharUtit(
            fontList =  self.getList(self.fontPathDir),
            fontSize = self.fontSize,
            fontRandomRange = self.fontRandomRange,
            fontColor = self.fontColor
        )
        # 生成一组字符图片
        charImageList = []
        for each in (label):
            charImageList.append(charImage.generateChar(each))
        return charImageList
    
    '''
    @msg: 把一组char的Image对象粘贴到背景Image上面
    '''
    def pasteCharImageList(self,bgImage,charImageList):
        # TODO：目的（把char的Image对象粘贴到对象背景上粘连上去）
        # 1. 预估charImageList需要的长度，若背景image对象不够长，调整背景image长度
        
        '''
        @msg: 预估函数
        '''
        def preCalcBgWeidth(start,step,charImageList):
            preCalc = start
            for i in range(len(charImageList)-1):
                eachW = charImageList[i].size[0]
                preCalc = preCalc+eachW+self.step
            return preCalc+charImageList[-1].size[0]
        
        preCalc = preCalcBgWeidth(self.startX,self.step,charImageList)
        
        if(preCalc>self.width): 
            # 重新调整背景的大小
            bgImage = bgImage.resize((preCalc,self.higt),Image.ANTIALIAS)
        # 2. 开始粘贴
        offsetX = self.startX;offsetY = 0
        for each in charImageList:
            charW,charH = each.size;mask = each
            bgImage.paste(each,(offsetX,int((self.higt-charH)/2)),mask)
            offsetX = offsetX+charW+self.step
        bgImage = bgImage.resize((self.width,self.higt),Image.ANTIALIAS)
        return bgImage
    
    '''
    @msg: 合成captcha
    '''
    def generateCaptcha(self,label,savePath):
        bgImage = self.getCaptchaBg()#生成背景
        charImageList = self.generateCharImageList(label)
        # 对图片进行旋转
        charImageList = self.rotateCharImage(charImageList)
        # 对图片进行扭曲
        # charImageList = self.warpCharImage(charImageList)
        image = self.pasteCharImageList(bgImage,charImageList)
        # image.show()
        image = self.addNoise(image)
        image.save(savePath)
    