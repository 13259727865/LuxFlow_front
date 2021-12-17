#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @author:Gemini
# @time:  2021/11/9:13:38
# @email: 13259727865@163.com
from pywinauto.keyboard import send_keys

from base.main import Main


class FrameSet(Main):
    """
    设置弹框内控件
    """


    #设置弹框右上角关闭按钮
    def set_close(self):
        self.click(auto_id="FormMain.widgetTitle.FormSoftSetting.widgetTitle.pbPopClose", control_type="Button")

    #语言下拉框选择
    def set_language(self,language):
        """
        :param language: "英""日""中"
        :return: 下拉框内容列表：['En', '日本語', '中']
        """
        self._dlg.print_control_identifiers()

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



    #设置弹框ip输入
    def set_ip(self,ip):
        self.click("IP 设置Edit")
        send_keys("^a")
        send_keys(ip)

    # 设置弹框端口输入
    def set_port(self, port):
        self.click("IP 端口Edit")
        send_keys(port)

     #设置弹框确认按钮
    def set_sure(self):
        self.click(title="Cancel", auto_id="FormMain.widgetTitle.FormSoftSetting.pbCancel", control_type="RadioButton")

    #设置弹框取消按钮
    def set_cancel(self):
        self.click(title="取消", auto_id="FormMain.widgetTitle.FormSoftSetting.pbCancel", control_type="RadioButton")

