#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @author:Gemini
# @time:  2021/12/6:14:54
# @email: 13259727865@163.com
from pywinauto.keyboard import send_keys

from base.main import Main


class SupportFrame(Main):
    "保存支撑参数弹框内容"

    #关闭弹框
    def close_save_frame(self):

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
        elif oper == "导出":
            self.win_desktop(win_title="保存配置文件",path_bar="Toolbar4", path = path,filename=conf,title="保存(&S)", class_name="Button")

    # 刷新和删除弹框提示
    def support_is_frame(self,is_oper=True,isclose=False):
        """
        :param is_oper: True（default） or Flase :是 与 否
        :param close: 是否直接关闭弹框
        :return:
        """
        message=self.find(auto_id="FormMain.rightwidget.stackedWidget.FormSupports.MyMessageBox", control_type="Window",isall=False).children()
        print(message)
        if isclose:
            self.click(auto_id = message[0].children()[1].get_properties()["automation_id"])
            return
        elif is_oper:
            self.click(auto_id=message[4].get_properties()["automation_id"],isall=False)
        elif is_oper == False:
            self.click(control=message[3].get_properties()["automation_id"],isall=False)
        return