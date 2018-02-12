# -*- coding: utf-8 -*-
# !/usr/bin/env python

# 程序主入口
import xtool.file_util as xfileu
import os

# os.path.walk(path) 遍历path，返回一个三元组（dirpath, dirnames, filenames).
# dirpath表示遍历到的路径, dirnames表示该路径下的子目录名，是一个列表,
# filesnames表示该路径下的文件名，也是一个列表. 例如: 当遍历到c:\windows时，
# dirpath="c:\windows",
# dirnames是这个路径下所有子目录名的列表，
# dirnames是这个路径下所有文件名的列表

def walk_all_files(root_path):
    for (dir_path, dir_names, file_names) in os.walk(root_path):
        print("Dir path is "+dir_path)
        for dn in dir_names:
            print("    Dir name is "+dn+" ========>>>")
            walk_all_files(dir_path+"/"+dn)
        for fn in file_names:
            print("    File name is "+fn)

# 测试相关函数的代码
if __name__ == "__main__":
    # cur_dir = xfileu.cur_script_dir()
    # print("Current directory is "+cur_dir)
    # walk_all_files("F:/Github/PythonTool/trunk")
    src = "F:/KumaGL"
    dst = "F:/Github/KumaGL/trunk"
    skip_dirs = ["Debug", "Release", "bin", "Help", "ipch", "TankForce", "TabSpaceShell", "Tetris", ".svn", "third_lib"]
    skip_exts = [".sdf", ".zip", "ilk", ".pdb", ".exe"]
    xfileu.copy_tree_filter(src, dst, skip_dirs, skip_exts)