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
def fun2(a,b,c):
    print(a,b,c)


def atest(**kwargs):
    fun2()



a = {"a":1,"b":2,"c":3}
atest(**a)


