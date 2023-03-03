#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @author:Gemini
# @time:  2022/3/25:13:49
# @email: 13259727865@163.com
import allure
import pytest


class TestSupport:


    #进入支撑页
    support_date = {"application":["齿科产品","鞋类产品","眼镜产品","其他产品"],"support_save_name":"test001"}
    allure.story("支撑页用例")
    pytest.mark.parametrize("support_date",[support_date])
    def test_into_support(self,start_flow,support_date):
        with allure.step("进入支撑页"):
            support = start_flow.jump_button(oper="支撑")
            pytest.assume(support.support_parent() is not False)
            start_flow.capture_image("进入支撑页")
        with allure.step("下拉列表展示：齿科产品、鞋类产品、眼镜产品、其他产品"):
            texts = support.return_all_texts(open=False)
            pytest.assume(texts["support3"] == support_date["application"])
        with allure.step("点击【保存】图标按钮"):
            assert support_date["support_save_name"] not in texts["support3"]
            save = support.support_set_button(oper="保存")
            save.save_frame_value(support_date["support_save_name"])
            start_flow.capture_image("保存弹框")
            save.save_button()
            pytest.assume(support_date["support_save_name"] in texts["support3"])

