import os
class Utils(object):
    def sayHi(self,content):
    
        print(content)
    
    def makeDir(self,path):
        if(not os.path.exists(path)):
            os.makedirs(path)
            print("make labels save dir")
        print("labels save dir is exist")
    
    def saveStringFile(self,filePath,fileContent):
        f = open(filePath,'w')
        f.write(fileContent)
        f.close
