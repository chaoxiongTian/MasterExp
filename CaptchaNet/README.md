mnist 
train
```
python CaptchaNet/main.py --captcha_len 1 --model_name mnist --train_num 1000 --test_num 100
```
test
```
python CaptchaNet/main.py --captcha_len 1 --model_name mnist --train_num 1000 --test_num 100 --mode test --load_ckpt best_acc.tar --net cnn
```

auth
train
```
python CaptchaNet/main.py --captcha_len 5 --model_name auth --train_num 2000 --test_num 200 --net cnn_256 --epoch 50 --net cnn_256--net cnn_256
```
test
```
python CaptchaNet/main.py --captcha_len 5 --model_name auth --train_num 2000 --test_num 200 --mode test --load_ckpt best_acc.tar --net cnn_256
```
