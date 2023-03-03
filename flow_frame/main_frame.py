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
        except:
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

    # 默认设备
    def default_terminal(self):
        default_terminal = \
            self.find(auto_id="FormMain.toolWidgte.pbDevice", control_type="CheckBox", isall=False).texts()[0]
        return default_terminal

    # 选择设备
    def choice_terminal(self, terminal_code):

        choice_terminal_autoid = self.terminal_parent()[1].get_properties()["automation_id"]
        choice_terminal = self.find(auto_id=choice_terminal_autoid, isall=False)
        self.scroll(control=choice_terminal, dist=1)
        if terminal_code <= 6:
            self.click(control=self.find(auto_id=choice_terminal_autoid, isall=False).children()[terminal_code - 1])
        elif terminal_code > 6:
            self.scroll(control=choice_terminal, dist=-1)
            terminal_code = terminal_code - 6
            self.click(control=self.find(auto_id=choice_terminal_autoid, isall=False).children()[terminal_code - 1])
        else:
            LogRoot.error("参数错误或找不到该设备")

    # 成形台选择
    def choice_forming(self, forming_code=None):
        forming = self.terminal_parent()[2].children()[0].children()[1]
        if type(forming_code) is int:
            self.click(control=forming)
            self.click(control=forming.children()[0].children()[forming_code - 1])
        return forming

    # 选择膜
    def choice_membrane(self, membrane_code=None):
        forming = self.terminal_parent()[2].children()[0].children()[3]
        if type(membrane_code) is int:
            self.click(control=forming)
            self.click(control=forming.children()[0].children()[membrane_code - 1])
        return forming

    # 确认or取消
    def confirm_cancel(self, oper="confirm"):
        """
        :param oper: confirm(确认) or cancel(取消)
        :return:
        """
        if oper is "confirm":
            self.click(control=self.terminal_parent()[3])
        elif oper is "cancel":
            self.click(control=self.terminal_parent()[4])
        else:
            LogRoot.error("参数有误：oper: confirm(确认) or cancel(取消)")


# 修复检测弹框
class RepairModle(Main):
    # 没有上传模型点击修复
    def no_modle(self):
        tips = self.wait(auto_id="FormMain.openGLWidget.FormVDFix.MyMessageBox.labelMessageText", control_type="Text")
        text = tips.texts()[0]
        return text

    # 点击弹框提示中“好的”按钮
    def tips_ok(self):
        self.click(auto_id="FormMain.openGLWidget.FormVDFix.MyMessageBox.pbConfirm", control_type="CheckBox",
                   isall=False)

    def repair_parent(self):
        repir_parent = self.find(title="Form", auto_id="FormMain.openGLWidget.FormVDFix",
                               control_type="Window")

        return repir_parent

    # 检测结果
    def testing_result(self):
        testing_result_dict = {}
        testing_chil = self.repair_parent().children()
        for i in testing_chil[5:19:3]:
            testing_result_dict[i.texts()[0]] = testing_chil[testing_chil.index(i) + 2].texts()[0]
        return testing_result_dict


    #检测按钮,可勾选三角面片
    def testing_button(self, checkout=None):
        """
        :param checkout: None(default):默认不勾选最后两项
                        1：勾选“反向三角面片”
                        2：勾选“相交三角面片”
                        3、同时勾选“反向三角面片”和“相交三角面片”
        :return: 检测结果 {'坏边': '0', '孔洞': '0', '壳体': '1', '反向三角面片': '-', '相交三角面片': '-'}
        """
        testing_chil = self.repair_parent().children()
        if checkout:
            if checkout == 1:
                reverse = testing_chil[14]
                reverse_status = reverse.get_toggle_state()
                if reverse_status == 0:
                    self.click(control=reverse)
                else:
                    LogRoot.error("反向三角已经是勾选状态，无需勾选")
            elif checkout == 2:
                intersect = testing_chil[17]
                reverse_status = intersect.get_toggle_state()
                if reverse_status == 0:
                    self.click(control=intersect)
                else:
                    LogRoot.error("相交三角已经是勾选状态，无需勾选")
            elif checkout == 3:
                reverse = testing_chil[14]
                reverse_status = reverse.get_toggle_state()
                if reverse_status == 0:
                    self.click(control=reverse)
                intersect = testing_chil[17]
                reverse_status = intersect.get_toggle_state()
                if reverse_status == 0:
                    self.click(control=intersect)
        testing_button = self.repair_parent().children()[20]
        self.click(control=testing_button)
        self.wait_time(auto_id="FormMain.openGLWidget.CProgress.widgetTitle", control_type="Group")


    #修复按钮
    def repair_button(self):
        repair_button = self.repair_parent().children()[21]
        self.click(control=repair_button)
        self.wait_time(auto_id="FormMain.openGLWidget.CProgress.widgetTitle", control_type="Group")

        # child_window(title="旋转", auto_id="FormMain.openGLWidget.CProgress", control_type="Window")
        # | |
        # | | GroupBox - ''(L2560, T428, R3200, B474)
        # | | ['GroupBox', '检测中，请等待GroupBox', 'GroupBox0', 'GroupBox1']
        # | | child_window(auto_id="FormMain.openGLWidget.CProgress.widgetTitle", control_type="Group")
        # | | |
        # | | | Static - '检测中，请等待'(L2590, T428, R2745, B474)
        # | | | ['检测中，请等待Static', '检测中，请等待', 'Static', 'Static0', 'Static1']
        # | | | child_window(title="检测中，请等待", auto_id="FormMain.openGLWidget.CProgress.widgetTitle.popTitle",
        #                    control_type="Text")
        # | | |
        # | | | Button - ''(L3140, T431, R3180, B471)
        # | | | ['检测中，请等待Button', 'Button', 'Button0', 'Button1']
        # | | | child_window(auto_id="FormMain.openGLWidget.CProgress.widgetTitle.pbPopClose", control_type="Button")
        # | |
        # | | Progress - ''(L2590, T514, R3170, B530)
        # | | ['Progress', '检测中，请等待Progress']
        # | | child_window(auto_id="FormMain.openGLWidget.CProgress.progressBar", control_type="ProgressBar")
        # | |
        # | | Static - '已用时：00:00:03'(L2590, T540, R3170, B562)
        # | | ['已用时：00:00:03', '已用时：00:00:03Static', 'Static2']
        # | | child_window(title="已用时：00:00:03", auto_id="FormMain.openGLWidget.CProgress.labelProcessTime",
        #                  control_type="Text")
        # | |
        # | | CheckBox - '取消'(L3050, T572, R3170, B612)
        # | | ['取消', 'CheckBox', '取消CheckBox', 'CheckBox0', 'CheckBox1']
        # | | child_window(title="取消", auto_id="FormMain.openGLWidget.CProgress.pbCancel", control_type="CheckBox")

    #关闭修复弹框
    def close_repair(self):
        close_button = self.repair_parent().children()[0].children()[1]
        self.click(control=close_button)

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
