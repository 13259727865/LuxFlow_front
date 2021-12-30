#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @author:Gemini
# @time:  2021/11/23:17:33
# @email: 13259727865@163.com
import json


class JsonIO:

    # 读取json文件内容
    def read_json(self, filename=r"E:\LuxFlow_front\config.json"):
        # json.load(open(file=r"E:\LuxFlow_front\config.json",encoding="utf-8"))
        with open(file=filename, encoding="utf-8") as f:
            return json.load(f)

