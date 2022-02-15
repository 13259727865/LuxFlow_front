#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @author:Gemini
# @time:  2021/12/27:14:01
# @email: 13259727865@163.com
import pytest

from common.logger import LogRoot
from flow_page.main_page import MainPage


@pytest.fixture(scope='session', autouse=True)
def start_flow():
    LogRoot.info("打开（连接）LuxFlow，开始执行测试用例！！！")
    main = MainPage()
    yield main
    LogRoot.info("用例执行完毕，关闭软件！！！")
    main.main_quit()
