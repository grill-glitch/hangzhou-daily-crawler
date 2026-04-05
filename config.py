"""
都市快报 RSS 订阅服务
"""

__version__ = "1.0.0"
__author__ = "grill-glitch"

# 数据目录配置
DATA_DIR = "data"
OUTPUT_DIR = "output"

# 确保数据目录存在
import os
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
