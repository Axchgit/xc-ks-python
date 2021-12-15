import sys
import PySide2
import PySide2.QtGui
from PySide2.QtGui import QIcon
import datetime

# dirname = os.path.dirname(PySide2.__file__)
# plugin_path = os.path.join(dirname, 'plugins', 'platforms')
# os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
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

# dirname = os.path.dirname(PySide2.__file__)
# plugin_path = os.path.join(dirname, 'plugins', 'platforms')
# os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
BaseUrl = "http://ks.api.xuechuangwl.com"

# BaseUrl = "http://dev.xchtzon.top:8088"

updateOrderTableUrl = BaseUrl+"/index/updateOrderTable"
updateBillTableUrl = BaseUrl+"/index/updateBillTable"
updateItemTable = BaseUrl+"/index/updateItemTable"

getActivityList = BaseUrl+"/index/getAllActivityIdList"

deleteUpdateTableExcel = BaseUrl+"/index/deleteUpdateTableExcel"


# 引入包缺失错误
# pyinstaller main.py  --hidden-import PySide2.QtGui
# 找不到运行平台错误
# dirname = os.path.dirname(__file__)
# plugin_path = os.path.join(dirname, 'plugins', 'platforms')
# os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
# 打包后运行出现命令行解决，后缀名更改
# pyinstaller -F main.pyw
updateBeginTime = 1617120000
updateDayCell = 4

startWork = False
workSleep = 120
secondWorkSleep = 1800
# designer.exe地址
# C:\Users\10278\AppData\Local\Programs\Python\Python38\Lib\site-packages\qt5_applications\Qt\bin

# 信号库


class SignalStore(QObject):
    # 定义一种信号
    progress_update = Signal(int)
    progress_item_update = Signal(int)
    
    text_append = Signal(str)
    statusbar_show = Signal(str)
    

    # 还可以定义其他作用的信号


# 实例化
so = SignalStore()
# bill_update = UpdateBill()


class MainWindow(QMainWindow):

    def __init__(self):
        # qfile_ks= QFile("ui/ks.ui")
        # qfile_ks.open(QFile.ReadOnly)
        # qfile_ks.close()

        self.ui = QUiLoader().load("ui\ks.ui")
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
        so.progress_item_update.connect(self.setProgressItem)
        self.ui.progressBar_item.setRange(0, 100)
        so.statusbar_show.connect(self.setStatusbar)
        self.ui.statusbar.showMessage('')
        

        # self.ui.createStatusBar()
        so.text_append.connect(self.textAppend)
        self.setIcon()

    def setIcon(self):
        appIcon = QIcon("ui\\xc_logo.png")
        self.ui.setWindowIcon(appIcon)

    def bt_start(self):
        global startWork
        # self.setStatusBar().showMessage('正在更新...')
        # so.text_append.emit('你点击了开始更新按钮')
        if repeat_thread_detection('updateThisMonth'):
            so.text_append.emit('正在更新,请勿重复开启')
        elif(repeat_thread_detection('updateOtherMonth')):
            so.text_append.emit('正在更新旧数据')
        else:
            startWork = True
            self.ui.statusbar.showMessage('正在更新')
            Thread(target=isTimeFrame, name='isTimeFrame').start()
            Thread(target=startUpdateThread, name='startUpdateThread').start()
            # Thread(target=testStartWork, name='testStartWork').start()
            

            # time.sleep(1)

    def bt_stop(self):
        global startWork
        startWork = False
        self.ui.statusbar.showMessage('暂停更新...(当前任务结束后暂停)')
        so.text_append.emit('暂停循环更新操作')

    def bt_update_other(self):
        global startWork
        startWork = False
        self.ui.statusbar.showMessage('正在更新两个月前数据(不建议频繁更新,一周一次即可)')
        # so.text_append.emit('你点击了开始更新按钮')
        if not repeat_thread_detection('updateOtherMonth'):
            # Thread(target=updateOtherMonth, name='updateOtherMonth').start()
            # Thread(target=updateBillOtherMonth,name='updateBillOtherMonth').start()
            # Thread(target=updateOtherActivityList,name='updateOtherActivityList').start()
            Thread(target=startOtherUpdateThread,name='startOtherUpdateThread').start()

        else:
            # print('func线程还处于活动状态，请勿启动新的实例')
            so.text_append.emit('已开启更新,请勿重复开启')

    def textAppend(self, value):
        self.ui.textBrowser.append(value)

    def setProgress(self, value):
        self.ui.progressBar.setValue(value)
        
    def setProgressItem(self, value):
        self.ui.progressBar_item.setValue(value)
        
    def setStatusbar(self, value):
        self.ui.statusbar.showMessage(value)


def startUpdateThread():
    Thread(target=updateThisMonth, name='updateThisMonth').start()
    time.sleep(2)
    Thread(target=updateBillThisMonth, name='updateBillThisMonth').start()
    time.sleep(2)
    Thread(target=updateLastMonth, name='updateLastMonth').start()
    time.sleep(2)
    Thread(target=updateBillLastMonth, name='updateBillLastMonth').start()
    time.sleep(2)
    Thread(target=updateActivityList, name='updateActivityList').start()


def startOtherUpdateThread():
    Thread(target=updateOtherMonth, name='updateOtherMonth').start()
    time.sleep(2)
    Thread(target=updateBillOtherMonth, name='updateBillOtherMonth').start()
    time.sleep(2)
    Thread(target=updateOtherActivityList,name='updateOtherActivityList').start()

# def testStartWork():
#     global startWork
#     while startWork:
#         print(123)
#         time.sleep(3)
        

def isTimeFrame():
    global startWork
    # 范围时间
    thisFunctionStart = True
    while True:
        d_time = datetime.datetime.strptime(
            str(datetime.datetime.now().date())+'00:00', '%Y-%m-%d%H:%M')
        d_time1 = datetime.datetime.strptime(
            str(datetime.datetime.now().date())+'07:00', '%Y-%m-%d%H:%M')
        # 当前时间
        n_time = datetime.datetime.now()
        # print(n_time)
        # 判断当前时间是否在范围时间内
        if (n_time > d_time and n_time < d_time1) and startWork == True:
            # if not repeat_thread_detection('updateOtherMonth'):
            startWork = False
            so.text_append.emit('------------------')            
            so.text_append.emit('不在更新时间范围内,暂停循环更新操作')
            so.statusbar_show.emit('不在更新时间范围内,停止更新')
            time.sleep(0)
            
            Thread(target=deleteUpdateFile, name='deleteUpdateFile').start()
            thisFunctionStart=False

        elif not(n_time > d_time and n_time < d_time1):
            if not repeat_thread_detection('updateOtherMonth') and thisFunctionStart == False:
                startWork = True
                so.text_append.emit('------------------')            
                so.text_append.emit('进入更新时间范围内,开始循环更新操作')
                so.statusbar_show.emit('正在更新')

            # Thread(target=isTimeFrame, name='isTimeFrame').start()
                Thread(target=startUpdateThread, name='startUpdateThread').start()
                thisFunctionStart = True
        time.sleep(60)
        # else:
        #     startWork = True

def deleteUpdateFile():
    global startWork
    # 范围时间
    while True:
        d_time = datetime.datetime.strptime(
            str(datetime.datetime.now().date())+'00:30', '%Y-%m-%d%H:%M')
        d_time1 = datetime.datetime.strptime(
            str(datetime.datetime.now().date())+'00:35', '%Y-%m-%d%H:%M')
        # 当前时间
        n_time = datetime.datetime.now()
        # print(n_time)
        # 判断当前时间是否在范围时间内
        if (n_time > d_time and n_time < d_time1) and startWork == False:
            resOrder = askUrl(deleteUpdateTableExcel+'?file_path=order')
            if(resOrder['code'] == 200):
                so.text_append.emit('------------------')
                so.text_append.emit('删除更新订单缓存文件成功')
            else:
                so.text_append.emit('------------------')
                so.text_append.emit('删除更新订单缓存文件失败')
            resBill = askUrl(deleteUpdateTableExcel+'?file_path=bill')
            if(resBill['code'] == 200):
                so.text_append.emit('------------------')
                so.text_append.emit('删除更新账单缓存文件成功')
            else:
                so.text_append.emit('------------------')
                so.text_append.emit('删除更新账单缓存文件失败')

        time.sleep(280)

def updateActivityList():
    global startWork
    if(startWork == False):
        so.text_append.emit('更新循环已停止')
    # global updateDayCell
    allNum = 1
    while startWork:

        num = 1
        activitys = askUrl(getActivityList)['data']
        work_num = len(activitys)
        so.text_append.emit('------------------')
        so.text_append.emit('商品更新循环第'+str(allNum) +
                            '次,本次循环任务查询次数:'+str(work_num))
        for activity in activitys:
            res = askUrl(updateItemTable+'?activityId='+str(activity))
            speed = num*(100/work_num)
            if(res['code'] == 200):
                so.progress_item_update.emit(speed)
                # so.text_append.emit('正在更新商品表,当前任务进度:'+str(speed)[0:4]+' %')
                # endTime = endTime-(updateDayCell*24*60*60)
            else:
                so.text_append.emit(
                    '当前第%d次商品表更新失败,错误信息:\n%s' % (num, res['msg']))
                so.text_append.emit(
                    '错误原因:\n%s' % res['data'])
            num = num + 1
        allNum = allNum+1
        time.sleep(workSleep)


def updateOtherActivityList():
    global startWork
    if(startWork == False):
        so.text_append.emit('更新循环已停止')
    num = 1
    activitys = askUrl(getActivityList+'?activity_status='+str(4))['data']
    work_num = len(activitys)
    so.text_append.emit('------------------')
    so.text_append.emit('商品旧数据更新循环任务查询次数:'+str(work_num))
    for activity in activitys:
        res = askUrl(updateItemTable+'?activityId='+str(activity))
        speed = num*(100/work_num)
        if(res['code'] == 200):
            so.text_append.emit('正在更新商品旧数据,当前任务进度:'+str(speed)[0:4]+' %')
            # endTime = endTime-(updateDayCell*24*60*60)
        else:
            so.text_append.emit(
                '当前第%d次商品旧数据更新失败,错误信息:\n%s' % (num, res['msg']))
            so.text_append.emit(
                '错误原因:\n%s' % res['data'])
        num = num + 1
        # time.sleep(workSleep)
# class UpdateBill:


def updateBillThisMonth():
    global startWork
    if(startWork == False):
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

        while num < work_num+1:
            timeStart = str((endTime-updateDayCell*24*60*60)*1000+1)
            speed = int(num*(100/work_num))
            if(speed > 100):
                speed = 100
            # so.text_append.emit('账单近一个月数据更新,当前任务第'+str(num)+'次更新,查询范围:\n'+time.strftime(
            #     "%Y-%m-%d %H:%M:%S", timeStartFormat)+'至'+time.strftime("%Y-%m-%d %H:%M:%S", timeEndFormat))
            # so.text_append.emit('账单近一个月数据更新,当前任务第'+str(num)+'次查询')
            res = askUrl(updateBillTableUrl+'?'+'settlementTimeStart=' +
                         timeStart+'&settlementTimeEnd='+str(endTime*1000))
            if(res['code'] == 200):
                so.text_append.emit('账单近一个月数据更新任务进度:' + str(speed)+'%')
            else:
                so.text_append.emit(
                    '账单近一个月数据更新,当前第%d次更新失败,错误信息:\n%s' % (num, res['msg']))
                so.text_append.emit(
                    '错误原因:\n%s' % res['data'])
            endTime = endTime-(updateDayCell*24*60*60)
            num = num + 1
        allNum = allNum+1
        time.sleep(workSleep)


def updateBillLastMonth():
    global startWork
    if(startWork == False):
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
            # so.text_append.emit('账单上一个月数据更新,当前任务第'+str(num)+'次更新')
            res = askUrl(updateBillTableUrl+'?'+'settlementTimeStart=' +
                         timeStart+'&settlementTimeEnd='+str(endTime*1000))
            if(res['code'] == 200):
                so.text_append.emit('账单上一个月数据更新任务进度:' + str(speed)+'%')
                endTime = endTime-(updateDayCell*24*60*60)
            else:
                so.text_append.emit(
                    '账单上一个月数据更新,当前第%d次更新失败,错误信息:\n%s' % (num, res['msg']))
                so.text_append.emit(
                    '错误原因:\n%s' % res['data'])
            num = num + 1
        allNum = allNum+1
        time.sleep(secondWorkSleep)


def updateBillOtherMonth():
    global startWork
    if(startWork == False):
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
        # so.text_append.emit('账单两个月前数据更新,当前任务第'+str(num)+'次更新')
        # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))))
        res = askUrl(updateBillTableUrl+'?'+'settlementTimeStart=' +
                     timeStart+'&settlementTimeEnd='+str(endTime*1000))
        if(res['code'] == 200):
            # SELECT *  FROM `order` WHERE `order_create_time` BETWEEN '2021-11-12 14:11:16.000000' AND '2021-12-12 14:12:00.000000' ORDER BY `order_create_time`  DESC
            # so.progress_update.emit(speed)
            so.text_append.emit('账单两个月前数据更新任务进度:' + str(speed)+'%')
            endTime = endTime-(updateDayCell*2*24*60*60)
            # time.sleep(60)

        else:
            so.text_append.emit(
                '账单两个月前数据更新,当前第%d次更新失败,错误信息:\n%s' % (num, res['msg']))
            so.text_append.emit(
                '错误原因:\n%s或此日期范围没有数据' % res['data'])
        num = num + 1
    startWork = True


def updateThisMonth():
    global startWork
    if(startWork == False):
        so.text_append.emit('更新循环已停止')
    global updateDayCell
    allNum = 1
    while startWork:
        # so.text_append.emit('------------------')
        # so.text_append.emit('订单最近一个月数据更新循环第%d次\n' % allNum)
        num = 1
        so.progress_update.emit(0)        
        endTime = (int(time.time()))
        timeStartFormatThis = time.localtime(endTime-30*24*60*60)
        timeEndFormatThis = time.localtime(endTime)
        so.text_append.emit('------------------')
        so.text_append.emit('订单最近一个月数据更新循环第'+str(allNum)+'次,本次循环任务查询范围:\n'+time.strftime(
            "%Y-%m-%d %H:%M:%S", timeStartFormatThis)+'至'+time.strftime("%Y-%m-%d %H:%M:%S", timeEndFormatThis))
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
            # so.text_append.emit('订单最近一个月数据更新,当前循环第'+str(num)+'次查询')
            res = askUrl(updateOrderTableUrl+'?'+'orderCreateTimeStart=' +
                         timeStart+'&orderCreateTimeEnd='+str(endTime*1000))
            if(res['code'] == 200):
                so.progress_update.emit(speed)
                endTime = endTime-(updateDayCell*24*60*60)
            else:
                so.text_append.emit(
                    '订单最近一个月数据更新,当前第%d次,更新失败,错误信息:\n%s' % (num, res['msg']))
            num = num + 1
        allNum = allNum+1
        time.sleep(workSleep)


def updateLastMonth():
    global startWork
    if(startWork == False):
        so.text_append.emit('更新循环已停止')
    global updateDayCell
    allNum = 1
    while startWork:
        # so.text_append.emit('------------------')
        # so.text_append.emit('订单上一个月数据更新循环第%d次\n' % allNum)
        num = 1
        endTime = (int(time.time())-30*24*60*60)
        timeStartFormatThis = time.localtime(endTime-30*24*60*60)
        timeEndFormatThis = time.localtime(endTime)
        so.text_append.emit('------------------')
        so.text_append.emit('订单上一个月数据更新循环第'+str(num)+'次,本次循环任务查询范围:\n'+time.strftime(
            "%Y-%m-%d %H:%M:%S", timeStartFormatThis)+'至'+time.strftime("%Y-%m-%d %H:%M:%S", timeEndFormatThis))
        work_num = 30/updateDayCell
        while num < work_num+1:
            timeStart = str((endTime-updateDayCell*24*60*60)*1000+1)
            speed = int(num*(100/work_num))
            if(speed > 100):
                speed = 100
            timeStartFormat = time.localtime(endTime-updateDayCell*24*60*60)
            timeEndFormat = time.localtime(endTime)
            # so.text_append.emit('------------------')
            # so.text_append.emit('订单上一个月数据更新,当前任务第'+str(num)+'次更新,查询范围:\n'+time.strftime(
            #     "%Y-%m-%d %H:%M:%S", timeStartFormat)+'至'+time.strftime("%Y-%m-%d %H:%M:%S", timeEndFormat))
            # so.text_append.emit('------------------')
            # so.text_append.emit('订单上一个月数据更新,当前任务第'+str(num)+'次更新')
            res = askUrl(updateOrderTableUrl+'?'+'orderCreateTimeStart=' +
                         timeStart+'&orderCreateTimeEnd='+str(endTime*1000))
            if(res['code'] == 200):
                so.text_append.emit('订单上一个月数据更新任务进度:' + str(speed)+'%')
                endTime = endTime-(updateDayCell*24*60*60)
            else:
                so.text_append.emit(
                    '订单上一个月数据更新,当前第%d次更新失败,错误信息:\n%s' % (num, res['msg']))
            num = num + 1
        allNum = allNum+1
        time.sleep(secondWorkSleep)


def updateOtherMonth():
    global startWork
    if(startWork == False):
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
        # so.text_append.emit('订单两个月前数据更新,当前任务第'+str(num)+'次更新')
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
            so.text_append.emit(
                '订单两个月前数据更新,当前第%d次更新失败,错误信息:\n%s' % (num, res['msg']))
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
