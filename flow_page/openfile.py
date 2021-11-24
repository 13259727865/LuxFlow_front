#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @author:Gemini
# @time:  2021/11/23:18:29
# @email: 13259727865@163.com
import pywinauto
from pywinauto.keyboard import send_keys

from base.main import Main



class Open(Main):
    # 本地打开
    def openfile(self, path, model):
        """
        :param path: 模型路径
        :param model: 模型名称，多模型例 '"格子收纳盒.stl""heart.stl"'
        :return: 按钮文本
        """
        openfile_text = self.find(title="本地打开", auto_id="FormMain.rightwidget.stackedWidget.FormLoad.pbLocal",
                                  control_type="Button").texts()[0]
        self.click(title="本地打开", auto_id="FormMain.rightwidget.stackedWidget.FormLoad.pbLocal", control_type="Button")
        win = pywinauto.Desktop()
        # win["打开文件"].print_control_identifiers()
        dizhi = win["打开文件"]["Toolbar3"]
        dizhi.click()
        send_keys(path)
        send_keys("{VK_RETURN}")
        filename = win["打开文件"].child_window(class_name="Edit")
        filename.click()
        send_keys(model)
        win["打开文件"].child_window(title="打开(&O)", class_name="Button").click()

        return openfile_text