# -*- coding: utf-8 -*-
# !/usr/bin/env python

import os


# 检查Java环境是否安装,有安装返回True，未安装返回False
def check_java_environment():
    r = os.system("java -version")
    if r != 0:
        return True
    else:
        return False