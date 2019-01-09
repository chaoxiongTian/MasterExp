net_data.py

用来把预处理之后的验证码进行分割，分割成识别网络测试集合或分割成识别网络的训练集合。
目录结构：在CaptchaSegment下面有一个data，每个文件夹对应着每个验证码。
python --captcha captcha_name#验证码的名称
       --use cnn # 是生成测试集还是生成训练集
       --tar org # 如果是训练集的话子目录的名称，可能有多组训练集
```
python CaptchaSegment/net_data.py --captcha qq --use cnn
python CaptchaSegment/net_data.py --captcha qq --use seg --tar org --cond 62,105
....
# 需要保证对应目录下面存在labels。
/home/tianchaoxiong/LinuxData/code/pythonpro/MasterExp/CaptchaSegment/data/qq/seg/org/images
/home/tianchaoxiong/LinuxData/code/pythonpro/MasterExp/CaptchaSegment/data/qq/seg/org/test_sets
/home/tianchaoxiong/LinuxData/code/pythonpro/MasterExp/CaptchaSegment/data/qq/seg/qq_test_200_labels.txt

/home/tianchaoxiong/LinuxData/code/pythonpro/MasterExp/CaptchaSegment/data/qq/cnn/images
/home/tianchaoxiong/LinuxData/code/pythonpro/MasterExp/CaptchaSegment/data/qq/cnn/train_sets
/home/tianchaoxiong/LinuxData/code/pythonpro/MasterExp/CaptchaSegment/data/qq/cnn/qq_train_5000_labels.txt

```