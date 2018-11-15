'''
@Description: label对象，可以输出一个labels，构造函数为 lable字符集和labels长度。
@version: 1.0
@Author: MaxCentaur
@Date: 2018-11-14 17:40:00
@LastEditors: MaxCentaur
@LastEditTime: 2018-11-15 11:36:20
'''
import random
class CaptchaLabel(object):
    charList = []
    captchaLen = 0
    def __init__(self,charList,captchaLen):
      self.charList = charList
      self.captchaLen = captchaLen
      self.label = ""
      self.getLabel()
    
    def getLabel(self):
      labelList = []
      for _ in range(self.captchaLen):
        labelList.append(random.choice(self.charList))
      self.label = ''.join(labelList)
      return  self.label
