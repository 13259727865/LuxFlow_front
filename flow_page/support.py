#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @author:Gemini
# @time:  2021/11/18:15:56
# @email: 13259727865@163.com
from pywinauto.controls.uia_controls import StaticWrapper

from base.main import Main


class Support(Main):

    #返回支撑页：应用、支撑设置栏文本字典
    def return_all_parameter(self):
        support_static_dict = {}
        support_child = self.find(
            auto_id="FormMain.rightwidget.stackedWidget.FormSupports.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents",
            control_type="Group").children()
        s = 0
        for i in range(0,len(support_child)) :
            if i < 11:
                if support_child[i].texts()[0]:
                    s += 1
                    if len(support_child[i].texts())<2:
                        support_static_dict[f"support{s}"]=support_child[i].texts()[0]
                    elif len(support_child[i].texts())>1:
                        support_static_dict[f"support{s}"] = support_child[i].texts()
            elif i>=11:
                if support_child[i].texts()[0]:
                    s += 1
                    if type(support_child[i].texts()[0])==list:
                        support_static_dict[f"support{s}"] = support_child[i].texts()[0][0]
                    else:
                        support_static_dict[f"support{s}"] = support_child[i].texts()[0]
                elif support_child[i].texts()[0] == "":
                    if len(support_child[i].children())>0:
                        for j in range(0,len(support_child[i].children())):
                            if support_child[i].children()[j].texts()[0]:
                                s += 1
                                support_static_dict[f"support{s}"] = support_child[i].children()[j].texts()[0]
        return support_static_dict




