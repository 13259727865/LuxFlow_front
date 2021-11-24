#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @author:Gemini
# @time:  2021/11/10:10:00
# @email: 13259727865@163.com
from flow_page.main_page import MainPage
import pytest

class TestSet:
    def setup(self):
        self.main = MainPage()

    def test_set(self):
        self.main.set_menu().set_language()
        print(self.main.is_english()[0])


