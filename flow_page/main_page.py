#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @author:Gemini
# @time:  2021/11/9:11:00
# @email: 13259727865@163.com
import time

from pywinauto import mouse
from pywinauto.keyboard import send_keys

from common.io import JsonIO
from base.main import Main
from common.logger import LogRoot
from flow_frame.main_frame import TerminalFrame, MaterialFrame, FrameSet, CopyFrame, RepairModle
from flow_frame.slice_frame import SliceFrame
from flow_page.batch import Batch
from flow_page.marking import Marking
from flow_page.slice import Slice
from flow_page.support import Support


class MainPage(Main):
    _page_path = JsonIO().read_json()["path"]

    #上排控件父项
    def button_parent(self):
        button_parent=self.find(auto_id="FormMain.toolWidgte", control_type="Group")
        # buttons = button_parent.children()
        return button_parent


    #修复按钮
    def repair_button(self):
        # self._dlg.print_control_identifiers()
        repair_button = self.button_parent().children()[12]
        return repair_button

    #点击修复打开弹框
    def click_repair(self):
        self.click(control=self.repair_button())
        self.wait(title="Form", auto_id="FormMain.openGLWidget.FormVDFix",
                               control_type="Window")
        return RepairModle(self._dlg)


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
                    LogRoot.info("发现检测修复弹框,是否修复")
                    if oper == "上传修复":
                        LogRoot.info("上传修复")
                        self.click(index="修复")
                        self.wait_not(auto_id="FormMain.openGLWidget.CProgress.widgetTitle")
                    elif oper == "切片修复":
                        LogRoot.info("切片修复")
                        self.click(index="修复")
                        self.wait_not(auto_id="FormMain.openGLWidget.CProgress.widgetTitle")
                        self.click(index="切片")
                        return SliceFrame(self._dlg).slice_time()
                    elif oper == "忽略":
                        LogRoot.info("忽略")
                        self.click(index="忽略")
                    elif oper == "取消":
                        LogRoot.info("取消")
                        self.click(index="取消")
                    elif oper == "切片":
                        LogRoot.info("切片")
                        self.click(index="切片")
                        return SliceFrame(self._dlg).slice_time()
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
        # LogRoot.info(f"返回（{set_text}，设置弹框类）")
        return set_text, FrameSet(self._dlg)

    # 菜单栏选择设备-打开弹框
    def terminal(self):
        # 设备图标

        default_terminal = \
            self.find(auto_id="FormMain.toolWidgte.pbDevice", control_type="CheckBox", isall=False).texts()[0]
        self.click(auto_id="FormMain.toolWidgte.pbDevice", isall=False)
        LogRoot.info(f"(默认设备{default_terminal})")
        return TerminalFrame(self._dlg)


    def material(self):
        # 材料图标
        material_lcon = self.find(auto_id="FormMain.toolWidgte.labeMaterial", control_type="Text")
        default_material = \
            self.find(auto_id="FormMain.toolWidgte.pbMaterial", control_type="CheckBox", isall=False).texts()[0]
        self.click(auto_id="FormMain.toolWidgte.pbMaterial", control_type="CheckBox", isall=False)
        LogRoot.info(f"(默认材料{default_material}，材料弹框类)")
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
            LogRoot.info(f"返回保存后提示{save_result}")
            return save_result
        except Exception as e:
            LogRoot.error("报错处理", e)

    # 零件列表
    def get_modle_list(self):
        """
        :return: 列表lcon，列表名称，列表内容列表
        """
        # auto_id = "FormMain.splitter.partListUi.listModels", control_type = "List"
        try:
            modle_parent = self.find(auto_id="FormMain.leftWidget.FormPartList.listModels",
                                     control_type="List")
            modle_list = []
            if len(modle_parent.children())==0:
                LogRoot.error("零件列表为空")
                return modle_list
            # 循环上滚，直到第一个序号为1
            while int(modle_parent.children()[0].texts()[0].split(".")[0]) != 1:
                self.scroll(control=modle_parent, dist=1)
            # 第一页模型列表
            frist_modle_list = modle_parent.children()
            # 第一页模型名称列表

            for i in frist_modle_list:
                modle_list.append(i.texts()[0].split(".", 1)[1])
            if len(frist_modle_list) < 10:
                # 第一页不够十个，直接返回名称列表
                return modle_list
            elif len(frist_modle_list) == 10:
                pagesum = 10
                while True:
                    now_parent = self.find(auto_id="FormMain.leftWidget.FormPartList.listModels",
                                           control_type="List")
                    # 所在页最后一个模型得序号
                    self.scroll(control=modle_parent, dist=-1)
                    page_index = int(now_parent.children()[-1].texts()[0].split(".", 1)[0])
                    now_page_sur = page_index - pagesum
                    if now_page_sur == 0:
                        return modle_list
                    elif now_page_sur < 3:
                        for i in modle_parent.children()[-now_page_sur:]:
                            modle_list.append(i.texts()[0].split(".", 1)[1])
                        return modle_list
                    elif now_page_sur == 3:
                        for i in modle_parent.children()[-now_page_sur:]:
                            modle_list.append(i.texts()[0].split(".", 1)[1])
                        pagesum += 3
        except Exception as e:
            LogRoot.error("报错处理", e)

    # 点击选中列表中得零件
    def click_modle(self, model_code):

        modle_parent = self.find(auto_id="FormMain.leftWidget.FormPartList.listModels",
                                 control_type="List")

        model_list = modle_parent.children()
        if len(model_list) < 10:
            self.click(control=model_list[model_code - 1])
            return
        elif len(model_list) == 10:
            if int(model_list[0].texts()[0].split(".")[0]) <= model_code & int(
                    model_list[-1].texts()[0].split(".")[0]) >= model_code:
                for i in modle_parent.children():
                    if int(i.texts()[0].split(".")[0]) == model_code:
                        self.click(control=i)
                        return

            while True:
                now_frist = int(modle_parent.children()[0].texts()[0].split(".")[0])
                now_end = int(modle_parent.children()[-1].texts()[0].split(".")[0])
                if now_frist > model_code:
                    self.scroll(control=modle_parent, dist=1)
                    scroll_frist = int(modle_parent.children()[0].texts()[0].split(".")[0])
                    if now_frist == scroll_frist:
                        return f"未找到第{model_code}个模型"

                    for i in modle_parent.children()[0:3]:
                        if int(i.texts()[0].split(".")[0]) == model_code:
                            self.click(control=i)
                            return
                elif now_end < model_code:
                    self.scroll(control=modle_parent, dist=-1)
                    scroll_end = int(modle_parent.children()[-1].texts()[0].split(".")[0])
                    if now_end == scroll_end:
                        return f"未找到第{model_code}个模型"
                    for i in modle_parent.children()[-3:]:
                        if int(i.texts()[0].split(".")[0]) == model_code:
                            self.click(control=i)
                            return

    # 复制模型
    def copy_file(self, file_index=0):
        file_list = self.find(auto_id="FormMain.leftWidget.FormPartList.listModels", control_type="List").children()
        print(file_list)
        list_num = len(file_list)
        if list_num == 0:
            LogRoot.error("没有可选零件")
        elif list_num > 0:
            if file_index <= list_num - 1:
                self.click(control=file_list[file_index])
            else:
                LogRoot.error(f"没有第{file_index}个零件")
                return
            self.click(auto_id="FormMain.toolWidgte.pushButtonCopyParts", control_type="Button")
            return CopyFrame(self._dlg)

    # 获取模型参数
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

    # 打开零件
    def openfile(self, path,model="all"):
        """
        :param path: 模型路径
        :param model: 模型名称，多模型例 '"格子收纳盒.stl""heart.stl"'
        :return: 按钮文本
        """
        try:
            openfile_text = self.find(title="本地打开", auto_id="FormMain.rightwidget.stackedWidget.FormLoad.pbLocal",
                                      control_type="Button").texts()[0]
            self.click(title="本地打开", auto_id="FormMain.rightwidget.stackedWidget.FormLoad.pbLocal",
                       control_type="Button")
            LogRoot.info("点击本地打开按钮")
            self.win_desktop(win_title="打开文件", path_bar="Toolbar4", path=path,filename=model)
            self.wait_not(auto_id="FormMain.openGLWidget.CProgress.widgetTitle")
            return openfile_text
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
    def jump_button(self, oper="打开"):
        try:
            button_parent = self.find(auto_id="FormMain.splitter.openGLWidget.FormWizard.buttonWidget",
                                      control_type="Group").children()
            if oper == "打开":
                # 打开
                self.click(control=button_parent[0])
                LogRoot.info("进入打开页")
            elif oper == "支撑":
                # 支撑
                self.click(control=button_parent[2])
                LogRoot.info("进入支撑页")
                return Support(self._dlg)
            # elif oper == "布局":
            #     # 布局
            #     self.click(control=button_parent[4])
            #     LogRoot.info("进入布局页")
            #     return Batch(self._dlg)
            # elif oper == "编码":
            #     # 编码
            #     self.click(control=button_parent[6])
            #     LogRoot.info("进入编码页")
            #     return Marking(self._dlg)
            elif oper == "切片":
                # 切片
                self.click(control=button_parent[4])
                LogRoot.info("进入切片页")
                return Slice(self._dlg)
        except Exception as e:
            LogRoot.error("报错处理,oper有误！", e)

    #选中全部或某个模型
    def choice_model(self,model_sum="all"):
        mate = self.find(auto_id="FormMain.toolWidgte.labeMaterial", isall=False)
        merge = self.find(auto_id="FormMain.leftWidget.FormPartList.pushButtonPartsMarge", isall=False)
        mate_rect = mate.rectangle()
        merge_rect = merge.rectangle()
        click_x = mate_rect.right
        click_y = merge_rect.bottom
        mouse.click(coords=(click_x, click_y))
        if model_sum is "all":
            send_keys("^a")
        elif type(model_sum) is int:
            self.click_modle(model_code=model_sum)
        else:
            LogRoot.error("参数错误")


    #删除模型
    def del_model(self,dele="all"):
        self.choice_model(model_sum=dele)
        send_keys("{DELETE}")



    def print_dlg(self):
        # print(type(self._dlg.print_control_identifiers()))
        self._dlg.print_control_identifiers()
        # self._dlg.capture_as_image().save("./111.png")
        # 材料温度设置
        # self._dlg.child_window(auto_id="FormMain.FormEditParameter").print_control_identifiers()
        # self.click(control=self._dlg.child_window(auto_id="FormMain.openGLWidget.FormDeviceTypeSelection.deviceList", control_type="List").children()[2])

        # self._dlg.child_window(auto_id="FormMain.rightwidget.stackedWidget.FormSupports.scrollArea.
        # qt_scrollarea_viewport.scrollAreaWidgetContents.cbpara", control_type="ComboBox").texts()
        # button = self.find(auto_id="FormMain.rightwidget.stackedWidget.FormSupports.scrollArea.qt_scrollarea_viewport.
        # scrollAreaWidgetContents.widgetBarBase.pushButtonBase",
        # auto_id="FormMain.FormEditParameter.FormSaveModel.widgetTitle.popTitle"


if __name__ == '__main__':
    main = MainPage()
    # a.is_isappear_outside(choice_index=7,outside=a.find(auto_id="FormMain.openGLWidget.FormDeviceTypeSelection.deviceList", control_type="List"))
    # a.capture_image(img_doc="test")
    # dict1 = {"X轴":100,"Y轴":100,"外轮廓":0.2654,"内轮廓":0.2654}
    # support_parameter = {"抬升高度": 10, "支撑点直径": 1.5, "支撑头长度": 2.5, "支撑柱直径": 1.5, "支撑点间距": 4.5, "临界角": 75,
    #                      "是否加固": True, "起始高度": 1.5, "角度": 50, "支撑加底座": True, "底座高度": 1.5}
    # a.jump_button(oper="支撑").input_parameter(support_parameter)
    # main._dlg.print_control_identifiers()
    # main.click(auto_id="FormMain.rightwidget.stackedWidget.FormAnalyseResult.pbParameter",isall=False)
    # main.terminal().choice_membrane1(membrane_code=1)
    # time.sleep(5)
    # print(main.find(index="修复"))
    # print(main.find(title="修复", auto_id="qtooltip_label", control_type="Window"))
    # main.print_dlg()
    # path = r"E:\model\商务测试档案\正常\batch_1"
    # main.openfile(path=path)
    a = main.click(title="项目视图", control_type="List")

    print(a)
