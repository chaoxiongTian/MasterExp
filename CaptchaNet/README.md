mnist 
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
train
```
python CaptchaNet/main.py --net cnn --epoch 200 --real_captcha_len 6 --captcha blizzard
python CaptchaNet/main.py --net cnn --epoch 200 --real_captcha_len 4 --captcha authorize
python CaptchaNet/main.py --net cnn --epoch 200 --real_captcha_len 5 --captcha captcha_net
python CaptchaNet/main.py --net cnn --epoch 200 --real_captcha_len 5 --captcha nih


```
test
```
python CaptchaNet/main.py --captcha qq --real_captcha_len 4 --mode test --load_ckpt best_acc.tar --net cnn
```
