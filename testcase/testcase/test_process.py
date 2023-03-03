#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @author:Gemini
# @time:  2022/1/13:15:29
# @email: 13259727865@163.com


import allure
import pytest


class TestProcess:

    support_parameter = {"抬升高度": 10, "支撑点直径": 1.5, "支撑头长度": 2.5, "支撑柱直径": 1.5, "支撑点间距": 4.5, "临界角": 75,
                         "是否加固": True, "起始高度": 1.5, "角度": 50, "支撑加底座": True, "底座高度": 1.5}

    # 用例参数
    process_date = {"path": r"E:\model\商务测试档案\正常\batch_1", "model": '"孔洞花瓶.stl" "谢牙龈.stl"', "opentext": "本地打开",
                    "support_parameter": support_parameter, "copy_num": 3, "spacing": 5, "layout_mode": 2,
                    "thickness_type": "自定义"}
    ids = ["全流程测试"]

    @allure.story("全流程测试")
    @pytest.mark.parametrize("process_date", [process_date], ids=ids)
    def test_openpart(self, start_flow, process_date):
        with allure.step("打开零件"):
            start_flow.jump_button(oper="打开")
            start_flow.openfile(process_date["path"])
            # openfile = start_flow.openfile(process_date["path"], process_date["model"])
            # pytest.assume(openfile == process_date["opentext"])
            # start_flow.modle_check_tips(oper="上传修复")

            start_flow.wait(auto_id="FormMain.leftWidget.FormPartList.listModels", control_type="List")
            # pytest.assume(len(start_flow.get_modle_list()) == len(process_date["model"].split(" ")))
            start_flow.capture_image("打开零件")

        with allure.step("添加支撑"):
            support = start_flow.jump_button(oper="支撑")
            support.choice_application(click_index=0)
            support.input_parameter(process_date["support_parameter"])
            # 选中列表中第1个模型
            start_flow.click(control=start_flow.click_modle(1))
            support_frame = support.support_oper()
            support_frame.support_time()
        with allure.step("复制零件"):
            copy = start_flow.copy_file()
            copy.copy_num(process_date["copy_num"])
            copy.copy()
            copy.copyFrame_close()
        with allure.step("布局"):
            batch = support.next_step()
            batch.set_spacing(spacing=process_date["spacing"])
            batch.layout_mode(mode=process_date["layout_mode"])
            batch.layout().batch_times()
            slice = start_flow.jump_button()
        with allure.step("切片"):
            slice.choice_thickness_type(type=process_date["thickness_type"])
            pytest.assume(slice.slice().slice_time() is not False)
            # assert slice.slice().slice_time() is not False
