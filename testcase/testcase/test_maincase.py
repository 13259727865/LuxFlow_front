#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @author:Gemini
# @time:  2022/3/3:15:56
# @email: 13259727865@163.com
import allure
import pytest
from pywinauto.keyboard import send_keys


class TestOpenModel:

    #测试参数

    model_info0 = {'长:': '43.64 mm', '宽:': '22.82 mm', '高:': '100.00 mm', '体积:': '19.19 ml', '面积:': '996.04 mm²'}
    model_info1 = {'长:': '21.99 mm', '宽:': '10.00 mm', '高:': '22.00 mm', '体积:': '2.52 ml', '面积:': '219.92 mm²'}
    open_model_data0={"path":r"E:\model\model","model": "孔洞花瓶.stl","check_model":"忽略","click_model":1,"model_info":model_info0}
    open_model_data1 = {"path": r"E:\model\model", "model": '"heart.stl" "22.STL" "耳机.stx" "立方体.stl" "眼镜.stl" "通用手机支架.stl" "十字.stl"',
                        "check_model": "上传修复","click_model":3,"model_info":model_info1}

    ids = ["打开模型0","打开模型1"]
    @allure.story("本地上传模型展示")
    @pytest.mark.parametrize("open_model_data",[open_model_data0,open_model_data1],ids=ids)
    #打开零件
    def test_open_model(self,start_flow,open_model_data):
        start_flow.capture_image(img_doc="进入LuxFlow")
        start_flow.openfile(path=open_model_data["path"],model=open_model_data["model"])
        start_flow.modle_check_tips(oper=open_model_data["check_model"])
        with allure.step("查看零件列表与零件信息弹框会自动弹出"):
            start_flow.capture_image(img_doc="导入模型")
            pytest.assume(len(start_flow.get_modle_list()) == len(open_model_data["model"].split(" ")))
        with allure.step("查看零件被选中"):
            start_flow.click_modle(open_model_data["click_model"])
            start_flow.capture_image(img_doc="选中模型")
        with allure.step("验证模型参数"):
            start_flow.capture_image("模型参数")
            pytest.assume(start_flow.model_info()['零件信息'] == open_model_data["model_info"])
        with allure.step("删除选中模型"):
            start_flow.del_model(dele=open_model_data["click_model"])
            start_flow.capture_image(img_doc="删除模型")
            print(len(start_flow.get_modle_list()),len(open_model_data["model"].split(" "))-1)
            pytest.assume(len(start_flow.get_modle_list()) == len(open_model_data["model"].split(" "))-1)

        #清理数据
        start_flow.del_model()


#选择设备
class TestTerminal:
    #用例参数
    terminal_data1={"terminal_code":1,"membrane_code":1,"terminal_oper":"cofirm"}
    terminal_data2 = {"terminal_code": 8, "membrane_code": 2,"terminal_oper":"cancel"}
    @allure.story("设备选择")
    @pytest.mark.parametrize("terminal_data",[terminal_data1,terminal_data2],)
    #选择设备
    def test_terminal_choice(self,start_flow,terminal_data):
        terminal_choice=start_flow.terminal()
        terminal_choice.choice_terminal(terminal_code=terminal_data["terminal_code"])
        terminal_choice.choice_membrane(membrane_code=terminal_data["membrane_code"])
        terminal_choice.confirm_cancel(oper=terminal_data["terminal_oper"])
        start_flow.capture_image(img_doc="选择设备")


#检测修复
class TestRepir:
    @allure.story("鼠标悬浮修复按钮")
    def test_check_suspension(self,start_flow):
        start_flow.mouse_suspension(start_flow.repair_button())
        start_flow.capture_image("鼠标悬浮修复按钮")


    repir_data={"texts":"请导入模型。"}
    @allure.story("模型检测修复-未导入模型")
    @pytest.mark.parametrize("check_data",[repir_data])
    def test_noopen_modle(self,start_flow,check_data):
        # print(start_flow.click_repair().no_modle())
        tips = start_flow.click_repair()
        pytest.assume(tips.no_modle() == check_data["texts"])
        start_flow.capture_image("未导入模型")
        tips.no_modle()


    repir_nochoice_data = {"path":r"E:\model\model","model": '"孔洞花瓶.stl" "孔洞花瓶.stl"',"check_model":"忽略","texts": "请选择模型。"}
    @allure.story("模型检测修复-多模型未选择模型")
    @pytest.mark.parametrize("check_data", [repir_nochoice_data])
    def test_nochoice_modle(self,start_flow,check_data):
        start_flow.capture_image(img_doc="进入LuxFlow")
        start_flow.openfile(path=check_data["path"], model=check_data["model"])
        start_flow.modle_check_tips(oper=check_data["check_model"])
        tips = start_flow.click_repair()
        pytest.assume(tips.no_modle() == check_data["texts"])
        start_flow.capture_image("未选择模型")
        tips.tips_ok()
        start_flow.del_model()


    modle_testing_result = {'坏边': '50', '孔洞': '7', '壳体': '1', '反向三角面片': '-', '相交三角面片': '-'}
    repir_single_data = {"path": r"E:\model\model", "model": "孔洞花瓶.stl", "check_model": "忽略", "texts": "请选择模型。","repair_result":modle_testing_result}
    @allure.story("模型检测修复-单模型未选择模型")
    @pytest.mark.parametrize("check_data", [repir_single_data])
    def test_single_modle(self,start_flow,check_data):
        start_flow.capture_image(img_doc="进入LuxFlow")
        start_flow.openfile(path=check_data["path"], model=check_data["model"])
        start_flow.modle_check_tips(oper=check_data["check_model"])
        repair = start_flow.click_repair()
        repair.testing_button()
        result = repair.testing_result()
        pytest.assume(result == check_data["repair_result"])
        start_flow.capture_image(f"{check_data['model']}检测结果")
        start_flow.del_model()


    modle_testing_result = {'坏边': '50', '孔洞': '7', '壳体': '1', '反向三角面片': '-', '相交三角面片': '-'}
    repir_single_data = {"path": r"E:\model\model", "model": "孔洞花瓶.stl", "check_model": "忽略", "texts": "请选择模型。",
                         "repair_result": modle_testing_result}
    @allure.story("模型检测修复-多模型选择后检测")
    @pytest.mark.parametrize("check_data", [repir_single_data])
    def test_single_modle(self, start_flow, check_data):
        start_flow.capture_image(img_doc="进入LuxFlow")
        start_flow.openfile(path=check_data["path"], model=check_data["model"])
        start_flow.modle_check_tips(oper=check_data["check_model"])
        start_flow.choice_model()
        repair = start_flow.click_repair()
        repair.testing_button()
        result = repair.testing_result()
        pytest.assume(result == check_data["repair_result"])
        start_flow.capture_image(f"{check_data['model']}检测结果")
        start_flow.del_model()









