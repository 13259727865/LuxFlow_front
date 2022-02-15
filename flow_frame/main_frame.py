#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @author:Gemini
# @time:  2021/12/30:16:46
# @email: 13259727865@163.com
from pywinauto.keyboard import send_keys
from base.main import Main
from common.logger import LogRoot


class FrameSet(Main):
    """
    设置弹框内控件
    """

    # 设置弹框右上角关闭按钮
    def set_close(self):
        self.click(auto_id="FormMain.widgetTitle.FormSoftSetting.widgetTitle.pbPopClose", control_type="Button")

    # 语言下拉框选择
    def set_language(self, language):
        """
        :param language: "英""日""中"
        :return: 下拉框内容列表：['En', '日本語', '中']
        """
        self.click(auto_id="FormMain.widgetTitle.FormSoftSetting.cbLanguage", control_type="ComboBox")
        children_texts = self.find(index="ListBox").texts()

        try:
            if language == "英":
                self.click(title="En", control_type="ListItem")
            elif language == "日":
                self.click(title="日本語", control_type="ListItem")
            elif language == "中":
                self.click(title="中", control_type="ListItem")
        except :
            print("目前只支持参数：中、英、日")
        return children_texts

    # 设置弹框ip输入
    def set_ip(self, ip):
        self.click("IP 设置Edit")
        send_keys("^a")
        send_keys(ip)

    # 设置弹框端口输入
    def set_port(self, port):
        self.click("IP 端口Edit")
        send_keys(port)

    # 设置弹框确认按钮
    def set_sure(self):
        self.click(title="Cancel", auto_id="FormMain.widgetTitle.FormSoftSetting.pbCancel", control_type="RadioButton")

    # 设置弹框取消按钮
    def set_cancel(self):
        self.click(title="取消", auto_id="FormMain.widgetTitle.FormSoftSetting.pbCancel", control_type="RadioButton")


class MaterialFrame(Main):
    pass


# 选择设备弹框
class TerminalFrame(Main):
    # 选择设备页父级的子集
    def terminal_parent(self):
        terminal_parent = self.find(auto_id="FormMain.openGLWidget.FormDeviceTypeSelection", control_type="Window",
                                    isall=False)
        return terminal_parent.children()

    def choice_terminal(self, terminal_index):
        choice_terminal_autoid = self.terminal_parent()[1].get_properties()["automation_id"]
        choice_terminal_children = self.find(auto_id=choice_terminal_autoid, isall=False).children()
        terminal_page = terminal_index // 6 + 1
        # terminal_page_index
        if terminal_page == 1:
            self.click(control=choice_terminal_children[terminal_index])
        elif terminal_page > 1:
            pass


class CopyFrame(Main):
    # 复制弹框
    def copyFrame(self):
        copyframe = self.find(auto_id="FormMain.openGLWidget.FormCopyParts", control_type="Window", isall=False)
        return copyframe

    # 复制次数填写
    def copy_num(self, copy_num):
        self.insert(value=copy_num, control=self.copyFrame().children()[1].children()[2])

    # +或-按钮
    def copy_num_button(self, click_num):
        """
        :param click_num: 点击+、-按钮，click_num为正数点击+，负数点击-
        :return:
        """
        if click_num > 0:
            for i in range(click_num):
                self.click(control=self.copyFrame().children()[1].children()[3])
        elif click_num < 0:
            for i in range(click_num):
                self.click(control=self.copyFrame().children()[1].children()[1])
        else:
            LogRoot.error("请检查参数！")

    # 复制按钮
    def copy(self):
        self.click(control=self.copyFrame().children()[1].children()[4])

    # 镜像复制
    def image_copy(self, oper, oper_num=1):
        """
        :param oper: 'XY','XZ','YZ'
        :param oper_num: 点击次数：1(default)
        :return:
        """
        for i in range(oper_num):
            if oper == "XY":
                self.click(control=self.copyFrame().children()[3].children()[1])
            elif oper == "XZ":
                self.click(control=self.copyFrame().children()[3].children()[2])
            elif oper == "YZ":
                self.click(control=self.copyFrame().children()[3].children()[3])
            else:
                LogRoot.error("请检查参数！！")

    # 关闭复制功能弹框
    def copyFrame_close(self):
        self.click(control=self.copyFrame().children()[0].children()[1])
