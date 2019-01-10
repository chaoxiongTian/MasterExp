### labels生成
```shell
python CaptchaGenerate/labels_generate.py --labels train_5000 --captcha_number 5000 --captcha baidu  
python CaptchaGenerate/labels_generate.py --labels train_5000 --captcha_number 5000 --captcha sina_2014
python CaptchaGenerate/labels_generate.py --labels train_5000 --captcha_number 5000 --captcha recaptcha_2011

```
### 验证码生成
```shell
# 生成训练样本， single_char保存cnn训练时候需要的样本。
python CaptchaGenerate/captcha_generate.py --labels train_5000 --tar train --single_char True --captcha baidu 
python CaptchaGenerate/captcha_generate.py --labels train_5000 --tar train --single_char True --captcha sina_2014
python CaptchaGenerate/captcha_generate.py --labels train_5000 --tar train --single_char True --captcha recaptcha_2011

```