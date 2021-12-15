#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @author:Gemini
# @time:  2021/11/9:10:10
# @email: 13259727865@163.com
import time
import os

import pywinauto
from pywinauto.keyboard import send_keys

os.environ.update({"__COMPAT_LAYER": "RUnAsInvoker"})
from pywinauto import application, WindowSpecification, mouse


class Main:
    # 安装路径
    _page_path = ""
    _page_process = 12756


    def __init__(self, dlg: WindowSpecification = None):
        if dlg is None:
            self._app = application.Application(backend='uia')
            if self._page_path != "":
                # self._app.start(self._page_path)
                # time.sleep(15)
                self._app.connect(process=self._page_process)
                self._dlg = self._app["LuxCreo"]

        else:
            self._dlg = dlg

    #打开windows弹框
    def win_desktop(self,win_title,path_bar,path,filename,**kwargs):
        """
        :param title: 弹框title
        :param path_bar: path输入框
        :param path: 文件路径
        :param filename: 文件名
        :param kwargs: 确认按钮child_windows()
        :return:
        """
        self.win = pywinauto.Desktop()
        openconf = self.win[win_title]
        # openconf = self.win_desktop(title="保存配置文件")
        openconf[path_bar].click()
        send_keys(path)
        send_keys("{VK_RETURN}")
        file = openconf.child_window(class_name="Edit")
        file.click()
        send_keys(filename)
        # openconf.child_window(**kwargs).click()
        self.click(openconf["打开"])


    def find(self, index=None, isall=True, text=False, **kwargs):
        """
        :param index: 随机序列名，部分控件容易变化
        :param isall: True and False，判断kwargs是否是想查找的全部，False会对未填字段至 ”“
        :param kwargs: child_window内容
        :return: pywinauto.application控件
        """

        if index:
            title = self._dlg[index]
            if title.exists():
                return self._dlg[index]
            else:
                return False

        else:

            if isall:
                if kwargs.get("title") == None or kwargs.get("title") == "":
                    kwargs["title"] = ""
                if kwargs.get("control_type") == None or kwargs.get("control_type") == "":
                    kwargs["control_type"] = ""
                if kwargs.get("auto_id") == None or kwargs.get("auto_id") == "":
                    kwargs["auto_id"] = ""
                exists = self._dlg.child_window(**kwargs).exists()
                if text == False:
                    if exists:
                        return self._dlg.child_window(**kwargs)
                    else:
                        return False
                elif text == True:
                    if exists:
                        return self._dlg.child_window(**kwargs).texts()[0]
                    else:
                        return False
            else:
                exists = self._dlg.child_window(**kwargs).exists()

                if text == False:
                    if exists:
                        return self._dlg.child_window(**kwargs)
                    else:
                        return False
                elif text == True:
                    if exists:
                        return self._dlg.child_window(**kwargs).texts()[0]
                    else:
                        return False

    #找到控件点击
    def click(self,control=None,button='left',double=False, **kwargs):
        """
        :param control: 控件
        :param button: 按钮**单击鼠标按钮。左键、右键中的一个，“middle”或“x”（默认值为“left”，“move”为特例）
        :param double:双击**是否双击（默认为False）
        :param wheel_dist:滚轮距离**移动鼠标滚轮的距离（默认值：0）
        :param kwargs:
        :return:
        """

        if control:
            control.click_input(button=button,double=double)
        elif kwargs:
            isfind: WindowSpecification = self.find(**kwargs)
            isfind.click_input(button=button,double=double)
            return isfind
        else:
            return "控件不存在或其他异常"

    #判断control是否在outside里面
    def is_in_outside(self,outside=None,control=None):
        outside_left = outside.rectangle().left
        outside_top = outside.rectangle().top
        outside_right = outside.rectangle().right
        outside_bottom = outside.rectangle().bottom
        control_left = control.rectangle().left
        control_top = control.rectangle().top
        control_right = control.rectangle().right
        control_bottom = control.rectangle().bottom

        if control_top >= outside_top and control_bottom <= outside_bottom:
            return True
        elif control_bottom < outside_top:
            mouse.scroll(coords=(outside_left+((outside_right-outside_left)//2), outside_top+((outside_bottom-outside_top)//2)), wheel_dist=2)
            return(self.is_in_outside(outside=outside,control=control))
        elif control_top > outside_bottom:
            mouse.scroll(coords=(3654, 477), wheel_dist=-2)
            return (self.is_in_outside(outside=outside, control=control))
        else:
            return False


    #截图保存
    def capture_image(self,control,path):
        control.capture_as_image().save(path)
        return f"{path}已保存"

    #下拉框选中
    def listbox_choice(self, click_index=1,parent=2,**kwargs):
        """
        :param click_index: 下拉框index
        :param parent:1父级、2层父级 3层父级
        :return:
        """
        application_child = self.click(**kwargs).children()
        if parent == 1 :
            self.click(control=application_child[click_index])
        elif parent == 2:
            control=application_child[0].children()[click_index]
            self.click(control=control)
        elif parent == 3:
            self.click(control=application_child[0].children()[0].children()[click_index])

    #等待出现
    def wait(self, timeout=9999, **kwargs):
        self.find(**kwargs).wait(wait_for="exists enabled visible ready", timeout=timeout)


    #等待消失
    def wait_not(self,timeout=9999,**kwargs):
        self._dlg.print_control_identifiers()
        self.find(**kwargs).wait_not(wait_for_not="exists enabled visible ready",timeout=timeout)
