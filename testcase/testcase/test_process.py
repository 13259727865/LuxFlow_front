#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @author:Gemini
# @time:  2021/11/23:13:59
# @email: 13259727865@163.com


import time
import allure


# @pytest.fixture(scope='module')
# def setup_module(self):
#     self.main = MainPage()


@allure.feature("测试类")
class TestOpen:
    #     # def teardown(self):
    #     #     self.main.main_quit()

    # 打开零件
    @allure.story("打开零件")
    def test_openpart(self, start_flow):
        with allure.step("打开零件"):
            start_flow.jump_button(oper="打开")
            openfile = start_flow.openfile(r"E:\model\model", '"孔洞花瓶.stl" "heart.stl"')
            assert openfile == "本地打开"
            start_flow.modle_check_tips(oper="上传修复")
            start_flow.wait(auto_id="FormMain.leftWidget.FormPartList.listModels", control_type="List")
            time.sleep(3)
            assert len(start_flow.modle_list()[2]) == 2

    # 支撑应用选择
    @allure.story("支撑应用选择")
    def test_support(self, start_flow):
        with allure.step("选择应用"):
            support = start_flow.jump_button(oper="支撑")
            support.choice_application(click_index=2)
            assert support.return_all_texts()["support3"][2] == "眼镜产品"
