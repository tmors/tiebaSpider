# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget.ui'
#
# Created by: PyQt5 UI code generator 5.8
#
# WARNING! All changes made in this file will be lost!
import threading
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QListWidgetItem
import spider
import multiprocessing.queues
import resource_rc
class monitorScannerThread(threading.Thread):
    def __init__(self,totalThreads,widget,dictThread):
        threading.Thread.__init__(self)
        self.threadStop = False
        self.totalThreads = totalThreads
        self.widget = widget
        self.isAllThreadsStopped = False
        self.dictThread = dictThread
    def run(self):
        time.sleep(5)
        while (True):
            curAlivedThread = 0
            for curThread in self.totalThreads:
                if (curThread.isAlive() == True):
                    curAlivedThread += 1
            if (curAlivedThread == 0):
                break
            print("cur alived thread is ", curAlivedThread)
            time.sleep(5)
        self.dictThread.stop()
        for i in spider.dict:
            curUser = spider.dict.get(i)
            str = curUser.toString()
            item = QListWidgetItem(str)
            self.widget.searchResult.addItem(item)

        self.widget.searchResult.show()
        return
    def stop(self):
        self.threadStop = True

class monitorDictThread(threading.Thread):
    def __init__(self,widget):
        threading.Thread.__init__(self)
        self.widget = widget
        self.threadStop = False
    def run(self):
        while (self.threadStop==False):
            self.widget.dictCountOutput.setText(str(spider.dict.__len__()))
            print("monitor dict")
            time.sleep(5)
        return
    def stop(self):
        self.threadStop = True
        return

class Ui_Widget(object):
    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(380, 320)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Widget.sizePolicy().hasHeightForWidth())
        Widget.setSizePolicy(sizePolicy)
        Widget.setMinimumSize(QtCore.QSize(380, 320))
        Widget.setMaximumSize(QtCore.QSize(380, 320))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/tb.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Widget.setWindowIcon(icon)
        self.searchButton = QtWidgets.QPushButton(Widget)
        self.searchButton.setGeometry(QtCore.QRect(250, 10, 101, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.searchButton.setFont(font)
        self.searchButton.setObjectName("searchButton")
        self.formGroupBox = QtWidgets.QGroupBox(Widget)
        self.formGroupBox.setGeometry(QtCore.QRect(30, 10, 201, 91))
        self.formGroupBox.setObjectName("formGroupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.formGroupBox)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.tb_name_show = QtWidgets.QLabel(self.formGroupBox)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.tb_name_show.setFont(font)
        self.tb_name_show.setScaledContents(True)
        self.tb_name_show.setObjectName("tb_name_show")
        self.gridLayout.addWidget(self.tb_name_show, 0, 0, 1, 1)
        self.keywords_input = QtWidgets.QLineEdit(self.formGroupBox)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.keywords_input.setFont(font)
        self.keywords_input.setObjectName("keywords_input")
        self.gridLayout.addWidget(self.keywords_input, 2, 1, 1, 1)
        self.keywords_show = QtWidgets.QLabel(self.formGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.keywords_show.sizePolicy().hasHeightForWidth())
        self.keywords_show.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.keywords_show.setFont(font)
        self.keywords_show.setScaledContents(True)
        self.keywords_show.setObjectName("keywords_show")
        self.gridLayout.addWidget(self.keywords_show, 2, 0, 1, 1)
        self.sex_show = QtWidgets.QLabel(self.formGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sex_show.sizePolicy().hasHeightForWidth())
        self.sex_show.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.sex_show.setFont(font)
        self.sex_show.setScaledContents(True)
        self.sex_show.setObjectName("sex_show")
        self.gridLayout.addWidget(self.sex_show, 3, 0, 1, 1)
        self.sex_input = QtWidgets.QComboBox(self.formGroupBox)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.sex_input.setFont(font)
        self.sex_input.setObjectName("sex_input")
        self.sex_input.addItem("")
        self.sex_input.addItem("")
        self.sex_input.addItem("")
        self.gridLayout.addWidget(self.sex_input, 3, 1, 1, 1)
        self.tb_name_input = QtWidgets.QLineEdit(self.formGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_name_input.sizePolicy().hasHeightForWidth())
        self.tb_name_input.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.tb_name_input.setFont(font)
        self.tb_name_input.setText("")
        self.tb_name_input.setObjectName("tb_name_input")
        self.gridLayout.addWidget(self.tb_name_input, 0, 1, 1, 1)
        self.searchResult = QtWidgets.QListWidget(Widget)
        self.searchResult.setGeometry(QtCore.QRect(40, 190, 181, 121))
        self.searchResult.setObjectName("searchResult")
        self.outputFile = QtWidgets.QPushButton(Widget)
        self.outputFile.setGeometry(QtCore.QRect(250, 50, 101, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.outputFile.setFont(font)
        self.outputFile.setObjectName("outputFile")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Widget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(230, 260, 142, 51))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_3.setSpacing(3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.label_2.setFont(font)
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.label = QtWidgets.QLabel(Widget)
        self.label.setGeometry(QtCore.QRect(240, 180, 101, 61))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/images/01_logo.jpg"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.gridLayoutWidget = QtWidgets.QWidget(Widget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(50, 110, 154, 71))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.postPageLimit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.postPageLimit.setFont(font)
        self.postPageLimit.setObjectName("postPageLimit")
        self.gridLayout_2.addWidget(self.postPageLimit, 0, 1, 1, 1)
        self.postCommentPageLimit_show = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.postCommentPageLimit_show.setFont(font)
        self.postCommentPageLimit_show.setScaledContents(True)
        self.postCommentPageLimit_show.setObjectName("postCommentPageLimit_show")
        self.gridLayout_2.addWidget(self.postCommentPageLimit_show, 0, 2, 1, 1)
        self.postPageLimit_show = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.postPageLimit_show.setFont(font)
        self.postPageLimit_show.setScaledContents(True)
        self.postPageLimit_show.setObjectName("postPageLimit_show")
        self.gridLayout_2.addWidget(self.postPageLimit_show, 0, 0, 1, 1)
        self.postPageLimit_show_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.postPageLimit_show_2.setFont(font)
        self.postPageLimit_show_2.setScaledContents(True)
        self.postPageLimit_show_2.setObjectName("postPageLimit_show_2")
        self.gridLayout_2.addWidget(self.postPageLimit_show_2, 1, 0, 1, 1)
        self.postCommentPageLimit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.postCommentPageLimit.setFont(font)
        self.postCommentPageLimit.setObjectName("postCommentPageLimit")
        self.gridLayout_2.addWidget(self.postCommentPageLimit, 1, 1, 1, 1)
        self.postCommentPageLimit_show_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.postCommentPageLimit_show_2.setFont(font)
        self.postCommentPageLimit_show_2.setScaledContents(True)
        self.postCommentPageLimit_show_2.setObjectName("postCommentPageLimit_show_2")
        self.gridLayout_2.addWidget(self.postCommentPageLimit_show_2, 1, 2, 1, 1)
        self.dictCountShow = QtWidgets.QLabel(Widget)
        self.dictCountShow.setGeometry(QtCore.QRect(231, 121, 75, 17))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.dictCountShow.setFont(font)
        self.dictCountShow.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.dictCountShow.setScaledContents(True)
        self.dictCountShow.setObjectName("dictCountShow")
        self.dictCountOutput = QtWidgets.QLabel(Widget)
        self.dictCountOutput.setGeometry(QtCore.QRect(312, 121, 41, 17))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.dictCountOutput.setFont(font)
        self.dictCountOutput.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.dictCountOutput.setObjectName("dictCountOutput")
        self.frame = QtWidgets.QFrame(Widget)
        self.frame.setGeometry(QtCore.QRect(231, 144, 16, 16))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.searchButton.raise_()
        self.formGroupBox.raise_()
        self.searchResult.raise_()
        self.outputFile.raise_()
        self.label.raise_()
        self.verticalLayoutWidget_2.raise_()
        self.label.raise_()
        self.sex_show.raise_()
        self.gridLayoutWidget.raise_()

        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)

        self.searchButton.clicked.connect(self.search)
        self.outputFile.clicked.connect(self.saveFile)


    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", "贴吧用户采集器"))
        self.searchButton.setText(_translate("Widget", "开始搜索"))
        self.tb_name_show.setText(_translate("Widget", "贴吧名称"))
        self.keywords_show.setText(_translate("Widget", "关键词(选填)"))
        self.sex_show.setText(_translate("Widget", "性别"))
        self.sex_input.setItemText(0, _translate("Widget", "不限"))
        self.sex_input.setItemText(1, _translate("Widget", "男性"))
        self.sex_input.setItemText(2, _translate("Widget", "女性"))
        self.outputFile.setText(_translate("Widget", "导出"))
        self.dictCountOutput.setText(_translate("Widget", "0"))
        self.dictCountShow.setText(_translate("Widget", "已获取用户数:"))
        self.label_2.setText(_translate("Widget", "01工作室"))
        self.label_3.setText(_translate("Widget", "qq群:595202003"))
        self.postCommentPageLimit_show.setText(_translate("Widget", "页帖子"))
        self.postPageLimit_show.setText(_translate("Widget", "采集前"))
        self.postPageLimit_show_2.setText(_translate("Widget", "采集前"))
        self.postCommentPageLimit_show_2.setText(_translate("Widget", "页回复"))

    def saveFile(self):
        fileName = QFileDialog.getSaveFileName(None, 'save file', '', "Text Files (*.txt)")
        if(fileName[0]==""):
            return
        curFile = open(fileName[0], "w", encoding="utf-8")
        for i in spider.dict:
            curFile.write(i + "\n")

    isClicked = False
    def search(self):
        _translate = QtCore.QCoreApplication.translate
        if (self.isClicked == False):
            self.isClicked = True
            self.searchResult.clear()
            self.dictCountOutput.setText("0")

            self.searchButton.setText(_translate("Widget", "停止"))
            tb_name = self.tb_name_input.text()
            sex = self.sex_input.currentIndex()
            keywords = self.keywords_input.text()
            postPageLimit = self.postPageLimit.text()
            postCommentPageLimit = self.postCommentPageLimit.text()
            dictMonitor = monitorDictThread(self)
            dictMonitor.setDaemon(True)
            dictMonitor.start()
            mainThread = spider.Main(tb_name, keywords, {"sex": sex}, postPageLimit, postCommentPageLimit)
            mainThread.start()

            monitorScanner = monitorScannerThread(spider.totalThread, self, dictMonitor)
            monitorScanner.start()
        else:
            # stop all threads and set button text to start search
            self.searchButton.setText(_translate("Widget", "开始搜索"))
            self.stopAllThreads()
            self.isClicked = False

    def stopAllThreads(self):
        totalThreads = spider.totalThread
        for i in totalThreads:
            i.stop()

if __name__ == "__main__":

    import sys


    app = QtWidgets.QApplication(sys.argv)

    Widget = QtWidgets.QWidget()
    ui = Ui_Widget()
    ui.setupUi(Widget)
    Widget.show()
    sys.exit(app.exec_())
    print()




