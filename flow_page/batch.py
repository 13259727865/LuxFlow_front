#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @author:Gemini
# @time:  2021/11/18:16:22
# @email: 13259727865@163.com
from pywinauto.controls.uia_controls import ButtonWrapper
from pywinauto.keyboard import send_keys

from base.main import Main
from common.logger import LogRoot
from flow_frame.batch_frame import BatchFrame
from flow_page.marking import Marking
from flow_page.slice import Slice


class Batch(Main):
    #编码页控件list
    def batch_parent_children(self):
        batch_parent_children=self.find(
            auto_id="FormMain.rightwidget.stackedWidget.FormLayout.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents.layoutWidget",
            control_type="Group").children()

        return batch_parent_children


    #返回编码页所有文本信息
    def return_batch_texts(self):
        batch_texts = []
        for i in self.batch_parent_children():
            tests = i.texts()[0]
            if tests:
                batch_texts.append(i.texts()[0])
        a = self.find(title="整齐布局", auto_id="FormMain.rightwidget.stackedWidget.FormLayout.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents.layoutWidget.rbNeatLayout", control_type="RadioButton")
        self._dlg.print_control_identifiers()
        ButtonWrapper(a.TCheckBox.WrapperObject()).GetCheckState()
        LogRoot.info(f"返回编码页参数文本{batch_texts}")
        return batch_texts

    #间距设置
    def set_spacing(self,spacing=None,second=0):
        """
        :param spacing: 间距值
        :param button: "add"增加按钮，“sub”减少按钮，，（可直接由second的正负控制，该参数可忽略）
        :param second:点击按钮次数，负数点击button的反值
        :return:
        """
        LogRoot.info("开始输入间距设置")
        if spacing == None and second == 0 :
            LogRoot.error("请填写至少一个参数")
            return
        batch_parent_children = self.batch_parent_children()
        if spacing:
            self.insert(value=spacing,control=batch_parent_children[3])
            LogRoot.info(f"输入参数值{spacing}")
        if second:
            if second > 0:
                for i in range(second):
                    self.click(control=batch_parent_children[4])
            elif second < 0:
                for i in range(abs(second)):
                    self.click(control=batch_parent_children[2])


    #选择布局方式
    def layout_mode(self,mode=1):
        """
        :param mode: "整齐布局" or "嵌套布局"
        :return:
        """
        if mode == 1 or mode == "整齐布局":
            self.click(control=self.batch_parent_children()[5])
            LogRoot.info("选择整齐布局")
        elif mode == 2 or mode == "嵌套布局":
            self.click(control=self.batch_parent_children()[6])
            LogRoot.info("选择嵌套布局")

    #布局按钮
    def layout(self):
        self.click(self.batch_parent_children()[7])
        LogRoot.info("开始布局")
        return BatchFrame(self._dlg)



    #下一步
    def next_step(self):
        """
        :return: 下一页控件类
        """
        self.click_next_button()
        # 跳转切片页
        LogRoot.info("进入编码页")
        return Slice(self._dlg)