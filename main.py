import sys

# 这里我们提供必要的引用。基本控件位于pyqt5.qtwidgets模块中。
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow

import ks
from functools import partial
if __name__ == '__main__':


    # 每一pyqt5应用程序必须创建一个应用程序对象。sys.argv参数是一个列表，从命令行输入参数。
    app = QApplication(sys.argv)
    # QWidget部件是pyqt5所有用户界面对象的基类。他为QWidget提供默认构造函数。默认构造函数没有父类。
    w = QMainWindow()
    ui = ks.Ui_KSUpdate()
    ui.setupUi(w)
    w.show()

    ui.pushButton_stop.clicked.connect(partial(ui.slot1, mes='1231'))

    # ui.pushButton_stop.clicked.connect(ui.text_printf(self, "程序输出内容"))

    # def click_success():
        

    sys.exit(app.exec_())
