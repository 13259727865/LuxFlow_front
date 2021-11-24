#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @author:Gemini
# @time:  2021/11/9:11:00
# @email: 13259727865@163.com
import pywinauto
from pywinauto.keyboard import send_keys

from base.main import Main
from flow_page.batch import Batch
from flow_page.marking import Marking
from flow_page.material_frame import MaterialFrame
from flow_page.set_frame import FrameSet
from flow_page.slice import Slice
from flow_page.support import Support
from flow_page.terminal_frame import TerminalFrame



class MainPage(Main):

    _page_path = r"D:\Program Files(x86)\Luxflows\LuxFlow1103\dev\LuxFlow\LuxFlow.exe"


    # 零件破损检测提示
    def modle_check_tips(self, oper="忽略"):
        """
        :param oper: "上传修复""切片修复""忽略""取消""切片"
        :return:
        """
        auto_id = ["FormMain.openGLWidget.FormFixQuery.widgetList",
                   "FormMain.rightwidget.stackedWidget.FormPrintSetting.FormVDSliceQuery.widgetList"]
        try:

            for i in range(len(auto_id)):
                tips = self.find(auto_id=auto_id[i], control_type="Group")
                if tips != False:
                    print(f"找到{auto_id[i]}")
                    if oper == "上传修复":
                        self.click(index="修复")
                    elif oper == "切片修复":
                        self.click(index="修复")
                        self.click(index="切片")
                    elif oper == "忽略":
                        self.click(index="忽略")
                    elif oper == "取消":
                        self.click(index="取消")
                    elif oper == "切片":
                        self.click(index="切片")
                    return
                else:
                    print(f"未找到{auto_id[i]}")
        except Exception as e:
            print("报错处理", e)



    # 设置菜单-打开设置弹框
    def menu_set(self):
        self.click(title="设置", control_type="MenuItem")
        self.click(title="设置", control_type="MenuItem", auto_id="FormMain.widgetTitle.wMenuBar.actionSetting")
        self._dlg.print_control_identifiers()

        return FrameSet(self._dlg)

    # 菜单栏选择设备-打开弹框
    def terminal(self):
        # 设备图标
        terminal_lcon = self.find(auto_id="FormMain.toolWidgte.labelDevice", control_type="Text")
        default_terminal = \
            self.find(auto_id="FormMain.toolWidgte.pbDevice", control_type="CheckBox", isall=False).texts()[0]
        self.click(auto_id="FormMain.toolWidgte.pbDevice", isall=False)
        self._dlg.print_control_identifiers()

        return terminal_lcon, default_terminal, TerminalFrame(self._dlg)

    def material(self):
        # 材料图标
        material_lcon = self.find(auto_id="FormMain.toolWidgte.labeMaterial", control_type="Text")
        default_material = \
            self.find(auto_id="FormMain.toolWidgte.pbMaterial", control_type="CheckBox", isall=False).texts()[0]
        self.click(auto_id="FormMain.toolWidgte.pbMaterial", control_type="CheckBox", isall=False)

        return material_lcon, default_material, MaterialFrame(self._dlg)

    # 本地打开
    def openfile(self, path, model):
        """
        :param path: 模型路径
        :param model: 模型名称，多模型例 '"格子收纳盒.stl""heart.stl"'
        :return: 按钮文本
        """
        openfile_text = self.find(title="本地打开", auto_id="FormMain.rightwidget.stackedWidget.FormLoad.pbLocal",
                                  control_type="Button").texts()[0]
        self.click(title="本地打开", auto_id="FormMain.rightwidget.stackedWidget.FormLoad.pbLocal", control_type="Button")
        # win = pywinauto.Desktop()
        # win["打开文件"].print_control_identifiers()
        openfile = self.win_desktop("打开文件")
        openfile["Toolbar3"].click()
        send_keys(path)
        send_keys("{VK_RETURN}")
        filename = self.win_desktop("打开文件").child_window(class_name="Edit")
        filename.click()
        send_keys(model)
        self.win_desktop("打开文件").child_window(title="打开(&O)", class_name="Button").click()

        return openfile_text

    #保存文件
    def save_file(self,save_path,save_name):
        self.click(auto_id="FormMain.toolWidgte.pbTSave", control_type="Button")
        savefile = self.win_desktop("保存文件")
        savefile["Toolbar4"].click()
        send_keys(save_path)
        send_keys("{VK_RETURN}")
        savefile.child_window(class_name="Edit").click()
        send_keys(save_name)
        savefile.child_window(class_name="Button").click()
        save_result = self.find(auto_id="FormMain.openGLWidget.MyMessageBox.labelMessageText", control_type="Text",isall=False,text=True)
        self.click(title="好的", auto_id="FormMain.openGLWidget.MyMessageBox.pbConfirm", control_type="CheckBox")
        return save_result


    # 模型列表
    def modle_list(self):
        """
        :return: 列表lcon，列表名称，列表内容列表
        """
        self._dlg.print_control_identifiers()
        modle_list_lcon = self.find(auto_id="FormMain.leftWidget.FormPartList.label", control_type="Text")
        modle_list_text = \
            self.find(auto_id="FormMain.leftWidget.FormPartList.labelModelList", control_type="Text",
                      isall=True).texts()[0]
        modle_list = self.find(auto_id="FormMain.leftWidget.FormPartList.listModels", control_type="List").children()

        return modle_list_lcon, modle_list_text, modle_list

    # 选中模型的模型参数
    def model_info(self):
        """
        :return:字典--名称、参数
        """
        model_info_dict = {}
        model_info_dict["modle_info_lcon"] = self.find(
            auto_id="FormMain.leftWidget.FormPartList.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents.label_2",
            control_type="Text")
        model_info_dict["modle_info_text"] = self.find(
            auto_id="FormMain.leftWidget.FormPartList.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents.labelPartInfo",
            control_type="Text", isall=False, text=True)
        model_info_dict["modle_length_text"] = self.find(
            auto_id="FormMain.leftWidget.FormPartList.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents.labelLenth",
            control_type="Text", isall=False, text=True)
        model_info_dict["modle_length"] = self.find(
            auto_id="FormMain.leftWidget.FormPartList.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents.lengthInfo",
            control_type="Text", isall=False, text=True)
        model_info_dict["modle_width_text"] = self.find(
            auto_id="FormMain.leftWidget.FormPartList.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents.lengthInfo",
            control_type="Text", isall=False, text=True)
        model_info_dict["modle_width"] = self.find(
            auto_id="FormMain.leftWidget.FormPartList.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents.lengthInfo",
            control_type="Text", isall=False, text=True)
        model_info_dict["modle_height_text"] = self.find(
            auto_id="FormMain.leftWidget.FormPartList.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents.labelWidth",
            control_type="Text", isall=False, text=True)
        model_info_dict["modle_height"] = self.find(
            auto_id="FormMain.leftWidget.FormPartList.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents.widthInfo",
            control_type="Text", isall=False, text=True)
        model_info_dict["modle_volume_text"] = self.find(
            auto_id="FormMain.leftWidget.FormPartList.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents.labelHeight",
            control_type="Text", isall=False, text=True)
        model_info_dict["modle_volume"] = self.find(
            auto_id="FormMain.leftWidget.FormPartList.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents.heightInfo",
            control_type="Text", isall=False, text=True)
        model_info_dict["modle_area_text"] = self.find(
            auto_id="FormMain.leftWidget.FormPartList.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents.labelArea",
            control_type="Text", isall=False, text=True)
        model_info_dict["modle_area"] = self.find(
            auto_id="FormMain.leftWidget.FormPartList.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents.areaInfo",
            control_type="Text", isall=False, text=True)
        return model_info_dict


    # 按钮下一步
    def next_step(self):
        """
        :return: 下一页控件类
        """
        self.click(title="下一步", auto_id="FormMain.nextStepWidget.pbNextStep", control_type="Button")
        return Support(self._dlg)


    # 退出Luxflow
    def main_quit(self, oper='不保存'):
        """
        :param oper: '取消''不保存''保存'
        :return:
        """
        self.click(title="关闭", control_type="Button")
        if self.find(auto_id="FormMain.FormSaveModel.widgetTitle", control_type="Group"):
            self.click(index=oper)



    #下方跳转按钮
    def jump_button(self,oper="切片"):
        if oper == "切片":
            #打开
            self.click(auto_id="FormMain.openGLWidget.FormWizard.buttonWidget.pbLoad.pushButton", control_type="CheckBox")
        elif oper == "支撑":
            #支撑
            self.click(auto_id="FormMain.openGLWidget.FormWizard.buttonWidget.pbSupport.pushButton", control_type="CheckBox")
            return Support(self._dlg)
        elif oper == "布局":
            #布局
            self.click(auto_id="FormMain.openGLWidget.FormWizard.buttonWidget.pbLayout.pushButton", control_type="CheckBox")
            return Batch(self._dlg)
        elif oper == "编码":
            #编码
            self.click(auto_id="FormMain.openGLWidget.FormWizard.buttonWidget.pbCoding.pushButton", control_type="CheckBox")
            return Marking(self._dlg)
        elif oper == "切片":
            #切片
            self.click(auto_id="FormMain.openGLWidget.FormWizard.buttonWidget.pbPrintSet.pushButton", control_type="CheckBox")
            return Slice(self._dlg)
        else:
            print("oper有误！！")


    def print_dlg(self):
        self._dlg.print_control_identifiers()
        # self.win_desktop("Dialog").print_control_identifiers()

if __name__ == '__main__':
    a = MainPage()
    # a.openfile("E:\model\model","20211116.stx")
    a.print_dlg()
    # a.save_file()
