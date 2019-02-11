# -*- coding: utf-8 -*-
# @Time    : 18-12-10 上午11:25
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : out_utils.py
# @Software: PyCharm

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from utils import *

data_folder = os.path.join(os.path.split(os.path.abspath(os.sys.argv[0]))[0], "data")
