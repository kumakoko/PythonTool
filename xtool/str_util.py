# -*- coding: utf-8 -*-
# !/usr/bin/env python

import re
import xtool.java_util

# 检测文件名中是否包含中文字符
def has_chinese_character(checked_str):
    '''判断是否包含中文'''
    if not isinstance(checked_str, unicode):
        checked_str = checked_str.decode('utf8')
    if re.search(ur"[\u4e00-\u9fa5]+",checked_str):
        return True
    else:
        return False


# 检测文件名中是否包含空格
def has_space(checked_str):
    '''判断是否包含空格'''
    if re.search(ur"\s",checked_str):
        return True
    else:
        return False

def lowercase_digit_underscode_only(checked_str):
    '''判断字符串中是否只有小写字母,数字,和下划线和圆点'''
    # s='12345abc'
    if re.match(u'^[0-9a-z_.]+$', checked_str):
        return True
    else:
        return False