#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @author:Gemini
# @time:  2021/11/23:18:24
# @email: 13259727865@163.com
from base.main import Main
from common.logger import LogRoot


class Upload(Main):
    #查找上传页父级控件
    def slice_results(self):
        upload_parent = self.find(auto_id="FormMain.rightwidget", control_type="Group")
        return upload_parent