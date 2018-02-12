# -*- coding: utf-8 -*-
# !/usr/bin/env python

# 和文本控制台相关的一些工具函数

import time
import sys

# percent 当前进度的百分比，取值范围是[0,100]
# bar_length 进度条的长度
# sleep_time 间隔多少秒刷新一次
def progress(percent,bar_length,sleep_time):
    hashes = '#' * int(percent/100.0 * bar_length)
    spaces = ' ' * (bar_length - len(hashes))
    sys.stdout.write(u"\r当前进度: [%s] %d%%"%(hashes + spaces, percent))
    sys.stdout.flush()
    time.sleep(sleep_time)

# 测试相关函数的代码
if __name__ == "__main__":
    for percent in xrange(0, 100):
        progress(percent,10,0.1)