#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @author:Gemini
# @time:  2022/1/7:15:07
# @email: 13259727865@163.com
from base.main import Main
from common.logger import LogRoot
from flow_page.upload import Upload


class SliceFrame(Main):

    #推荐层厚保存弹框
    def recommended_save(self):
        self.click()


    #自定义层厚保存弹框
    def customized_save(self):
        cust_frame = self.find(auto_id="FormMain.openGLWidget.MyMessageBox", control_type="Window",isall=False)
        return cust_frame

    #自定义弹框title
    def cust_title(self):
        title = self.customized_save().children()[0].children()[0].texts()[0]
        return title

    #自定义弹框关闭
    def cust_close(self):
        close_autoid = self.customized_save().children()[0].children()[1].get_properties()["automation_id"]
        self.click(auto_id=close_autoid,isall=False)

    #自定义弹框提示语
    def cust_texts(self):
        cust_texts = self.customized_save().children()[2].texts()[0]
        return cust_texts

    #自定义弹框”好的“按钮
    def cust_ok(self):
        cust_ok = self.customized_save().children()[3]
        self.click(control=cust_ok)

    #切片进度弹框
    def slise_frame(self):
        slice_frame = self.find(auto_id="FormMain.openGLWidget.CProgress", control_type="Window",isall=False)
        return slice_frame


    #切片进度弹框关闭
    def slice_close(self):
        self.click(control=self.slise_frame().children()[0].children()[1])
        LogRoot.info("点击切片进度条关闭按钮")

    #切片进度取消
    def slice_cancel(self):
        self.click(control=self.slise_frame().children()[3])
        LogRoot.info("点击切片进度条关闭按钮")

    #切片时间计算
    def slice_time(self):
        self.wait_time(auto_id="FormMain.openGLWidget.CProgress", control_type="Window")
        self.capture_image(img_doc="切片后截图")
        LogRoot.info("准备跳转进入上传页")
        return Upload(self._dlg).slice_results()

    def save_file(self,filename,path):
        self.click(auto_id="FormMain.rightwidget.stackedWidget.FormAnalyseResult.pbExportSlice", control_type="Button",isall=False)
        self.win_desktop(win_title="保存", path_bar="Toolbar4",filename=filename, path=path)
        self.wait_not(auto_id="FormMain.splitter.openGLWidget.CProgress.widgetTitle", control_type="Group")

    def save_frame(self):
        ok_button = self.find(auto_id="FormMain.splitter.openGLWidget.MyMessageBox.pbConfirm", control_type="CheckBox",isall=False)
        self.wait(title="保存成功", auto_id="FormMain.splitter.openGLWidget.MyMessageBox.labelMessageText", control_type="Text")
        self.click(ok_button)