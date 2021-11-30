#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @author:Gemini
# @time:  2021/11/18:15:56
# @email: 13259727865@163.com
from typing import List

from pywinauto import WindowSpecification
from pywinauto.controls.uia_controls import StaticWrapper

from base.main import Main



class Support(Main):

    def support_parent(self,index):
        support_parent:List[WindowSpecification] = self.find(
        auto_id="FormMain.rightwidget.stackedWidget.FormSupports.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents",
        control_type="Group").children()
        if index:
            auto_id=support_parent[index].get_properties()["automation_id"]
            return auto_id
        else:
            return support_parent

    # 返回支撑页：应用、支撑设置栏文本字典
    def return_all_parameter(self):
        support_static_dict = {}
        support_child = self.support_parent()
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

    #选择应用
    def choice_application(self,click_index = 1,parent=2):
        """
        :param click_index: 下拉框index
        :param parents: 通过第几层父级查找
        :param kwargs: 父级控件
        :return:
        """

        application_parent = self.support_parent(2)
        self.listbox_choice(parent=parent, click_index=click_index,isall=False,auto_id=application_parent)

    #支撑设置按钮操作
    def support_set_button(self,oper="保存"):
        """
        :param oper_index: 按钮类型：保存-导入-导出-刷新-删除
        :return:
        """
        if oper == "保存":
            self.click(self.support_parent()[5])
        elif oper == "导入":
            self.click(self.support_parent()[6])
        elif oper == "导入":
            self.click(self.support_parent()[7])
        elif oper == "导入":
            self.click(self.support_parent()[8])
        elif oper == "导入":
            self.click(self.support_parent()[9])
        else:
            print("输入有误")

    #推荐参数下拉框选择
    def choice_recommend(self,click_index = 1,parent=2):
        auto_id = "FormMain.rightwidget.stackedWidget.FormSupports.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents.cbpara"
        control_type = "ComboBox"
        self.listbox_choice(parent=parent,click_index=click_index,auto_id=auto_id,control_type=control_type)

    #支撑设置展开/关闭
    def basic_setup_open(self,oper = "基础设置"):
        self.click(index=oper)

    #输入参数值
    def input_parameter(self,oper_text="抬升高度"):
        print(self.find(index=oper_text).parent().get_properties())


