# MasterExp
Experimental part of the master's paper.
> 该项目为毕业论文的实验部分。

**初步分为三个部分**
```
MasterExp
├── CaptchaGenerate # 对抗验证码生成单元
├── CaptchaNet　# 验证码识别和对抗样本生成单元
├── CaptchaSegment　# 验证码分割单元
├── README.md
├── utils.py
```
## 1: 验证码生成

**labels生成**
```shell
python CaptchaGenerate/labels_generate.py --labels train_5000 --captcha_number 5000 --captcha_len 4 --captcha qq
  
python CaptchaGenerate/labels_generate.py --labels test_200 --captcha_number 200 --captcha_len 4 --captcha qq 
```

**验证码生成**
```shell
python CaptchaGenerate/captcha_generate.py --labels train_5000 --tar train --single_char True --captcha qq

python CaptchaGenerate/captcha_generate.py --labels train_5000 --tar train --captcha qq

python CaptchaGenerate/captcha_generate.py --labels test_200 --tar test --captcha qq
```

## 2: 验证码分割
```
用来把预处理之后的验证码进行分割，分割成识别网络测试集合或分割成识别网络的训练集合。
目录结构：在CaptchaSegment下面有一个data，每个文件夹对应着每个验证码。
python --captcha captcha_name#验证码的名称
       --use cnn # 是生成测试集还是生成训练集
       --tar org # 如果是训练集的话子目录的名称，可能有多组训练集
```

**找字符范围**
```shell
python CaptchaSegment/find_char_range.py --use seg --tar org --captcha qq
```

**用于训练的验证码生成**
```shell
python CaptchaSegment/net_data.py --use cnn --captcha qq
```

**按照预设条件进行的分割**
```shell
python CaptchaSegment/net_data.py --use seg --tar org --cond 256 --captcha qq
```

**找到的一些预设条件**
```shell
'qq': 62,104 # 4
'megaupload': 62,89 #4  68,146
'blizzard': 256 (都是一个字符)
'authorize': 56
'captcha_net': 256 (都是一个字符)
'nih': 256 (都是一个字符)
'reddit': 37
'digg': 256
'baidu': 60,105,144  # 4   45,105
'sina_2014': 47,80,  # 5
'baidu_2013' 44 # 4
'amazon': generate_amazon,  # 6
'yahoo': generate_yahoo,  # 7
'recaptcha_2011': 34,61,83,109,118,153  # 8
```
## 3: 验证码识别
```
python CaptchaNet/main.py --captcha mnist # 对应验证码的种类，后面用于模型文件夹等。 
--train_num 1000 # 若不赋值，则对应data_sets/captcha/train 中图片的数量
--test_num 100 # 若不赋值，则对应data_sets/captcha/test 中图片的数量
--epoch # 迭代次数
--net #选的网络
--batch_size # 批大小默认64
--moad train # 默认为train 
--real_captcha_len # 4 对分割之后的验证码做预估的时候正式验证码的字符长度
``` 

**训练**
```shell
python CaptchaNet/main.py --net cnn --epoch 200 --real_captcha_len 4 --captcha qq
```

**测试**
```shell
python CaptchaNet/main.py --load_ckpt best_acc.tar --mode test --net cnn --real_captcha_len 4 --captcha qq 
```

**对抗样本生成**
