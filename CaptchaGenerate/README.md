### labels生成
```shell
python CaptchaGenerate/labels_generate.py --captcha megaupload --labels train_5000 --captcha_len 4 --captcha_number 5000
```
### 验证码生成
```shell
python CaptchaGenerate/captcha_generate.py --captcha megaupload --labels test_200 --captcha_len 4 --tar test
```