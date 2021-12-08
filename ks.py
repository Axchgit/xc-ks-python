
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ks.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import threading
import time
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_KSUpdate(object):
    def setupUi(self, KSUpdate):
        KSUpdate.setObjectName("KSUpdate")
        KSUpdate.setEnabled(True)
        KSUpdate.resize(720, 480)
        KSUpdate.setMinimumSize(QtCore.QSize(720, 480))
        self.centralwidget = QtWidgets.QWidget(KSUpdate)
        self.centralwidget.setObjectName("centralwidget")
        self.label_message = QtWidgets.QLabel(self.centralwidget)
        self.label_message.setGeometry(QtCore.QRect(50, 25, 111, 20))
        self.label_message.setObjectName("label_message")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(50, 55, 300, 380))
        self.textBrowser.setObjectName("textBrowser")
        self.dateTimeEdit = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.dateTimeEdit.setGeometry(QtCore.QRect(380, 60, 194, 22))
        self.dateTimeEdit.setObjectName("dateTimeEdit")
        self.label_endtime = QtWidgets.QLabel(self.centralwidget)
        self.label_endtime.setGeometry(QtCore.QRect(380, 30, 111, 20))
        self.label_endtime.setObjectName("label_endtime")
        self.label_time = QtWidgets.QLabel(self.centralwidget)
        self.label_time.setGeometry(QtCore.QRect(380, 100, 111, 20))
        self.label_time.setObjectName("label_time")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(380, 130, 69, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("1")
        self.comboBox.addItem("2")
        self.comboBox.addItem("3")
        self.comboBox.addItem("4")
        self.comboBox.addItem("5")
        
        icon = QtGui.QIcon.fromTheme("132")
        self.comboBox.addItem(icon, "")
        self.pushButton_stop = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_stop.setGeometry(QtCore.QRect(380, 410, 75, 23))
        self.pushButton_stop.setObjectName("pushButton_stop")
        self.pushButton_start = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_start.setGeometry(QtCore.QRect(470, 410, 75, 23))
        self.pushButton_start.setObjectName("pushButton_start")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(380, 200, 256, 192))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(3)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        self.label_table = QtWidgets.QLabel(self.centralwidget)
        self.label_table.setGeometry(QtCore.QRect(380, 170, 111, 20))
        self.label_table.setObjectName("label_table")
        KSUpdate.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(KSUpdate)
        self.statusbar.setObjectName("statusbar")
        KSUpdate.setStatusBar(self.statusbar)

        self.retranslateUi(KSUpdate)
        QtCore.QMetaObject.connectSlotsByName(KSUpdate)

    def retranslateUi(self, KSUpdate):
        _translate = QtCore.QCoreApplication.translate
        KSUpdate.setWindowTitle(_translate("KSUpdate", "ks"))
        self.label_message.setText(_translate("KSUpdate", "更新状态信息展示:"))
        self.label_endtime.setText(_translate("KSUpdate", "更新时间截止日期:"))
        self.label_time.setText(_translate("KSUpdate", "更新时间间隔:"))
        self.comboBox.setItemText(0, _translate("KSUpdate", "1天"))
        self.comboBox.setItemText(1, _translate("KSUpdate", "2天"))
        self.comboBox.setItemText(2, _translate("KSUpdate", "5天"))
        self.comboBox.setItemText(3, _translate("KSUpdate", "10天"))
        self.comboBox.setItemText(4, _translate("KSUpdate", "半天"))

        self.pushButton_stop.setText(_translate("KSUpdate", "停止更新"))
        self.pushButton_start.setText(_translate("KSUpdate", "启动更新"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("KSUpdate", "新建行"))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("KSUpdate", "新建行"))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("KSUpdate", "新建行"))
        self.label_table.setText(_translate("KSUpdate", "更新任务列表:"))

    # def slot1(self, mes):
    #     def _slot1(textBrowser, line):

    #         textBrowser.append(mes)  # 文本框逐条添加数据
    #         textBrowser.moveCursor(textBrowser.textCursor().End)  # 文本框显示到底部
    #         time.sleep(0.2)

    #     threading.Thread(target=_slot1, args=(
    #         self.textBrowser, 123)).start()
    def updateBrowser(self, mse):
        try:
            # text = unicode(self.lineedit.text())
            self.textBrowser.append(mse)  # 显示内容支撑html格式语法，eval返回表达式结果
        except:
            self.textBrowser.append(
                "<font color=red>%s is invalid!</font>" % mse)
