### labels生成
```shell
python CaptchaGenerate/labels_generate.py --captcha megaupload --labels train_5000 --captcha_len 4 --captcha_number 5000
```
### 验证码生成
```shell
# 生成训练样本， single_char保存cnn训练时候需要的样本。
python CaptchaGenerate/captcha_generate.py --captcha megaupload --labels train_5000 --captcha_len 4 --tar test --single_char True
```