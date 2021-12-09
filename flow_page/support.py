#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @author:Gemini
# @time:  2021/11/18:15:56
# @email: 13259727865@163.com
from typing import List

from pywinauto import WindowSpecification, mouse
from pywinauto.controls.uia_controls import StaticWrapper
from pywinauto.keyboard import send_keys

from base.main import Main
from flow_frame.support_frame import SaveFrame


class Support(Main):

    #获取支撑页父级目录
    def support_parent(self, index=None):
        """
        :param index: 父级目录下index
        :return:
        """
        support_parent: List[WindowSpecification] = self.find(
            auto_id="FormMain.rightwidget.stackedWidget.FormSupports.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents",
            control_type="Group").children()
        if index:
            auto_id = support_parent[index].get_properties()["automation_id"]
            #返回父目录下第index个子控件的auto_id
            return auto_id
        else:
            #返回父控件
            return support_parent

    # 返回支撑页：应用、支撑设置栏文本字典
    def return_all_parameter(self):
        support_static_dict = {}
        support_child = self.support_parent()
        s = 0
        for i in range(0, len(support_child)):
            if i < 11:
                if support_child[i].texts()[0]:
                    s += 1
                    if len(support_child[i].texts()) < 2:
                        support_static_dict[f"support{s}"] = support_child[i].texts()[0]
                    elif len(support_child[i].texts()) > 1:
                        support_static_dict[f"support{s}"] = support_child[i].texts()
            elif i >= 11:
                if support_child[i].texts()[0]:
                    s += 1
                    if type(support_child[i].texts()[0]) == list:
                        support_static_dict[f"support{s}"] = support_child[i].texts()[0][0]
                    else:
                        support_static_dict[f"support{s}"] = support_child[i].texts()[0]
                elif support_child[i].texts()[0] == "":
                    if len(support_child[i].children()) > 0:
                        for j in range(0, len(support_child[i].children())):
                            if support_child[i].children()[j].texts()[0]:
                                s += 1
                                support_static_dict[f"support{s}"] = support_child[i].children()[j].texts()[0]
        return support_static_dict

    # 选择应用
    def choice_application(self, click_index=1, parent=2):
        """
        :param click_index: 下拉框index
        :param parents: 通过第几层父级查找
        :param kwargs: 父级控件
        :return:
        """
        application_parent = self.support_parent(index=2)
        self.listbox_choice(parent=parent, click_index=click_index, isall=False, auto_id=application_parent)

    # 支撑设置按钮操作
    def support_set_button(self, oper="保存", **kwargs):
        """
        :param oper_index: 按钮类型：保存-导入-导出-刷新-删除
        :return:
        """
        if oper == "保存":
            auto_id = self.support_parent(index=5)
            self.click(isall=False, auto_id=auto_id)
            return SaveFrame(self._dlg)
        elif oper == "导入":
            auto_id = self.support_parent(index=6)
            self.click(isall=False, auto_id=auto_id)
            return self.import_export_parameter(oper, **kwargs)
        elif oper == "导出":
            auto_id = self.support_parent(index=7)
            self.click(isall=False, auto_id=auto_id)
            return self.import_export_parameter(oper, **kwargs)
        elif oper == "刷新":
            auto_id = self.support_parent(index=8)
            self.click(isall=False, auto_id=auto_id)
            return self.support_is_frame(oper)
        elif oper == "删除":
            auto_id = self.support_parent(index=9)
            self.click(isall=False, auto_id=auto_id)
            return self.support_is_frame(oper)
        else:
            print("输入有误")

    # 保存参数弹框
    def save_frame(self, close=False, value=None, save_oper="保存"):
        """
        :param close: 是否直接关闭
        :param value: 输入的名称
        :param oper: 保存（default）、取消
        :return:
        """

        if close :
            self.click(auto_id="FormSupportCfgSaveName.widget.pbPopClose", control_type="Button")
            return "关闭弹框"
        if value:
            self.click(auto_id="FormSupportCfgSaveName.lineEdit", control_type="Edit")
            send_keys(value)

        if save_oper == "保存":
            self.click(auto_id="FormSupportCfgSaveName.pushButtonSave", control_type="Button",isall=False)
            self._dlg.print_control_identifiers()
        elif save_oper == "取消":
            self.click(auto_id="FormSupportCfgSaveName.pushButtonCancel", control_type="Button",isall=False)
        else:
            print("oper参数有误")

    #刷新和删除弹框提示
    def support_is_frame(self,is_oper=True,close=False):
        """
        :param is_oper: True（default） or Flase :是 与 否
        :param close: 是否直接关闭弹框
        :return:
        """
        message=self.find(auto_id="FormMain.rightwidget.stackedWidget.FormSupports.MyMessageBox", control_type="Window",isall=False).children()
        print(message)
        if close:
            self.click(auto_id = message[0].children()[1].get_properties()["automation_id"])
            return
        elif is_oper:
            self.click(auto_id=message[4].get_properties()["automation_id"],isall=False)
        elif is_oper == False:
            self.click(control=message[3].get_properties()["automation_id"],isall=False)
        return


    #导入导出操作
    def import_export_parameter(self, oper="导入", path=None, conf=None):
        """
        :param path: 文件路径
        :param conf: 支撑配置文件名
        :param oper: 操作：导入（default）、导出
        :return:
        """
        if oper == "导入":
            self.win_desktop(win_title="打开配置文件",path_bar="Toolbar3",path=path,filename=conf,title="打开(&O)", class_name="Button")
            self._dlg.print_control_identifiers()
        elif oper == "导出":
            self.win_desktop(win_title="保存配置文件",path_bar="Toolbar4", path = path,filename=conf,title="保存(&S)", class_name="Button")


    # 推荐参数下拉框选择
    def choice_recommend(self, click_index=1, parent=2):
        application_parent = self.support_parent(10)
        self.listbox_choice(parent=parent, click_index=click_index, isall=False, auto_id=application_parent)


    # 支撑设置展开/关闭
    def basic_setup_open(self, oper="基础设置"):
        self.click(index=oper)

    # 输入参数值
    def input_parameter(self,kwargs):
        """
        :param kwargs: {"抬升高度"：10.8，“角度”：45}
        :return:
        """
        outside = self.find(auto_id="FormMain.rightwidget.stackedWidget.FormSupports.scrollArea.qt_scrollarea_viewport", control_type="Group")
        switch_parent = {"Basics_auto_id":"FormMain.rightwidget.stackedWidget.FormSupports.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents.widgetContaintBasic",
                         "reinforce_auto_id":"FormMain.rightwidget.stackedWidget.FormSupports.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents.widgetContaintReinforce",
                         "base_auto_id":"FormMain.rightwidget.stackedWidget.FormSupports.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents.widgetContaintBase"}
        switch_button = {"Basics_auto_id":"FormMain.rightwidget.stackedWidget.FormSupports.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents.widgetBarBasic",
                         "reinforce_auto_id":"FormMain.rightwidget.stackedWidget.FormSupports.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents.widgetBarReinforce",
                         "base_auto_id":"FormMain.rightwidget.stackedWidget.FormSupports.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents.widgetBarBase"

        }
        for key,value in switch_parent.items():
            if self.find(auto_id=value,isall=False)==False:
                switch = self.find(auto_id=switch_button[key],isall=False)
                self.is_in_outside(outside=outside,control=switch)
                self.click(control=switch)

        for oper_key,oper_value in kwargs.items():
            oper_control = self.find(index=oper_key)
            parent = oper_control.parent()
            children = parent.children()

            if oper_control :
                oper_auto_id=oper_control.get_properties()["automation_id"]
            else:
                return f"未找到{oper_key}"

            for i in range(len(children)):
                auto_id = children[i].get_properties()["automation_id"]
                if auto_id == oper_auto_id:
                    # print(self.find(auto_id=parent[i + 1].get_properties()["automation_id"], isall=False).is_visible(),"是否可见")
                    # mouse.scroll(coords=(3654, 477), wheel_dist=-2)
                    control = self.find(auto_id=children[i+1].get_properties()["automation_id"],isall=False)
                    self.is_in_outside(outside=parent.parent().parent(),control=control)
                    self.click(control=control)
                    send_keys("^a")
                    send_keys(str(oper_value))



