#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @author:Gemini
# @time:  2021/12/22:10:40
# @email: 13259727865@163.com
from base.main import Main
from common.logger import LogRoot


class BatchFrame(Main):

    # 是否有弹框
    def is_frame(self):
        batch_frame = self.find(auto_id="FormMain.openGLWidget.CProgress", isall=False)
        LogRoot.info(f"布局弹框{batch_frame}")
        return batch_frame

    #布局时间
    def batch_times(self):
        self.wait_time(auto_id="FormMain.openGLWidget.CProgress", control_type="Window")
        self.capture_image(img_doc="布局截图")


    #取消布局
    def batch_cancel(self):
        self.click(auto_id="FormMain.openGLWidget.CProgress.pbCancel", control_type="CheckBox",isall=False)
