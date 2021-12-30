#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @author:Gemini
# @time:  2021/11/18:16:23
# @email: 13259727865@163.com
from base.main import Main
import threading


class Marking(Main):
    def a(self):
        pass

    def change_user(self):
        print('这是中断,切换账号')

        t = threading.Timer(3, self.change_user)

        t.start()


if __name__ == '__main__':
    a = Marking()
    a.change_user()
