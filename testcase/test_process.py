#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @author:Gemini
# @time:  2021/11/23:13:59
# @email: 13259727865@163.com


#
from flow_page.main_page import MainPage


class TestProcess:

    def setup_class(self):
        self.main = MainPage()
#
#     # def teardown(self):
#     #     self.main.main_quit()
#
    def test_process(self):
        self.main.openfile("E:\model\model", '"孔洞花瓶.stl" "heart.stl"')
        self.main.modle_check_tips(oper="上传修复")
