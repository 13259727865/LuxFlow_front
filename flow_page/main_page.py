#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @author:Gemini
# @time:  2021/11/9:11:00
# @email: 13259727865@163.com

from common.io import JsonIO
from base.main import Main
from common.logger import LogRoot
from flow_page.batch import Batch
from flow_page.marking import Marking
from flow_frame.material_frame import MaterialFrame
from flow_frame.set_frame import FrameSet
from flow_page.open import Open
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
                if tips is not False:
                    LogRoot.info("发现检测修复弹框,是否修")
                    if oper == "上传修复":
                        LogRoot.info("上传修复")
                        LogRoot.info(f"找到{auto_id[i]}")
                        self.click(index="修复")
                    elif oper == "切片修复":
                        LogRoot.info("切片修复")
                        self.click(index="修复")
                        self.click(index="切片")
                    elif oper == "忽略":
                        LogRoot.info("忽略")
                        self.click(index="忽略")
                    elif oper == "取消":
                        LogRoot.info("取消")
                        self.click(index="取消")
                    elif oper == "切片":
                        LogRoot.info("片")
                        self.click(index="切片")
                    return
                else:
                    LogRoot.info("未发现修复检测弹框，无需修复")
        except Exception as e:
            LogRoot.error("报错处理", e)


    # 设置菜单-打开设置弹框
    def menu_set(self):
        set_text = {}
        self.click(title="设置", control_type="MenuItem")
        self.click(title="设置", control_type="MenuItem", auto_id="FormMain.widgetTitle.wMenuBar.actionSetting")
        set_text["title"] = \
            self.find(title="设置", auto_id="FormMain.widgetTitle.FormSoftSetting.widgetTitle.popTitle",
                      control_type="Text").texts()[0]
        set_text["language"] = \
            self.find(title="语言", auto_id="FormMain.widgetTitle.FormSoftSetting.labelLanguage",
                      control_type="Text").texts()[0]
        set_text["ipset"] = \
            self.find(title="IP 设置", auto_id="FormMain.widgetTitle.FormSoftSetting.labelIpsetting",
                      control_type="Text").texts()[0]
        set_text["ipport"] = \
            self.find(title="IP 端口", auto_id="FormMain.widgetTitle.FormSoftSetting.labelPortSetting",
                      control_type="Text").texts()[0]
        set_text["software"] = \
            self.find(title="软件版本", auto_id="FormMain.widgetTitle.FormSoftSetting.labelSoftware",
                      control_type="Text").texts()[0]
        set_text["version"] = self._dlg["Static6"].texts()[0]
        LogRoot.info(f"返回（{set_text}，设置弹框类）")
        return set_text, FrameSet(self._dlg)

    # 菜单栏选择设备-打开弹框
    def terminal(self):
        # 设备图标
        terminal_lcon = self.find(auto_id="FormMain.toolWidgte.labelDevice", control_type="Text")
        default_terminal = \
            self.find(auto_id="FormMain.toolWidgte.pbDevice", control_type="CheckBox", isall=False).texts()[0]
        self.click(auto_id="FormMain.toolWidgte.pbDevice", isall=False)
        LogRoot.info(f"(设备选择图片，默认设备{default_terminal}，设备弹框类)")
        return terminal_lcon, default_terminal, TerminalFrame(self._dlg)

    def material(self):
        # 材料图标
        material_lcon = self.find(auto_id="FormMain.toolWidgte.labeMaterial", control_type="Text")
        default_material = \
            self.find(auto_id="FormMain.toolWidgte.pbMaterial", control_type="CheckBox", isall=False).texts()[0]
        self.click(auto_id="FormMain.toolWidgte.pbMaterial", control_type="CheckBox", isall=False)
        LogRoot.info(f"(材料选择图片，默认材料{default_material}，材料弹框类)")
        return material_lcon, default_material, MaterialFrame(self._dlg)


    # 保存文件
    def save_file(self, save_path, save_name):
        try:
            self.click(auto_id="FormMain.toolWidgte.pbTSave", control_type="Button")
            LogRoot.info("点击保存按钮")
            self.win_desktop("保存文件", path_bar="Toolbar4", path=save_path, filename=save_name)
            LogRoot.info("操作保存win弹框")
            save_result = self.find(auto_id="FormMain.openGLWidget.MyMessageBox.labelMessageText", control_type="Text",
                                    isall=False, text=True)
            self.click(title="好的", auto_id="FormMain.openGLWidget.MyMessageBox.pbConfirm", control_type="CheckBox")
            LogRoot.info("返回保存成功提示")
            return save_result
        except Exception as e:
            LogRoot.error("报错处理", e)

    # 零件列表
    def modle_list(self):
        """
        :return: 列表lcon，列表名称，列表内容列表
        """
        try:
            modle_list_lcon = self.find(auto_id="FormMain.leftWidget.FormPartList.label", control_type="Text")
            modle_list_text = self.find(auto_id="FormMain.leftWidget.FormPartList.labelModelList", control_type="Text",
                                        isall=False).texts()[0]
            modle_list = self.find(auto_id="FormMain.leftWidget.FormPartList.listModels",
                                   control_type="List").children()
            LogRoot.info(f"返回（零件列表图标，列表text,零件list{modle_list}）")
            return modle_list_lcon, modle_list_text, modle_list
        except Exception as e:
            LogRoot.error("报错处理", e)


    # 选中模型的模型参数
    def model_info(self):
        """
        :return:字典--名称、参数 {'零件信息':
                                {'长:': '43.64 mm', '宽:': '22.82 mm', '高:': '100.00 mm', '体积:': '19.19 ml',
                                '面积:': '996.04 mm²'}
                            }
        """
        try:
            model_info_dict = {}
            model_info = self.find(
                auto_id="FormMain.leftWidget.FormPartList.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents",
                control_type="Group").children()
            model_info_text = model_info[1].texts()[0]
            model_info_dict[model_info_text] = {}
            for i in range(2, len(model_info), 2):
                model_info_dict[model_info_text][model_info[i].texts()[0]] = model_info[i + 1].texts()[0]
            LogRoot.info(f"返回选中零件得信息{model_info_dict}")
            return model_info_dict
        except Exception as e:
            LogRoot.error("报错处理", e)

    # 按钮下一步
    def next_step(self):
        """
        :return: 下一页控件类
        """
        try:
            self.click_next_button()
            LogRoot.info("点击下一步，跳转支撑页")
            # 跳转支撑页
            return Support(self._dlg)
        except Exception as e:
            LogRoot.error("报错处理", e)

    # 退出Luxflow
    def main_quit(self, oper='不保存'):
        """
        :param oper: '取消''不保存''保存'
        :return:
        """
        try:
            self.click(index="关闭")
            LogRoot.info("关闭软件")
            if self.find(auto_id="FormMain.FormSaveModel.widgetTitle", control_type="Group"):
                self.click(index=oper)
                LogRoot.info(f"{oper}")
        except Exception as e:
            LogRoot.error("报错处理", e)


    # 下方跳转按钮
    def jump_button(self, oper="切片"):
        try:
            button_parent = self.find(auto_id="FormMain.openGLWidget.FormWizard.buttonWidget",
                                      control_type="Group").children()
            if oper == "打开":
                # 打开
                self.click(control=button_parent[0])
                LogRoot.info("进入打开页")
            elif oper == "支撑":
                # 支撑
                self.click(control=button_parent[2])
                LogRoot.info("进入打开页")
                return Support(self._dlg)
            elif oper == "布局":
                # 布局
                self.click(control=button_parent[4])
                LogRoot.info("进入布局页")
                return Batch(self._dlg)
            elif oper == "编码":
                # 编码
                self.click(control=button_parent[6])
                LogRoot.info("进入编码页")
                return Marking(self._dlg)
            elif oper == "切片":
                # 切片
                self.click(control=button_parent[8])
                LogRoot.info("进入切片页")
                return Slice(self._dlg)
        except Exception as e:
            LogRoot.error("报错处理,oper有误！", e)



    def print_dlg(self):
        # print(type(self._dlg.print_control_identifiers()))
        self._dlg.print_control_identifiers()
        # self._dlg.child_window(auto_id="FormMain.rightwidget.stackedWidget.FormSupports.scrollArea.
        # qt_scrollarea_viewport.scrollAreaWidgetContents.cbpara", control_type="ComboBox").texts()
        # button = self.find(auto_id="FormMain.rightwidget.stackedWidget.FormSupports.scrollArea.qt_scrollarea_viewport.
        # scrollAreaWidgetContents.widgetBarBase.pushButtonBase",


if __name__ == '__main__':
    a = MainPage()
    # auto_id = "FormMain.rightwidget.stackedWidget.FormSupports.scrollArea.qt_scrollarea_viewport.
    # scrollAreaWidgetContents.cbScene"
    # control_type = "ComboBox"
    # print(a.model_info())
    # dict = {"抬升高度":0.10,"是否加固":True,"起始高度":0.05,"仅底座":False}

    a.print_dlg()
