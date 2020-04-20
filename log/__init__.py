# -*- coding: utf-8 -*-
"""
 @Time    : 20/4/20 11:47
 @Author  : CyanZoy
 @File    : __init__.py.py
 @Software: PyCharm
 @Describe: 
 """
import logging

for_str = "\033[0;36m%(asctime)s [%(name)s][%(levelname)s] %(message)s\033[0m"

logging.basicConfig(level=logging.INFO, format=for_str)
logger = logging.getLogger(__name__)
