#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @author:Gemini
# @time:  2021/11/18:15:56
# @email: 13259727865@163.com
from typing import List

from pywinauto import WindowSpecification, mouse
from pywinauto.keyboard import send_keys

from base.main import Main
from common.logger import LogRoot
from flow_frame.support_frame import SupportFrame
from flow_page.batch import Batch


class Support(Main):

    #获取支撑页父级目录
    def support_parent(self, index=None,sonindex=None):
        """
        :param index: 父级目录下index
        :return:
        """
        support_parent: List[WindowSpecification] = self.find(
            auto_id="FormMain.rightwidget.stackedWidget.FormSupports.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents",
            control_type="Group").children()
        if index:
            if sonindex:
                # 返回父目录下第index个子控件的第sunindex个子空间的auto_id
                auto_id = support_parent[index].children()[sonindex].get_properties()["automation_id"]
            else:
                # 返回父目录下第index个子控件的auto_id
                auto_id = support_parent[index].get_properties()["automation_id"]
            return auto_id
        else:
            #返回父控件
            return support_parent


    #基础设置、加固设置、底座设置是否全部展开。如果有未展开的，点击展开
    def support_is_open(self):
        switch_button = {
            "Basics_auto_id":"FormMain.rightwidget.stackedWidget.FormSupports.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents.widgetBarBasic.pushButtonBasic",
            "reinforce_auto_id":"FormMain.rightwidget.stackedWidget.FormSupports.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents.widgetBarReinforce.pushButtonReinforce",
            "base_auto_id": "FormMain.rightwidget.stackedWidget.FormSupports.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents.widgetBarBase.pushButtonBase"
            }
        for value in switch_button.values():
            checkbox = self.find(auto_id=value, isall=False)
            if checkbox.get_toggle_state() == 0:
                checkbox.click()


    # 返回支撑页：应用、支撑设置栏文本字典
    def return_all_texts(self,open=True):
        """
        open: 是否需要全部展开
        :return: {'support1': '支撑', 'support2': '应用', 'support3': ['齿科产品', '鞋类产品', '眼镜产品', '其他产品'],
        'support4': '支撑设置', 'support5': ['推荐参数', '123'], 'support6': '基础设置', 'support7': '抬升高度',
        'support8': '2.50 mm', 'support9': '支撑点直径', 'support10': '1.20 mm', 'support11': '支撑头长度',
        'support12': '2.00 mm', 'support13': '支撑柱直径', 'support14': '1.20 mm', 'support15': '支撑点间距',
        'support16': '4.00 mm', 'support17': '临界角', 'support18': '70.00 °', 'support19': '加固设置',
        'support20': '是否加固', 'support21': 0, 'support22': '起始高度', 'support23': '0.01 mm', 'support24': '角度',
        'support25': '45.00 °', 'support26': '底座设置', 'support27': '支撑加底座', 'support28': 0, 'support29': '仅底座',
         'support30': 0, 'support31': '底座高度', 'support32': '0.30 mm', 'support33': '生 成', 'support34': '删 除',
          'support35': '编辑'}

        """
        support_static_dict = {}
        if open:
            self.support_is_open()
        support_child = self.support_parent()
        s = 0
        for i in range(0, len(support_child)):
            if i < 11:
                if support_child[i].texts()[0]:
                    s += 1
                    if len(support_child[i].texts()) < 2:
                        support_static_dict[f"support{s}"] = support_child[i].texts()[0]
                        # s += 1
                        # support_static_dict[f"support{s}"] = support_child[i].texts()[0]
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
                            text=support_child[i].children()[j].texts()[0]
                            if text:
                                if text=="是否加固" or text=="支撑加底座" or text=="仅底座":
                                    s += 1
                                    support_static_dict[f"support{s}"] = support_child[i].children()[j].texts()[0]
                                    s += 1
                                    support_static_dict[f"support{s}"] = support_child[i].children()[j].get_toggle_state()
                                else:
                                    s += 1
                                    support_static_dict[f"support{s}"] = support_child[i].children()[j].texts()[0]
        # LogRoot.info(f"返回支撑页参数{support_static_dict}")
        return support_static_dict




    # 选择应用
    def choice_application(self, click_index, parent=2):
        """
        :param click_index: 下拉框index
        :param parents: 通过第几层父级查找
        :param kwargs: 父级控件
        :return:
        """
        application_parent = self.support_parent(index=2)
        self.listbox_choice(parent=parent, click_index=click_index, isall=False, auto_id=application_parent)
        LogRoot.info(f"选择第{click_index}项应用")



    # 支撑设置按钮操作
    def support_set_button(self, oper,path=None,conffile=None,whether=True,isclose=False):
        """
        :param oper_index: 按钮类型：保存-导入-导出-刷新-删除
        :return:
        """
        if oper == "保存":
            auto_id = self.support_parent(index=5)
            self.click(isall=False, auto_id=auto_id)
            LogRoot.info("点击保存，进入弹框")
            return SupportFrame(self._dlg)
        elif oper == "导入":
            auto_id = self.support_parent(index=6)
            self.click(isall=False, auto_id=auto_id)
            LogRoot.info("点击导入，进入弹框")
            return SupportFrame(self._dlg).import_export_parameter(oper=oper,path=path,conf=conffile)
        elif oper == "导出":
            auto_id = self.support_parent(index=7)
            self.click(isall=False, auto_id=auto_id)
            LogRoot.info("点击导出，进入弹框")
            # return self.import_export_parameter(oper, **kwargs)
            return SupportFrame(self._dlg).import_export_parameter(oper=oper,path=path,conf=conffile)
        elif oper == "刷新":
            auto_id = self.support_parent(index=8)
            self.click(isall=False, auto_id=auto_id)
            LogRoot.info("点击刷新，进入弹框")
            return SupportFrame(self._dlg).support_is_frame(is_oper=whether,isclose=isclose)
        elif oper == "删除":
            auto_id = self.support_parent(index=9)
            self.click(isall=False, auto_id=auto_id)
            LogRoot.info("点击删除，进入弹框")
            return SupportFrame(self._dlg).support_is_frame(is_oper=whether,isclose=isclose)
        else:
            LogRoot.info("输入有误")



    # 推荐参数下拉框选择
    def choice_recommend(self, click_index=1):
        application_parent = self.support_parent(10)
        self.listbox_choice(parent=2, click_index=click_index, isall=False, auto_id=application_parent)
        LogRoot.info(f"选择第{click_index}项推荐参数")

    # 支撑设置展开/关闭
    def basic_setup_open(self, oper="基础设置"):
        self.click(index=oper)
        LogRoot.info("展开/关闭oper")


    # 输入参数值
    def input_parameter(self,kwargs):
        """
        :param kwargs: {"抬升高度"：10.8，“角度”：45,"是否加固":False,"支撑加底座":True}
        :return:
        """
        LogRoot.info(f"输入参数{kwargs}")
        self.support_is_open()
        for oper_key,oper_value in kwargs.items():
            oper_control = self.find(index=oper_key)
            parent = oper_control.parent()
            children = parent.children()
            if oper_key == "是否加固" or oper_key == "支撑加底座" or oper_key == "仅底座":
                state = self.find(index=oper_key).get_toggle_state()
                if (oper_value and state==0) or (oper_value ==False and state==1) :
                    self.click(index=oper_key)
                    LogRoot.info(f"点击{oper_key}")
            if oper_control :
                oper_auto_id=oper_control.get_properties()["automation_id"]
            else:
                LogRoot.error(f"未找到{oper_key}")
                return

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

    #生成-删除-编辑
    def support_oper(self,oper="生成"):
        self.click(index=oper)
        LogRoot.info(oper)

    #下一步
    def next_step(self):
        """
        :return: 下一页控件类
        """
        self.click_next_button()
        # 跳转支撑页
        LogRoot.info("进入布局页")
        return Batch(self._dlg)


