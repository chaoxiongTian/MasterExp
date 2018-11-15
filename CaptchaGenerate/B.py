# import A
# a = A.A()
# a.sayHello("hello B")
# from A import A
# a = A()
# a.sayHello("hello me")
# import CaptchaGeneateUtil
# a = CaptchaGeneateUtil.CaptchaGenerateUtil()
# a.sayHi("hi a")

# from CaptchaGeneateUtil import CaptchaGenerateUtil
# a = CaptchaGenerateUtil()
# a.sayHi("hi second")
import os
import sys
# sys.path.append(os.path.abspath(os.getcwd()))
# from Utils import Utils
# a = Utils();
# a.sayHi("hi outside")
print(os.path.dirname(__file__))
print(os.pardir)
parentUrl = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
print(parentUrl)

    