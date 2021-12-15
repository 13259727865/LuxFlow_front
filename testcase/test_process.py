#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @author:Gemini
# @time:  2021/11/23:13:59
# @email: 13259727865@163.com


#
import time

from pywinauto import application

from flow_page.main_page import MainPage


class TestProcess:

    def setup_class(self):
        self.main = MainPage()
#
#     # def teardown(self):
#     #     self.main.main_quit()
#
    def test_process(self):
        self.main.jump_button(oper="打开")
        print(123)
        assert self.main.openfile("E:\model\model", '"孔洞花瓶.stl" "heart.stl"') == "本地打开"
        self.main.modle_check_tips(oper="上传修复")
        self.main.wait(auto_id="FormMain.leftWidget.FormPartList.listModels", control_type="List")
        time.sleep(3)
        print(46)
        assert len(self.main.modle_list()[2].children())==2

    def test_support(self):
        support = self.main.jump_button(oper="支撑")
        support.choice_application(click_index=2)
        assert support.return_all_parameter()["support3"][2]=="眼镜产品"

