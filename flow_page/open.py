#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @author:Gemini
# @time:  2021/12/29:14:34
# @email: 13259727865@163.com
from base.main import Main
from common.logger import LogRoot


class Open(Main):
    #打开零件
    def openfile(self, path, model):
        """
        :param path: 模型路径
        :param model: 模型名称，多模型例 '"格子收纳盒.stl""heart.stl"'
        :return: 按钮文本
        """
        try:
            openfile_text = self.find(title="本地打开", auto_id="FormMain.rightwidget.stackedWidget.FormLoad.pbLocal",
                                      control_type="Button").texts()[0]
            self.click(title="本地打开", auto_id="FormMain.rightwidget.stackedWidget.FormLoad.pbLocal",
                       control_type="Button")
            LogRoot.info("点击本地打开按钮")
            self.win_desktop(win_title="打开文件", path_bar="Toolbar3", path=path, filename=model)
            LogRoot.info("操作打开文件win弹窗")
            LogRoot.info("返回按钮text")
            return openfile_text
        except Exception as e:
            LogRoot.error("报错处理", e)