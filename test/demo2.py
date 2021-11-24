#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @author:Gemini
# @time:  2021/11/5:10:19
# @email: 13259727865@163.com

import time

import pywinauto
import os
os.environ.update({"__COMPAT_LAYER":"RUnAsInvoker"})
from pywinauto import application

# app = application.Application(backend='uia').start('D:/Program Files(x86)/Luxflows/LuxFlow1028/LuxFlow/LuxFlow.exe')
app = application.Application(backend='uia')
app.connect(process=24232,timeout=20)
print(121)
time.sleep(3)
dlg = app["Dialog"]
print(type(dlg))
# dlg.print_control_identifiers()
# dlg.MenuSelect("帮助->检查更新->软件更新")
# print(dir(dlg.wrapper_object()))
# #帮助菜单
menu = dlg["['Menu2']"]
# help = menu.child_window(title="帮助", control_type="MenuItem")
# help.click_input()
# update = menu.child_window(title="检查更新", control_type="MenuItem")
# update.click_input()
# canshu_update = menu.child_window(title="打印参数更新", auto_id="FormMain.widgetTitle.wMenuBar.actionMaterial_parameter_package_update", control_type="MenuItem")
# canshu_update.click_input()
set = menu.child_window(title="设置", control_type="MenuItem")
print(set.get_properties())

set.click_input()
menu.child_window(title="设置", auto_id="FormMain.widgetTitle.wMenuBar.actionSetting", control_type="MenuItem").click_input()

dlg.print_control_identifiers()
