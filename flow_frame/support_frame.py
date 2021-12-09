#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @author:Gemini
# @time:  2021/12/6:14:54
# @email: 13259727865@163.com
from pywinauto.keyboard import send_keys

from base.main import Main


class SaveFrame(Main):
    "保存支撑参数弹框内容"

    #关闭弹框
    def close_save_frame(self,):

        self.click(auto_id="FormSupportCfgSaveName.widget.pbPopClose", control_type="Button")
        return "关闭弹框"

    #输入名称
    def save_frame_value(self,value=""):
        self.click(auto_id="FormSupportCfgSaveName.lineEdit", control_type="Edit")
        send_keys(value)

    #保存
    def save_button(self):
        self.click(auto_id="FormSupportCfgSaveName.pushButtonSave", control_type="Button",isall=False)

    #取消
    def cancel_button(self):
        self.click(auto_id="FormSupportCfgSaveName.pushButtonCancel", control_type="Button",isall=False)


