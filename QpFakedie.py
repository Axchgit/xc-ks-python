
from PyQt5.QtWidgets import QApplication, QProgressBar, QPushButton
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
import time
from threading import  Thread
from PyQt5.QtCore import pyqtSignal,QObject

# 信号库
class SignalStore(QObject):
    # 定义一种信号
    progress_update = pyqtSignal(int)
    # 还可以定义其他作用的信号

# 实例化
so = SignalStore()

class ProgressBar(QtWidgets.QWidget):
    def __init__(self, parent= None):
        QtWidgets.QWidget.__init__(self)
        
        #信号和slot函数绑定
        so.progress_update.connect(self.setProgress)
        
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('ProgressBar')
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)
        self.pbar.setRange(0, 100)
        self.pbar.setValue(0)
        
        self.button = QPushButton('Start', self)
        self.button.setFocusPolicy(Qt.NoFocus)
        self.button.move(40, 80)
        
        self.button.clicked.connect(self.handleCalc)

    def handleCalc(self):
        def pbar_change():
            for i in range(100):
                time.sleep(0.2)
                so.progress_update.emit(i+1)
        worker = Thread(target=pbar_change)
        worker.start()
    # 处理进度的slot函数
    def setProgress(self,value):
        self.pbar.setValue(value)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    qb = ProgressBar()
    qb.show()
    sys.exit(app.exec_())
