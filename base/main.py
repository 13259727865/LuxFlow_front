#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @author:Gemini
# @time:  2021/11/9:10:10
# @email: 13259727865@163.com
import time
import os

import pywinauto

os.environ.update({"__COMPAT_LAYER": "RUnAsInvoker"})
from pywinauto import application, WindowSpecification


class Main:
    # 安装路径
    _page_path = ""
    _page_process = 5220


    def __init__(self, dlg: WindowSpecification = None):
        if dlg is None:
            self._app = application.Application(backend='uia')
            if self._page_path != "":
                # self._app.start(self._page_path)
                # time.sleep(15)
                self._app.connect(process=self._page_process)
                self._dlg = self._app["Dialog"]

        else:
            self._dlg = dlg

    #打开windows弹框
    def win_desktop(self,title):
        """
        :param title: 弹框名
        :return:
        """
        self.win = pywinauto.Desktop()
        return self.win[title]



    def find(self, index=None, isall=True, text=False, **kwargs):
        """
        :param index: 随机序列名，部分控件容易变化
        :param isall: True and False，判断kwargs是否是想查找的全部，False会对未填字段至 ”“
        :param kwargs: child_window内容
        :return: pywinauto.application控件
        """
        if index:
            if self._dlg.exists():
                return self._dlg[index]
            else:
                return False
        else:
            if isall:
                if kwargs.get("title") == None or kwargs.get("auto_id") == "":
                    kwargs["title"] = ""
                if kwargs.get("control_type") == None or kwargs.get("auto_id") == "":
                    kwargs["control_type"] = ""
                if kwargs.get("auto_id") == None or kwargs.get("auto_id") == "":
                    kwargs["auto_id"] = ""
                if text == False:
                    if self._dlg.child_window(**kwargs).exists():
                        return self._dlg.child_window(**kwargs)
                    else:
                        return False
                elif text == True:
                    if self._dlg.exists():
                        return self._dlg.child_window(**kwargs).texts()[0]
                    else:
                        return False
            else:
                if text == False:
                    if self._dlg.exists():
                        return self._dlg.child_window(**kwargs)
                    else:
                        return False
                elif text == True:
                    if self._dlg.exists():
                        return self._dlg.child_window(**kwargs).texts()[0]
                    else:
                        return False

    #找到
    def click(self, index=None, isall=True, **kwargs):
        if self.find(index, isall, **kwargs):
            self.find(index, isall, **kwargs).click_input()
        else:
            return "控件不存在或其他异常"

    def is_english(self):
        # dlg2 = self._app["SettingGroupBox"]
        dlg2 = self._app["LuxCreo"]
        return dlg2["SettingGroupBox"].children()
