#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @author:Gemini
# @time:  2021/11/9:11:00
# @email: 13259727865@163.com
from pywinauto.keyboard import send_keys

from base.io import JsonIO
from base.main import Main
from flow_page.batch import Batch
from flow_page.marking import Marking
from flow_frame.material_frame import MaterialFrame
from flow_frame.set_frame import FrameSet
from flow_page.slice import Slice
from flow_page.support import Support
from flow_frame.terminal_frame import TerminalFrame


class MainPage(Main):
    _page_path = JsonIO().read_json()["path"]

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
        set_text = {}
        self.click(title="设置", control_type="MenuItem")
        self.click(title="设置", control_type="MenuItem", auto_id="FormMain.widgetTitle.wMenuBar.actionSetting")
        set_text["title"] = \
            self._dlg.child_window(title="设置", auto_id="FormMain.widgetTitle.FormSoftSetting.widgetTitle.popTitle",
                                   control_type="Text").texts()[0]
        set_text["language"] = \
            self._dlg.child_window(title="语言", auto_id="FormMain.widgetTitle.FormSoftSetting.labelLanguage",
                                   control_type="Text").texts()[0]
        set_text["ipset"] = \
            self._dlg.child_window(title="IP 设置", auto_id="FormMain.widgetTitle.FormSoftSetting.labelIpsetting",
                                   control_type="Text").texts()[0]
        set_text["ipport"] = \
            self._dlg.child_window(title="IP 端口", auto_id="FormMain.widgetTitle.FormSoftSetting.labelPortSetting",
                                   control_type="Text").texts()[0]
        set_text["software"] = \
            self._dlg.child_window(title="软件版本", auto_id="FormMain.widgetTitle.FormSoftSetting.labelSoftware",
                                   control_type="Text").texts()[0]
        set_text["version"] = self._dlg["Static6"].texts()[0]
        return set_text, FrameSet(self._dlg)

    # 菜单栏选择设备-打开弹框
    def terminal(self):
        # 设备图标
        terminal_lcon = self.find(auto_id="FormMain.toolWidgte.labelDevice", control_type="Text")
        default_terminal = \
            self.find(auto_id="FormMain.toolWidgte.pbDevice", control_type="CheckBox", isall=False).texts()[0]
        self.click(auto_id="FormMain.toolWidgte.pbDevice", isall=False)

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
        self.win_desktop(win_title="打开文件",path_bar="Toolbar3",path=path,filename=model)
        # openfile = self.win_desktop("打开文件")
        # openfile["Toolbar3"].click()
        # send_keys(path)
        # send_keys("{VK_RETURN}")
        # filename = self.win_desktop("打开文件").child_window(class_name="Edit")
        # filename.click()
        # send_keys(model)
        # self.win_desktop("打开文件").child_window(title="打开(&O)", class_name="Button").click()

        return openfile_text

    # 保存文件
    def save_file(self, save_path, save_name):
        self.click(auto_id="FormMain.toolWidgte.pbTSave", control_type="Button")
        savefile = self.win_desktop("保存文件")
        savefile["Toolbar4"].click()
        send_keys(save_path)
        send_keys("{VK_RETURN}")
        savefile.child_window(class_name="Edit").click()
        send_keys(save_name)
        # savefile["保存文件Button"].click()
        savefile["Button"].click()
        save_result = self.find(auto_id="FormMain.openGLWidget.MyMessageBox.labelMessageText", control_type="Text",
                                isall=False, text=True)
        self.click(title="好的", auto_id="FormMain.openGLWidget.MyMessageBox.pbConfirm", control_type="CheckBox")
        return save_result

    # 零件列表
    def modle_list(self):
        """
        :return: 列表lcon，列表名称，列表内容列表
        """
        modle_list_lcon = self.find(auto_id="FormMain.leftWidget.FormPartList.label", control_type="Text")
        modle_list_text = self.find(auto_id="FormMain.leftWidget.FormPartList.labelModelList", control_type="Text",
                                    isall=False).texts()[0]
        modle_list = self.find(auto_id="FormMain.leftWidget.FormPartList.listModels", control_type="List").children()

        return modle_list_lcon, modle_list_text, modle_list

    # 选中模型的模型参数
    def model_info(self):
        """
        :return:字典--名称、参数 {'零件信息': {'长:': '43.64 mm', '宽:': '22.82 mm', '高:': '100.00 mm', '体积:': '19.19 ml', '面积:': '996.04 mm²'}}
        """
        model_info_dict = {}
        model_info = self.find(auto_id="FormMain.leftWidget.FormPartList.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents", control_type="Group").children()
        model_info_text = model_info[1].texts()[0]
        model_info_dict[model_info_text]={}
        for i in range(2,len(model_info),2):
            model_info_dict[model_info_text][model_info[i].texts()[0]]=model_info[i+1].texts()[0]
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

    # 下方跳转按钮
    def jump_button(self, oper="切片"):
        button_parent=self.find(auto_id="FormMain.openGLWidget.FormWizard.buttonWidget", control_type="Group").children()
        if oper == "打开":
            # 打开
            self.click(control=button_parent[0])
        elif oper == "支撑":
            # 支撑
            self.click(control=button_parent[2])
            return Support(self._dlg)
        elif oper == "布局":
            # 布局
            self.click(control=button_parent[4])
            return Batch(self._dlg)
        elif oper == "编码":
            # 编码
            self.click(control=button_parent[6])
            return Marking(self._dlg)
        elif oper == "切片":
            # 切片
            self.click(control=button_parent[8])
            return Slice(self._dlg)
        else:
            print("oper有误！！")

    def print_dlg(self):
        # print(type(self._dlg.print_control_identifiers()))
        self._dlg.print_control_identifiers()
        # self._dlg.child_window(auto_id="FormMain.rightwidget.stackedWidget.FormSupports.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents.cbpara", control_type="ComboBox").texts()
        # button = self.find(auto_id="FormMain.rightwidget.stackedWidget.FormSupports.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents.widgetBarBase.pushButtonBase",
        #                  control_type="CheckBox").WrapperObject
        # self._dlg.print_control_identifiers()
        # checkbox = self._dlg.child_window(title="支撑加底座", auto_id="FormMain.rightwidget.stackedWidget.FormSupports.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents.widgetContaintBase.checkBox_SupportBase", control_type="CheckBox")
        # checkbox = self.find(title="支撑加底座", auto_id="FormMain.rightwidget.stackedWidget.FormSupports.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents.widgetContaintBase.checkBox_SupportBase", control_type="CheckBox")
        # return checkbox.get_toggle_state()
        # self.win_desktop("Dialog").print_control_identifiers()
        # a = self.find(
        #     auto_id="FormMain.rightwidget.stackedWidget.FormSupports.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents.cbpara",
        #     control_type="ComboBox") \
        #     .texts()
        # # a = self._dlg.child_window(
        # #     auto_id="FormMain.rightwidget.stackedWidget.FormSupports.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents", control_type="Group").children()[2].texts()
        # return a
        # a = self.find(auto_id="FormMain.rightwidget.stackedWidget.FormSupports.scrollArea.qt_scrollarea_viewport", control_type="Group")
        # b = self.find(auto_id="FormMain.rightwidget.stackedWidget.FormSupports.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents.cbScene", control_type="ComboBox")
        #
        # # print(self.is_in_outside(a,b))
        # # self.click(control=b)
        # # self.find(index="打印参数编辑").print_control_identifiers()
        # # self._dlg["打印参数编辑"].print_control_identifiers()
        # self._dlg.child_window(auto_id="FormMain").print_control_identifiers()
        # a.click_input()
        # # self.click(auto_id=a.children()[0].get_properties()["automation_id"],isall=False)
        # print(a.children()[0].children())
        # print(dir(str))
        # return self.find(auto_id="FormMain.rightwidget.stackedWidget.FormSupports.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents.widgetContaintBasic",isall=False)
        # self._dlg.child_window(auto_id="FormMain.rightwidget.stackedWidget.FormSupports.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents.widgetContaintBasic")
        # self._dlg.print_control_identifiers()
        # self.wait_not(title="Dialog", auto_id="FormMain.openGLWidget.MyMessageBox", control_type="Window")
        # self.read_json()



if __name__ == '__main__':
    a = MainPage()
    # auto_id = "FormMain.rightwidget.stackedWidget.FormSupports.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents.cbScene"
    # control_type = "ComboBox"
    # print(a.model_info())
    # dict = {"抬升高度":0.10,"是否加固":False,"起始高度":0.05,"仅底座":False}
    #
    # b = a.jump_button(oper="支撑").input_parameter(dict)
    # # print(b)
    # a.menu_set()[1].set_language(language="中")
    a.print_dlg()



