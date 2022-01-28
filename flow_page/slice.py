#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @author:Gemini
# @time:  2021/11/18:16:24
# @email: 13259727865@163.com
from typing import Dict

from pywinauto.keyboard import send_keys

from base.main import Main
from common.logger import LogRoot
from flow_frame.slice_frame import SliceFrame


class Slice(Main):
    #切片页最高父级
    def slice_parent(self):
        slice_parent = \
            self.find(auto_id="FormMain.rightwidget.stackedWidget.FormPrintSetting.scrollArea.qt_scrollarea_viewport"
                              ".scrollAreaWidgetContents.widgetRDMode", control_type="Group")
        return slice_parent



    #点击层厚类型（推荐、自定义）
    def choice_thickness_type(self,type):
        """
        :param type: "推荐" or "自定义"
        :return:
        """

        thickness_types = self.slice_parent().children()[1].children()[1].children()
        print(thickness_types)
        LogRoot.info(f"在{type}里操作")
        if type == "推荐":
            self.click(control=thickness_types[0])
        elif type == "自定义":
            self.click(control=thickness_types[1])
        else:
            LogRoot.error(f"限制为：推荐、自定义，{type}无效")


    #推荐层厚选择
    def recommended_thickness(self,click_index):

        thickness_parent_autoid = \
            self.slice_parent().children()[1].children()[0].children()[0].children()[0].get_properties()["automation_id"]
        try:
            self.listbox_choice(parent=2, click_index=click_index, isall=False, auto_id=thickness_parent_autoid)
        except IndexError :
            LogRoot.error("该组参数无推荐层厚")


    #推荐层厚有无快慢两种打印方式
    def is_mode(self):
        # 侧后下拉框和切片方式下拉框的列表
        thickness_parent = self.slice_parent().children()[1].children()[0].children()[0].children()
        if len(thickness_parent)>1:
            LogRoot.info("该组参数可以设置快慢两种打印方式")
            return True
        else:
            LogRoot.error("该组参数不可以设置快慢两种打印方式")
            return False

    #推荐快慢类型选择
    def recommended_type(self,click_index):
        thickness_parent_autoid = \
        self.slice_parent().children()[1].children()[0].children()[0].children()[1].get_properties()["automation_id"]
        self.listbox_choice(parent=2, click_index=click_index, isall=False, auto_id=thickness_parent_autoid)

    #自定义层厚输入及展示框
    def customized_thickness(self,oper="texts",value=None):
        """
        :param oper: texts or insert
        value=None
        :return:
        """
        customized_thickness = \
            self.slice_parent().children()[1].children()[0].children()[0].children()[0].get_properties()[
                "automation_id"]
        if oper is "texts":
            thickness_text = self.find(auto_id=customized_thickness,isall=False,text=True)
            LogRoot.info(f"自定义层厚为{thickness_text}")
            return thickness_text
        elif oper is "insert":
            self.insert(value=value,auto_id=customized_thickness,isall=False)


    # 自定义层厚选择
    def customized_name_choice(self, click_index):
        customized_name = \
            self.slice_parent().children()[1].children()[0].children()[0].children()[1].get_properties()[
                "automation_id"]
        try:
            self.listbox_choice(parent=2, click_index=click_index, isall=False, auto_id=customized_name)
        except IndexError :
            LogRoot.error("该组参数无自定义层厚")

    #自定义层厚下拉框内容
    def customized_name_list(self):
        customized_list = \
            self.slice_parent().children()[1].children()[0].children()[0].children()[1].texts()
        return customized_list


    #自定义参数删除按钮
    def customized_delete(self):
        customized_delete = \
            self.slice_parent().children()[1].children()[0].children()[0].children()[2].get_properties()[
                "automation_id"]
        self.click(auto_id=customized_delete,isall=False)
        LogRoot.info("删除当前自定义参数")


    #判断高级设置是否打开
    def isfind_compensation(self):
        isfind = self.find(auto_id="FormMain.rightwidget.stackedWidget.FormPrintSetting.scrollArea.qt_scrollarea_viewport."
                          "scrollAreaWidgetContents.widgetRDMode.labelShrinkageRd", control_type="Text",isall=False)
        if isfind:
            LogRoot.info("高级设置已打开")
            return True
        else:
            LogRoot.info("高级设置未打开")
            return False

    #修改精度补偿参数
    def update_compensation(self,kwargs:Dict):
        if self.isfind_compensation() is False:
            self.click(auto_id="FormMain.rightwidget.stackedWidget.FormPrintSetting.scrollArea.qt_scrollarea_viewport."
                               "scrollAreaWidgetContents.widgetRDMode.pbArrow", control_type="Button")
        compensation_list = self.slice_parent().children()
        for key,value in kwargs.items():
            for i in compensation_list:
                if key == i.texts()[0]:
                    update_index = compensation_list.index(i)+1
                    self.click(control=compensation_list[update_index])
                    send_keys("^a")
                    send_keys(str(value))
        LogRoot.info(f"{kwargs}修改完成")

    #保存
    def slice_save(self):
        self.click(self.slice_parent().children()[-1])
        LogRoot.info("点击保存按钮")
        return SliceFrame(self._dlg)

    #切片
    def slice(self):
        self.click(auto_id="FormMain.nextStepWidget.pbNextStep", control_type="Button",isall=False)
        return SliceFrame(self._dlg)