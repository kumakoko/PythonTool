# -*- coding: utf-8 -*-
# !/usr/bin/env python

import os
import os.path
import re
import sys
import msvcrt
import xtool.file_util as xfileu

# root_dir = ["D:/work/MiJiGen/Assets/scenes"]
root_dir = []
current_work_dir = ""


# 从文件中读取根目录列表
def read_root_directory(work_dir):
    global root_dir
    f = open(work_dir + "/root_dir.txt")
    root_dir = f.readlines()


def check(rd):
    result_file_path = current_work_dir + "/check_result.txt"
    print result_file_path
    result_file = open(result_file_path, 'w')

    '''
    os.walk方法三个参数：分别返回:
    1 父目录
    2 所有文件夹名字（不含路径）
    3 所有文件名字
    '''
    for d in rd:
        print d
        for parent, dirnames, filenames in os.walk(d):
            dir_len = len(d)  # 根目录字符串的长度

            for filename in filenames:  # 输出文件信息
                full_path = os.path.join(parent, filename)
                sub_path = full_path[dir_len:]  # 取出去掉了根目录的长度的子串

                m = re.match(r"^[a-z0-9\.\\/_]+$", sub_path)

                if m:  # 完全匹配，跳过
                    pass
                else:
                    result_file.write(full_path)
                    result_file.write('\n')
                # else:   # 带有非数字小写字母下划线的

    result_file.close()  # 关闭
    print u"检查完成，不合法的文件目录名都记录在check_result.txt文件中"


if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf8')
    current_work_dir = xfileu.cur_script_dir()  # 读取到当前的工作目录
    print current_work_dir
    read_root_directory(current_work_dir)  # 读取到要处理的根目录
    check(root_dir)
    print u"按任意键退出"
    # print ord(msvcrt.getch())
    msvcrt.getch()
