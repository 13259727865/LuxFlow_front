#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @author:Gemini
# @time:  2021/10/28:17:27
# @email: 13259727865@163.com
# from pywinauto import application
# app = application.Application()
# app.start("Notepad.exe")
#
# app.UntitledNotepad.draw_outline()
# # app.UntitledNotepad.menu_select("编辑 -> 替换(&R)...")
# app.替换.print_control_identifiers()
# app.替换.取消.click()
# app.UntitledNotepad.编辑.type_keys("Hi from Python interactive prompt %s" % str(dir()), with_spaces = True)
# app.UntitledNotepad.menu_select("File -> Exit")
# app.Notepad.DontSave.click()

import datetime
from datetime import datetime
import time
#
# a = datetime.now().replace(microsecond=0)
# for i in range(3):
#     time.sleep(2)
# b = datetime.now().replace( microsecond=0)
# print(b - a)


def bubbleSort(arr):
    # for i in range(len(arr) - 1):
    for j in range(len(arr)-1):
        if arr[j] > arr[j + 1]:
            arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr[-1]


print(bubbleSort([4,5,9,7,8,12,2]))