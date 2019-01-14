### labels生成
```shell
python CaptchaGenerate/labels_generate.py --labels train_5000 --captcha_number 5000 --captcha_len 4 --captcha baidu  
python CaptchaGenerate/labels_generate.py --labels train_10000 --captcha_number 10000 --captcha_len 7 --captcha yahoo

python CaptchaGenerate/labels_generate.py --labels train_5000 --captcha_number 5000 --captcha yahoo
python CaptchaGenerate/labels_generate.py --labels train_5000 --captcha_number 5000 --captcha baidu_2013

```
### 验证码生成
```shell
# 生成训练样本， single_char保存cnn训练时候需要的样本。
python CaptchaGenerate/captcha_generate.py --labels train_5000 --tar ceshi --single_char True --captcha baidu 
python CaptchaGenerate/captcha_generate.py --labels train_5000 --tar ceshi --single_char True --captcha sina_2014
python CaptchaGenerate/captcha_generate.py --labels train_5000 --tar ceshi --single_char True --captcha recaptcha_2011
python CaptchaGenerate/captcha_generate.py --labels train_10000 --tar train --single_char True --captcha yahoo

python CaptchaGenerate/captcha_generate.py --labels train_5000 --tar train --single_char True --captcha baidu
python CaptchaGenerate/captcha_generate.py --labels train_5000 --tar train --single_char True --captcha megauploa

python CaptchaGenerate/captcha_generate.py --labels train_5000 --tar ceshi --single_char True --captcha baidu_2013

python CaptchaGenerate/captcha_generate.py --labels test_200 --tar test --captcha yahoo

python CaptchaGenerate/captcha_generate.py --labels test_200 --tar test --captcha baidu_2013

```