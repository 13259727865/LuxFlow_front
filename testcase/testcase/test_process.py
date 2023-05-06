#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @author:Gemini
# @time:  2022/1/13:15:29
# @email: 13259727865@163.com
import os
from datetime import datetime

import allure
import pytest


class TestProcess:

    support_parameter = {"抬升高度": 10, "支撑点直径": 1.5, "支撑头长度": 2.5, "支撑柱直径": 1.5, "支撑点间距": 4.5, "临界角": 75,
                         "是否加固": True, "起始高度": 1.5, "角度": 50, "支撑加底座": True, "底座高度": 1.5}

    # 用例参数
    process_date = {"path": r"E:\model\商务测试档案\正常\batch_1", "model": '"孔洞花瓶.stl" "谢牙龈.stl"', "opentext": "本地打开",
                    "support_parameter": support_parameter, "copy_num": 3, "spacing": 5, "layout_mode": 2,
                    "thickness_type": "自定义"}
    path = process_date["path"]+r"\save"
    ids = ["全流程测试"]

    @allure.story("全流程测试")
    @pytest.mark.parametrize("process_date", [process_date], ids=ids)
    def test_openpart(self, start_flow, process_date):
        Path = 'E:\\model\\auto_test\\'
        for i in os.listdir(Path):

            filepath = Path + i + '\\'
            with allure.step("打开零件"):
                start_flow.jump_button(oper="open")
                start_flow.all_model(delet=True)
                start_flow.openfile(filepath)
                # openfile = start_flow.openfile(process_date["path"], process_date["model"])
                # pytest.assume(openfile == process_date["opentext"])
                # start_flow.modle_check_tips(oper="上传修复")
                start_flow.wait(auto_id="FormMain.splitter.partListUi", control_type="Group")
                # pytest.assume(len(start_flow.get_modle_list()) == len(process_date["model"].split(" ")))
                start_flow.capture_image("open_model")
            with allure.step("添加辅助支撑、整齐布局"):
                orientation = start_flow.auxiliary_support(all=True)
                orientation=start_flow.toolWidgte_button(409)
                orientation.orientation(0)
                orientation.add()
                orientation.layout()
                orientation.close()
            with allure.step("切片"):
                start_flow.jump_button(oper="slice")
                slice = start_flow.slice()
            with allure.step("导出切片"):
                filename = datetime.now().strftime('%Y%m%d')
                os.chdir(filepath)
                if (filename in os.listdir()) is False:
                    print(filename in os.listdir())
                    os.mkdir(filename)
                slice.save_file(filename="test001", path=filepath+filename)
                slice.save_frame()
