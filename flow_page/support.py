#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @author:Gemini
# @time:  2021/11/18:15:56
# @email: 13259727865@163.com
from base.main import Main


class Support(Main):
    def support(self):
        self._dlg.print_control_identifiers()
        print("support")