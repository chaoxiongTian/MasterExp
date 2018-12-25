train:
python IdentifiNetwork/main.py --mode train --model_name d_mnist

test:
python IdentifiNetwork/main.py --mode test --model_name d_mnist --load_ckpt best_acc.tar