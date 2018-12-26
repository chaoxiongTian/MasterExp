train:
python IdentifiNetwork/main.py --mode train --model_name d_mnist --captcha Ture --captcha_len 4

test:
python IdentifiNetwork/main.py --mode test --model_name jd --load_ckpt best_acc_0.972.tar --captcha Ture --captcha_len 4

jd: captcha accuracy: 0.9100