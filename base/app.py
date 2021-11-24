#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @author:Gemini
# @time:  2021/11/23:17:33
# @email: 13259727865@163.com
import os
import time

os.environ.update({"__COMPAT_LAYER": "RUnAsInvoker"})
from pywinauto import application

page_path = r"D:\Program Files(x86)\Luxflows\LuxFlow1103\dev\LuxFlow\LuxFlow.exe"
app = application.Application(backend='uia').start(page_path)
dlg = app["Dialog"]
time.sleep(10)
dlg.print_control_identifiers()
