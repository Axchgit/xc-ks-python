import sys

# 这里我们提供必要的引用。基本控件位于pyqt5.qtwidgets模块中。
from PySide2.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QStatusBar, QProgressBar
import time
import threading
from threading import Thread
from PySide2.QtCore import Signal, QObject, QFile
from PySide2.QtUiTools import QUiLoader
import json

# from ks import Ui_KSUpdate
import urllib.request
from functools import partial

updateOrderTableUrl = "http://dev.xchtzon.top:8088/index/updateOrderTable"
updateBillTableUrl = "http://dev.xchtzon.top:8088/index/updateBillTable"
updateItemTable = "http://dev.xchtzon.top:8088/index/updateItemTable"

getActivityList = "http://dev.xchtzon.top:8088/index/getAllActivityIdList"


updateBeginTime = 1617120000
updateDayCell = 5

startWork = True
workSleep = 0
# designer.exe地址
# C:\Users\10278\AppData\Local\Programs\Python\Python38\Lib\site-packages\qt5_applications\Qt\bin

# 信号库


class SignalStore(QObject):
    # 定义一种信号
    progress_update = Signal(int)
    text_append = Signal(str)

    # 还可以定义其他作用的信号

# 实例化
so = SignalStore()
# bill_update = UpdateBill()

class MainWindow(QMainWindow):

    def __init__(self):
        # qfile_ks= QFile("ui/ks.ui")
        # qfile_ks.open(QFile.ReadOnly)
        # qfile_ks.close()

        self.ui = QUiLoader().load("ui/ks.ui")
        # super(mainWindow, self).__init__()
        # self.setupUi(self)
        self.ui.pushButton_start.clicked.connect(self.bt_start)
        self.ui.pushButton_stop.clicked.connect(self.bt_stop)
        self.ui.pushButton_update_other.clicked.connect(self.bt_update_other)
        # self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.ui.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)
        # 连接信号到处理的slot函数
        so.progress_update.connect(self.setProgress)
        self.ui.progressBar.setRange(0, 100)

        # self.ui.createStatusBar()
        so.text_append.connect(self.textAppend)

    def bt_start(self):
        global startWork
        startWork = True
        # self.setStatusBar().showMessage('正在更新...')
        self.ui.statusbar.showMessage('正在更新')
        so.text_append.emit('你点击了开始更新按钮')
        if repeat_thread_detection('updateThisMonth'):
            so.text_append.emit('已开启更新,请勿重复开启')
        elif(repeat_thread_detection('updateOtherMonth')):
            so.text_append.emit('正在更新旧数据')
        else:
            # Thread(target=updateThisMonth, name='updateThisMonth').start()
            # Thread(target=updateLastMonth, name='updateLastMonth').start()
            # Thread(target=updateBillThisMonth, name='updateBillThisMonth').start()
            # Thread(target=updateBillLastMonth, name='updateBillLastMonth').start()
            Thread(target=updateActivityList, name='updateActivityList').start()
            
            
    def bt_stop(self):
        global startWork
        startWork = False
        self.ui.statusbar.showMessage('暂停更新...(当前任务结束后暂停)')
        so.text_append.emit('暂停循环更新操作')

    def bt_update_other(self):
        global startWork
        startWork = False
        # self.ui.statusbar.showMessage('正在更新两个月前数据...(五分钟后开始更新,更新结束前请不要进行其他操作)')
        # time.sleep(300)

        # self.setStatusBar().showMessage('正在更新两个月前数据...')
        self.ui.statusbar.showMessage('正在更新两个月前数据(不建议频繁更新,一周一次即可)')
        # so.text_append.emit('你点击了开始更新按钮')
        if not repeat_thread_detection('updateOtherMonth'):
            Thread(target=updateOtherMonth, name='updateOtherMonth').start()
            Thread(target=updateBillOtherMonth, name='updateBillOtherMonth').start()
            
            # Thread(target=updateLastMonth).start()
        else:
            # print('func线程还处于活动状态，请勿启动新的实例')
            so.text_append.emit('已开启更新,请勿重复开启')

    def textAppend(self, value):
        self.ui.textBrowser.append(value)

    def setProgress(self, value):
        self.ui.progressBar.setValue(value)

def updateActivityList():
    global startWork
    if(startWork==False):
        so.text_append.emit('更新循环已停止')
    # global updateDayCell
    allNum = 1
    while startWork:

        num = 1
        activitys = askUrl(getActivityList)['data']
        work_num = len(activitys)
        so.text_append.emit('------------------')
        so.text_append.emit('商品更新循环第'+str(allNum)+'次,本次循环任务查询次数:'+str(work_num))
        for activity in activitys:
            res = activitys = askUrl(updateItemTable+'?activityId='+str(activity))
            speed = num*(100/work_num)
            if(res['code'] == 200):
                so.text_append.emit('正在更新商品表,当前任务进度:'+str(speed)[0:4]+' %')
                # endTime = endTime-(updateDayCell*24*60*60)
            else:
                so.text_append.emit(
                    '当前第%d次商品表更新失败,错误信息:\n%s' %(num, res['msg']))
                so.text_append.emit(
                    '错误原因:\n%s'% res['data'])
            num = num + 1
        allNum = allNum+1
        time.sleep(workSleep)
        
# class UpdateBill:
def updateBillThisMonth():
    global startWork
    if(startWork==False):
        so.text_append.emit('更新循环已停止')
    global updateDayCell
    allNum = 1
    while startWork:
        # so.text_append.emit('账单最近一个月数据更新循环第%d次\n'%allNum)
        num = 1
        endTime = (int(time.time()))
        timeStartFormat = time.localtime(endTime-30*24*60*60)
        timeEndFormat = time.localtime(endTime)
        so.text_append.emit('------------------')
        so.text_append.emit('账单最近一个月数据更新循环第'+str(allNum)+'次,本次循环任务查询范围:\n'+time.strftime(
            "%Y-%m-%d %H:%M:%S", timeStartFormat)+'至'+time.strftime("%Y-%m-%d %H:%M:%S", timeEndFormat))
        # work_num = (endTime-updateBeginTime)/(updateDayCell*24*60*60)
        work_num = 30/updateDayCell

        while num < work_num-3:
            timeStart = str((endTime-updateDayCell*24*60*60)*1000+1)
            speed = int(num*(100/work_num))
            if(speed > 100):
                speed = 100
            # so.text_append.emit('账单近一个月数据更新,当前任务第'+str(num)+'次更新,查询范围:\n'+time.strftime(
            #     "%Y-%m-%d %H:%M:%S", timeStartFormat)+'至'+time.strftime("%Y-%m-%d %H:%M:%S", timeEndFormat))
            so.text_append.emit('账单近一个月数据更新,当前任务第'+str(num)+'次更新')
            res = askUrl(updateBillTableUrl+'?'+'settlementTimeStart=' +
                        timeStart+'&settlementTimeEnd='+str(endTime*1000))
            if(res['code'] == 200):
                so.text_append.emit('账单近一个月数据更新任务进度:' + str(speed)+'%')
            else:
                so.text_append.emit(
                    '账单近一个月数据更新,当前第%d次更新失败,错误信息:\n%s'%(num ,res['msg']))
                so.text_append.emit(
                    '错误原因:\n%s'% res['data'])
            endTime = endTime-(updateDayCell*24*60*60)            
            num = num + 1
        allNum = allNum+1
        time.sleep(workSleep)



def updateBillLastMonth():
    global startWork
    if(startWork==False):
        so.text_append.emit('更新循环已停止')
    global updateDayCell
    allNum = 1
    while startWork:
        # so.text_append.emit('------------------')
        # so.text_append.emit('账单上一个月数据更新循环第%d次\n'%allNum)
        num = 1
        endTime = (int(time.time())-30*24*60*60)
        # endTime = (int(time.time()))
        timeStartFormat = time.localtime(endTime-30*24*60*60)
        timeEndFormat = time.localtime(endTime)
        so.text_append.emit('------------------')
        so.text_append.emit('账单上一个月数据更新循环第'+str(allNum)+'次,本次循环任务查询范围:\n'+time.strftime(
            "%Y-%m-%d %H:%M:%S", timeStartFormat)+'至'+time.strftime("%Y-%m-%d %H:%M:%S", timeEndFormat))
        work_num = 30/updateDayCell
        while num < work_num+1:
            timeStart = str((endTime-updateDayCell*24*60*60)*1000+1)
            speed = int(num*(100/work_num))
            if(speed > 100):
                speed = 100
            timeStartFormat = time.localtime(endTime-updateDayCell*24*60*60)
            timeEndFormat = time.localtime(endTime)
            # so.text_append.emit('账单上一个月数据更新,当前任务第'+str(num)+'次更新,查询范围:\n'+time.strftime(
            #     "%Y-%m-%d %H:%M:%S", timeStartFormat)+'至'+time.strftime("%Y-%m-%d %H:%M:%S", timeEndFormat))
            so.text_append.emit('账单上一个月数据更新,当前任务第'+str(num)+'次更新')
            res = askUrl(updateOrderTableUrl+'?'+'settlementTimeStart=' +
                        timeStart+'&settlementTimeEnd='+str(endTime*1000))
            if(res['code'] == 200):
                so.text_append.emit('账单上一个月数据更新任务进度:' + str(speed)+'%')
                endTime = endTime-(updateDayCell*24*60*60)
            else:
                so.text_append.emit(
                    '账单上一个月数据更新,当前第%d次更新失败,错误信息:\n%s' %(num, res['msg']))
                so.text_append.emit(
                    '错误原因:\n%s'% res['data'])
            num = num + 1
        allNum = allNum+1
        time.sleep(workSleep)
        
def updateBillOtherMonth():
    global startWork
    if(startWork==False):
        so.text_append.emit('更新循环已停止')
    global updateDayCell
    # while startWork:
    num = 1
    endTime = (int(time.time())-2*30*24*60*60)
    work_num = (endTime-updateBeginTime)/(updateDayCell*2*24*60*60)
    # work_num = 30/updateDayCell
    while num < work_num+1:
        timeStart = str((endTime-updateDayCell*2*24*60*60)*1000+1)
        speed = int(num*(100/work_num))
        if(speed > 100):
            speed = 100
        timeStartFormat = time.localtime(endTime-updateDayCell*2*24*60*60)
        timeEndFormat = time.localtime(endTime)
        # so.text_append.emit('账单两个月前数据更新,当前任务第'+str(num)+'次更新,查询范围:\n'+time.strftime(
        #     "%Y-%m-%d %H:%M:%S", timeStartFormat)+'至'+time.strftime("%Y-%m-%d %H:%M:%S", timeEndFormat))
        so.text_append.emit('账单两个月前数据更新,当前任务第'+str(num)+'次更新')
        # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))))
        res = askUrl(updateOrderTableUrl+'?'+'settlementTimeStart=' +
                    timeStart+'&settlementTimeEnd='+str(endTime*1000))
        if(res['code'] == 200):
            # SELECT *  FROM `order` WHERE `order_create_time` BETWEEN '2021-11-12 14:11:16.000000' AND '2021-12-12 14:12:00.000000' ORDER BY `order_create_time`  DESC
            # so.progress_update.emit(speed)
            so.text_append.emit('账单两个月前数据更新任务进度:' + str(speed)+'%')
            endTime = endTime-(updateDayCell*2*24*60*60)
            # time.sleep(60)

        else:
            so.text_append.emit('账单两个月前数据更新,当前第%d次更新失败,错误信息:\n%s' %( num,res['msg']))
            so.text_append.emit(
                '错误原因:\n%s或此日期范围没有数据'% res['data'])
        num = num + 1
    startWork = True

def updateThisMonth():
    global startWork
    if(startWork==False):
        so.text_append.emit('更新循环已停止')
    global updateDayCell
    allNum = 1
    while startWork:
        so.text_append.emit('------------------')
        so.text_append.emit('订单最近一个月数据更新循环第%d次\n'%allNum)
        num = 1
        endTime = (int(time.time()))
                # endTime = (int(time.time())-30*24*60*60)
        # endTime = (int(time.time()))
        timeStartFormat = time.localtime(endTime-30*24*60*60)
        timeEndFormat = time.localtime(endTime)
        so.text_append.emit('------------------')
        so.text_append.emit('账单上一个月数据更新循环第'+str(allNum)+'次,本次循环任务查询范围:\n'+time.strftime(
            "%Y-%m-%d %H:%M:%S", timeStartFormat)+'至'+time.strftime("%Y-%m-%d %H:%M:%S", timeEndFormat))
        # work_num = (endTime-updateBeginTime)/(updateDayCell*24*60*60)
        work_num = 30/updateDayCell
        while num < work_num+1:
            timeStart = str((endTime-updateDayCell*24*60*60)*1000+1)
            speed = int(num*(100/work_num))
            if(speed > 100):
                speed = 100
            timeStartFormat = time.localtime(endTime-updateDayCell*24*60*60)
            timeEndFormat = time.localtime(endTime)
            # so.text_append.emit('订单近一个月数据更新,当前任务第'+str(num)+'次更新,查询范围:\n'+time.strftime(
            #     "%Y-%m-%d %H:%M:%S", timeStartFormat)+'至'+time.strftime("%Y-%m-%d %H:%M:%S", timeEndFormat))
            so.text_append.emit('订单近一个月数据更新,当前任务第'+str(num)+'次更新')
            res = askUrl(updateOrderTableUrl+'?'+'orderCreateTimeStart=' +
                        timeStart+'&orderCreateTimeEnd='+str(endTime*1000))
            if(res['code'] == 200):
                so.progress_update.emit(speed)
                endTime = endTime-(updateDayCell*24*60*60)
            else:
                so.text_append.emit(
                    '订单近一个月数据更新,当前第%d次更新失败,错误信息:\n%s' %( num,res['msg']))
            num = num + 1
        allNum = allNum+1
        time.sleep(workSleep)


def updateLastMonth():
    global startWork
    if(startWork==False):
        so.text_append.emit('更新循环已停止')
    global updateDayCell
    allNum = 1
    while startWork:
        so.text_append.emit('------------------')
        so.text_append.emit('订单上一个月数据更新循环第%d次\n'%allNum)
        num = 1
        endTime = (int(time.time())-30*24*60*60)
        work_num = 30/updateDayCell
        while num < work_num+1:
            timeStart = str((endTime-updateDayCell*24*60*60)*1000+1)
            speed = int(num*(100/work_num))
            if(speed > 100):
                speed = 100
            timeStartFormat = time.localtime(endTime-updateDayCell*24*60*60)
            timeEndFormat = time.localtime(endTime)
            # so.text_append.emit('订单上一个月数据更新,当前任务第'+str(num)+'次更新,查询范围:\n'+time.strftime(
            #     "%Y-%m-%d %H:%M:%S", timeStartFormat)+'至'+time.strftime("%Y-%m-%d %H:%M:%S", timeEndFormat))
            so.text_append.emit('订单上一个月数据更新,当前任务第'+str(num)+'次更新')
            res = askUrl(updateOrderTableUrl+'?'+'orderCreateTimeStart=' +
                        timeStart+'&orderCreateTimeEnd='+str(endTime*1000))
            if(res['code'] == 200):
                so.text_append.emit('订单上一个月数据更新任务进度:' + str(speed)+'%')
                endTime = endTime-(updateDayCell*24*60*60)
            else:
                so.text_append.emit(
                    '订单上一个月数据更新,当前第%d次更新失败,错误信息:\n%s'%( num,res['msg']))
            num = num + 1
        allNum = allNum+1
        time.sleep(workSleep)


def updateOtherMonth():
    global startWork
    if(startWork==False):
        so.text_append.emit('更新循环已停止')
    global updateDayCell
    # while startWork:
    num = 1
    endTime = (int(time.time())-2*30*24*60*60)
    work_num = (endTime-updateBeginTime)/(updateDayCell*2*24*60*60)
    # work_num = 30/updateDayCell
    while num < work_num+1:
        timeStart = str((endTime-updateDayCell*2*24*60*60)*1000+1)
        speed = int(num*(100/work_num))
        if(speed > 100):
            speed = 100
        timeStartFormat = time.localtime(endTime-updateDayCell*2*24*60*60)
        timeEndFormat = time.localtime(endTime)
        # so.text_append.emit('订单两个月前数据更新,当前任务第'+str(num)+'次更新,查询范围:\n'+time.strftime(
        #     "%Y-%m-%d %H:%M:%S", timeStartFormat)+'至'+time.strftime("%Y-%m-%d %H:%M:%S", timeEndFormat))
        so.text_append.emit('订单两个月前数据更新,当前任务第'+str(num)+'次更新')
        # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))))
        res = askUrl(updateOrderTableUrl+'?'+'orderCreateTimeStart=' +
                    timeStart+'&orderCreateTimeEnd='+str(endTime*1000))
        if(res['code'] == 200):
            # SELECT *  FROM `order` WHERE `order_create_time` BETWEEN '2021-11-12 14:11:16.000000' AND '2021-12-12 14:12:00.000000' ORDER BY `order_create_time`  DESC
            # so.progress_update.emit(speed)
            so.text_append.emit('订单两个月前数据更新任务进度:' + str(speed)+'%')
            endTime = endTime-(updateDayCell*2*24*60*60)
            # time.sleep(60)

        else:
            so.text_append.emit('订单两个月前数据更新,当前第%d次更新失败,错误信息:\n%s'%( num,res['msg']))
        num = num + 1
    startWork = True
    # time.sleep(workSleep)


def repeat_thread_detection(tName):
    # 判断 tName线程是否处于活动状态
    for item in threading.enumerate():
        if tName == item.name:  # 如果名字相同，说明tName线程在活动的线程列表里面
            return True
    return False


def askUrl(url):
    head = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37"
    }
    html = ""
    req = urllib.request.Request(url=url, headers=head)
    response = urllib.request.urlopen(req)
    html = json.loads(response.read().decode("utf-8"))

    return html


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # ex = Example()
    w = MainWindow()
    w.ui.show()

    sys.exit(app.exec_())
