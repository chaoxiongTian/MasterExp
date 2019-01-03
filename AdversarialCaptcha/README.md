train:
```shell
python AdversarialCaptcha/main.py --mode train --model_name d_mnist
```


test:
```shell
python AdversarialCaptcha/main.py --mode test --model_name jd --load_ckpt best_acc.tar
```


generate
```shell
python AdversarialCaptcha/main.py --mode generate --iteration 1 --epsilon 0.2 --model_name d_mnist --load_ckpt best_acc.tar

```
