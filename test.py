
# '''
# Description:
# Author: xch
# Date: 2021-12-06 18:50:29
# FilePath: \vue-framed:\wamp64\www\xc-ks-python\test.py
# LastEditTime: 2021-12-06 19:09:38
# LastEditors: xch
# '''
#!/usr/bin/python3
# -*- coding: utf-8 -*-

# """
# Py40.com PyQt5 tutorial 

# In this example, we create a simple
# window in PyQt5.

# author: Jan Bodnar
# website: py40.com 
# last edited: January 2015
# """

import sys
import datetime
import time

# 这里我们提供必要的引用。基本控件位于pyqt5.qtwidgets模块中。
# from PySide2.QtWidgets import QApplication, QWidget


if __name__ == '__main__':
    # 每一pyqt5应用程序必须创建一个应用程序对象。sys.argv参数是一个列表，从命令行输入参数。
    # app = QApplication(sys.argv)
    # # QWidget部件是pyqt5所有用户界面对象的基类。他为QWidget提供默认构造函数。默认构造函数没有父类。
    # w = QWidget()
    # # resize()方法调整窗口的大小。这离是250px宽150px高
    # w.resize(250, 150)
    # # move()方法移动窗口在屏幕上的位置到x = 300，y = 300坐标。
    # w.move(300, 300)
    # # 设置窗口的标题
    # w.setWindowTitle('Simple')

    # 范围时间
    d_time = datetime.datetime.strptime(
        str(datetime.datetime.now().date())+'00:00', '%Y-%m-%d%H:%M')
    d_time1 = datetime.datetime.strptime(
        str(datetime.datetime.now().date())+'7:00', '%Y-%m-%d%H:%M')
    print(d_time)
    print(d_time1)
    struct_time = time.localtime(time.time())
    print(struct_time.tm_hour)
    print(time.localtime(time.time()))
    
     
    # 当前时间
    n_time = datetime.datetime.now()

    # 判断当前时间是否在范围时间内
    if (n_time > d_time and n_time < d_time1):
        print(1)
        pass
    # 显示在屏幕上
    # w.show()

    # 系统exit()方法确保应用程序干净的退出
    # 的exec_()方法有下划线。因为执行是一个Python关键词。因此，exec_()代替
    # sys.exit(app.exec_())
