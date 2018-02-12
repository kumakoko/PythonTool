#-*- coding: utf-8 -*-
#!/usr/bin/env python

import platform

def is_windows_os():
    return 'Windows' in platform.system()

def is_linux_os():
    return 'Linux' in platform.system()