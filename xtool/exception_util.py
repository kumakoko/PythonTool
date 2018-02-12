# -*- coding: utf-8 -*-
# !/usr/bin/env python

import sys


# 打印异常信息
# error_desc_title是异常的描述标题
def print_exception_info(error_desc_title):
    except_info = sys.exc_info()
    print(error_desc_title)
    print(str(except_info[0]))
    print(str(except_info[1]))
    print(str(except_info[2]))