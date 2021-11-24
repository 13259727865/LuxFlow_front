import os

import pywinauto
from pywinauto.keyboard import send_keys

os.environ.update({"__COMPAT_LAYER":"RUnAsInvoker"})
import time
from pywinauto import application
from pywinauto import mouse



app = application.Application(backend='uia').start('D:/Program Files(x86)/Luxflows/LuxFlow1028/LuxFlow/LuxFlow.exe')
# app = application.Application(backend='uia')
# app.connect(process=6368,timeout=20)

dlg_list = ['LuxCreo','Dialog','LuxCreoDialog','LuxFlow-defaultDialog','LuxFlow-default']

def print_dlg(n=0):


    try:
        dlg = app[dlg_list[n]]
        print(dlg,dlg_list[n])
        dlg.print_control_identifiers()
        return dlg

    except:
        print("报错了")
        return print_dlg(n+1)
# dlg = print_dlg()
print_dlg()


#上传模型文件
# get_dlg().child_window(title="本地打开", auto_id="FormMain.rightwidget.stackedWidget.FormLoad.pbLocal", control_type="Button").click()
# desktop = pywinauto.Desktop()
# dlg["本地打开"].click()
# openfile = desktop["打开文件"]
# # openfile.print_control_identifiers()
# openfile["Toolbar3"].click()
# send_keys("E:\model\model")
send_keys("{VK_RETURN}")
# openfile["Edit"].click()
# send_keys("heart.stl")
# openfile["Button"].click()
# dlg.print_control_identifiers()
# time.sleep(20)
# update = desktop["upgradeClient"]
# update.print_control_identifiers()
# dlg.get_menu_path()
# dlg.menu_select("帮助->检查更新->软件更新")
# dlg.print_control_identifiers()



# time.sleep(5)
# dlg.child_window(auto_id="FormMain.toolWidgte.pushButtonAutomaticFix", control_type="Button").click()
# dlg.child_window(title="检测", auto_id="FormMain.openGLWidget.FormVDFix.pushButtonCheck", control_type="Button").click()
# time.sleep(10)
# print(1)
# dlg.child_window(title="修复", auto_id="FormMain.openGLWidget.FormVDFix.pushButtonFix", control_type="Button").click()
