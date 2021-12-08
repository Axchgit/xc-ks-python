import sys

# 这里我们提供必要的引用。基本控件位于pyqt5.qtwidgets模块中。
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton
import time

from ks import Ui_KSUpdate
import urllib.request
from functools import partial

updateOrderTableUrl = "http://ks.api.xuechuangwl.com/index/updateOrderTable"
updateBillTableUrl = "http://ks.api.xuechuangwl.com/test/emojiTest"


updateBeginTime = 1617120000
updateTimeCell = 5


class mainWindow(QMainWindow, Ui_KSUpdate):

    # def __init__(self):
    #     super(Example,self).__init__()
    #     # self.setupUi(self)

    #     self.setupUi(self)

    def __init__(self):
        super(mainWindow, self).__init__()
        self.setupUi(self)
        self.pushButton_start.clicked.connect(self.bt_start)
        self.pushButton_stop.clicked.connect(self.bt_stop)

        self.show()
    # def ps_bt(self):
    #     print('123')
    #     self.textBrowser.clear()

    def bt_start(self):
        self.statusBar().showMessage('正在更新...')
        self.textBrowser.append('开始循环执行更新数据库操作')
        while True:
        # for(i=(int( time.time()));i>updateBeginTime;i = i-(updateTimeCell*24*60*60)):
            i = (int(time.time()))
            while i > updateBeginTime:
                print(i)
                self.textBrowser.append('当前执行进度%s' % i)
                time.sleep(2)
                # time.sleep(2)
                i = i-(updateTimeCell*24*60*60)

    def bt_stop(self):
        self.statusBar().showMessage('停止更新')
        self.textBrowser.append('结束循环更新操作')
    # def buttonClicked(self):

    #     sender = self.sender()
    #     self.statusBar().showMessage(sender.text() + ' was pressed')


# def updateBillTable(Ui_KSUpdate):
    # m = mainWindow()
    # while True:
    #     # for(i=(int( time.time()));i>updateBeginTime;i = i-(updateTimeCell*24*60*60)):
    #     i = (int(time.time()))
    #     while i > updateBeginTime:
    #         print(i)
    #         Ui_KSUpdate.textBrowser.append('当前执行进度%s' % i)
    #         time.sleep(2)
    #         # time.sleep(2)
    #         i = i-(updateTimeCell*24*60*60)


def askUrl(url):
    head = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37"
    }
    html = ""
    req = urllib.request.Request(url=url, headers=head)
    response = urllib.request.urlopen(req)
    html = response.read().decode("utf-8")

    return html


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # ex = Example()
    w = mainWindow()

    sys.exit(app.exec_())
