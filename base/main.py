#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @author:Gemini
# @time:  2021/11/9:10:10
# @email: 13259727865@163.com
import time
import os

import allure

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = curPath[:curPath.find("LuxFlow_front\\")+len("LuxFlow_front\\")]  # 获取LuxFlow_front，也就是项目的根路径
from datetime import datetime
import pywinauto
from pywinauto.keyboard import send_keys
from common.io import JsonIO
from common.logger import LogRoot
os.environ.update({"__COMPAT_LAYER": "RUnAsInvoker"})
from pywinauto import application, WindowSpecification, mouse


class Main:
    # 安装路径
    _jsonio = JsonIO().read_json()
    _page_path = ""
    _page_process = _jsonio["process"]


    def __init__(self, dlg: WindowSpecification = None):
        if dlg is None:
            self._app = application.Application(backend='uia')
            if self._page_path != "":
                if self._jsonio["action"]=="start":
                    self._app.start(self._page_path)
                    time.sleep(10)
                elif self._jsonio["action"]=="connect":
                    self._app.connect(process=self._page_process)
                self._dlg = self._app["Dialog"]

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

    #输入框填写信息
    def insert(self,value,**kwargs):
        self.click(**kwargs)
        send_keys("^a")
        send_keys(str(value))

    #判断control是否在outside里面
    def is_in_outside(self,outside=None,control=None):
        """
        :param outside: 外层控件
        :param control: 里层空间
        :param control_isappear: 里层控件是否一直可以获取到
        :return:
        """
        rect = outside.rectangle()
        outside_left = rect.left
        outside_top = rect.top
        outside_right = rect.right
        outside_bottom = rect.bottom
        control_left = rect.left
        control_top = rect.top
        control_right = rect.right
        control_bottom = rect.bottom
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

    #滚动控件直到要选的控件出现
    def is_isappear_outside(self,choice_index,outside):
        outside_list = outside.children()
        page = choice_index//(len(outside_list)//2)+1
        if page <= 2 :
            self.click(control=outside_list[choice_index])
        elif page > 2:
            rect = outside.rectangle()
            outside_left = rect.left
            outside_top = rect.top
            outside_right = rect.right
            outside_bottom = rect.bottom
            mouse.scroll(coords=(outside_left + ((outside_right - outside_left) // 2),
                                 outside_top + ((outside_bottom - outside_top) // 2)), wheel_dist=2-page)
            self.click(control=outside_list[choice_index%(len(outside_list)//2)+3])




    #截图保存
    def capture_image(self,img_doc,control=None):
        """
        :param img_doc: 图片说明
        :param control: 只对控件截图
        :return:
        """
        file_name = rootPath + r"\picture\{}_{}.png".format(img_doc,datetime.strftime(datetime.now(), "%Y%m%d%H%M%S"))
        print(file_name)
        if control is None:
            self._dlg.capture_as_image().save(file_name)
        elif control:
            control.capture_as_image().save(file_name)
        with open(file_name, mode='rb') as f:
            file = f.read()
        allure.attach(file, img_doc, allure.attachment_type.PNG)
        LogRoot.info(f"已保存截图至{file_name}")



    #下拉框选中
    def listbox_choice(self, click_index=1,parent=2,**kwargs):
        """
        :param click_index: 下拉框index
        :param parent:1父级、2层父级 3层父级
        :return:
        """
        application_child = self.click(**kwargs).children()
        LogRoot.info(f"下拉列表，第{click_index}个")
        if parent == 1 :
            self.click(control=application_child[click_index])
        elif parent == 2:
            control=application_child[0].children()[click_index]
            self.click(control=control)
        elif parent == 3:
            self.click(control=application_child[0].children()[0].children()[click_index])

    #等待出现
    def wait(self, timeout=9999, **kwargs):
        # self.find(**kwargs).wait(wait_for="exists enabled visible ready", timeout=timeout)
        self._dlg.child_window(**kwargs).wait(wait_for="exists enabled visible ready", timeout=timeout)


    #等待消失
    def wait_not(self,timeout=9999,**kwargs):
        self._dlg.child_window(**kwargs).wait_not(wait_for_not="exists enabled visible ready",timeout=timeout)

    #点击下一步按钮
    def click_next_button(self):
        self.click(title="下一步", auto_id="FormMain.nextStepWidget.pbNextStep", control_type="Button")

    #控件从出现到消失的总时长
    def wait_time(self,**kwargs):
        self.wait(**kwargs,timeout=5)
        LogRoot.info(f"控件出现{datetime.now()}")
        start_time = datetime.now().replace(microsecond=0)
        self.wait_not(**kwargs)
        LogRoot.info(f"控件消失{datetime.now()}")
        end_time = datetime.now().replace(microsecond=0)
        time = end_time-start_time
        LogRoot.info(f"存在时长{time}")
        return time

