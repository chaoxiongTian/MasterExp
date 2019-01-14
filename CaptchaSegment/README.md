net_data.py

用来把预处理之后的验证码进行分割，分割成识别网络测试集合或分割成识别网络的训练集合。
目录结构：在CaptchaSegment下面有一个data，每个文件夹对应着每个验证码。
python --captcha captcha_name#验证码的名称
       --use cnn # 是生成测试集还是生成训练集
       --tar org # 如果是训练集的话子目录的名称，可能有多组训练集
```
生成cnn训练样本
python CaptchaSegment/net_data.py --use cnn --captcha qq 
按照cfs分割找到字符的宽度
python CaptchaSegment/find_char_range.py --use seg --tar org --captcha blizzard
按照预设条件分割验证码
python CaptchaSegment/net_data.py --use seg --tar org --cond 256 --captcha blizzard 
....
# 需要保证对应目录下面存在labels。
/home/tianchaoxiong/LinuxData/code/pythonpro/MasterExp/CaptchaSegment/data/qq/seg/org/images
/home/tianchaoxiong/LinuxData/code/pythonpro/MasterExp/CaptchaSegment/data/qq/seg/org/test_sets
/home/tianchaoxiong/LinuxData/code/pythonpro/MasterExp/CaptchaSegment/data/qq/seg/qq_test_200_labels.txt

/home/tianchaoxiong/LinuxData/code/pythonpro/MasterExp/CaptchaSegment/data/qq/cnn/images
/home/tianchaoxiong/LinuxData/code/pythonpro/MasterExp/CaptchaSegment/data/qq/cnn/train_sets
/home/tianchaoxiong/LinuxData/code/pythonpro/MasterExp/CaptchaSegment/data/qq/cnn/qq_train_5000_labels.txt
```
```
qq: 62,104
megaupload: 62,89   68,146
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