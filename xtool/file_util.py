# -*- coding: utf-8 -*-
# !/usr/bin/env python

import os
import os.path
import sys
import shutil
import exception_util as eutil


def copy_tree(src, dst, symlinks=False):
    # 列出源目录下的所有子目录和文件
    names = os.listdir(src)

    # 如果目标目录不存在的话，创建之
    if not os.path.isdir(dst):  
        os.makedirs(dst)  
          
    errors = []
    for name in names:
        # 遍历每一个目标子目录和目标文件，对应生成目标子目录或者目标文件
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:  
            if symlinks and os.path.islink(srcname):  
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            # 如果是源子目录
            elif os.path.isdir(srcname):
                copy_tree(srcname, dstname, symlinks)  
            else:
                if os.path.isdir(dstname):  
                    os.rmdir(dstname)  
                elif os.path.isfile(dstname):  
                    os.remove(dstname)  
                shutil.copy2(srcname, dstname)  
            # XXX What about devices, sockets etc.?  
        except (IOError, os.error) as why:  
            errors.append((srcname, dstname, str(why)))  
        # catch the Error from the recursive copytree so that we can  
        # continue with other files  
        except OSError as err:  
            errors.extend(err.args[0])  
    try:  
        shutil.copystat(src, dst)
    except WindowsError:  
        # can't copy file access times on Windows  
        pass  
    except OSError as why:  
        errors.extend((src, dst, str(why)))
    if errors:  
        raise Error(errors)


def copy_tree_filter(src, dst, skip_dirs, skip_file_exts, symlinks=False):
    # 列出源目录下的所有子目录和文件
    names = os.listdir(src)

    # 如果目标目录不存在的话，创建之
    if not os.path.isdir(dst):
        os.makedirs(dst)

    errors = []
    for name in names:

        # 遍历每一个目标子目录和目标文件，对应生成目标子目录或者目标文件
        srcname = os.path.join(src, name)

        # 判断源文件，如果是后缀名过滤列表中的就跳过
        if os.path.isfile(srcname):
            file_ext = os.path.splitext(srcname)[1]
            if file_ext in skip_file_exts:
                print("=====> Skip file " + srcname)
                continue

        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            # 如果是源子目录
            elif os.path.isdir(srcname):
                if name in skip_dirs:
                    print("=====> Skip directory " + name)
                    continue
                else:
                    copy_tree_filter(srcname, dstname, skip_dirs, skip_file_exts, symlinks)
            else:
                if os.path.isdir(dstname):
                    os.rmdir(dstname)
                elif os.path.isfile(dstname):
                    os.remove(dstname)
                shutil.copy2(srcname, dstname)
                print("=====> Copy FILE " + srcname)

        except (IOError, os.error) as why:
            errors.append((srcname, dstname, str(why)))
        except OSError as err:
            errors.extend(err.args[0])
    try:
        shutil.copystat(src, dst)
    except WindowsError:
        # can't copy file access times on Windows
        pass
    except OSError as why:
        errors.extend((src, dst, str(why)))
    if errors:
        raise Error(errors)

# 拷贝某个文件src_file到指定的目录dst_dir，加上打印信息，加上异常判断
def copy_file_to_directory(src_file, dst_dir):
    try:
        shutil.copy(src_file, dst_dir)
        print(u"拷贝文件 %s \n -----> \n 到目录%s\n" % (src_file, dst_dir))
    except:
        eutil.print_exception_info(u"拷贝文件%s到指定的目录%s时发生异常"%(src_file, dst_dir) )

# 创建一个目录，加上判断检查
def make_directory(dst_dir):
    if not os.access(dst_dir, os.F_OK):
        os.makedirs(dst_dir)

# 获取当前脚本文件的当前路径
def cur_script_dir():
    # 获取脚本路径
    """

    :rtype : 返回获取到的路径
    """
    script_path = sys.path[0]
    # 判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的
    # 是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(script_path):
        return script_path
    elif os.path.isfile(script_path):
        return os.path.dirname(script_path)