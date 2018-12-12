# MasterExp
Experimental part of the master's paper.
> 该项目为毕业论文的实验部分。

**初步分为四个部分**
```
MasterExp
├── AdversarialCaptcha # 对抗样本生成部分
├── CaptchaGenerate # 对抗验证码生成部分
│   ├── captcha_generate.py # 验证码生成函数
│   ├── captcha.py #　验证码类
│   ├── captcha_utils.py　# 生成工具
│   ├── data　# 数据存储位置
│   │   ├── bg　# 背景
│   │   ├── captcha　# 生成好fdasfsf
│   │   ├── font　# 字体文件夹
│   │   └── labels　# 标签文件夹
│   ├── generate_unit.py　# 生成单元
│   ├── label.py　# 标签类
│   ├── labels_generate.py　# 标签生成函数
│   ├── options.py　# 参数类
│   ├── out_utils.py　# 调用外部类
├── CaptchaSegment　# 验证码分割单元
│   ├── data
│   ├── image_segment.py　# 分割函数
│   ├── net_data.py　#　生成训练数据
│   ├── out_utils.py　# 调用外部功能类
│   ├── segment_cfs.py　# 连通域分割算法
│   ├── segment_drop.py　# 滴水分割算法
│   ├── segment_projection.py　# 投影分割算法
│   ├── segment_synthesis.py　# 连通域和投影滴水的结合
│   └── segment_utils.py　# 功能单元
├── IdentifiNetwork
├── README.md
├── utils.py
└── 周报.txt

```


