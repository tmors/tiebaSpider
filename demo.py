# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget.ui'
#
# Created by: PyQt5 UI code generator 5.8
#
# WARNING! All changes made in this file will be lost!
import threading
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QListWidgetItem
import spider

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
        while(self.isAllThreadsStopped==False):
            self.isAllThreadsStopped = True
            for curThread in self.totalThreads:
                if (curThread.isAlive() == True):
                    self.isAllThreadsStopped = False
                    break

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
        Widget.resize(487, 318)
        self.searchButton = QtWidgets.QPushButton(Widget)
        self.searchButton.setGeometry(QtCore.QRect(250, 50, 99, 31))
        self.searchButton.setObjectName("searchButton")
        self.formLayoutWidget = QtWidgets.QWidget(Widget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(30, 10, 191, 141))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(11, 11, 11, 11)
        self.formLayout.setSpacing(6)
        self.formLayout.setObjectName("formLayout")
        self.tb_name_show = QtWidgets.QLabel(self.formLayoutWidget)
        self.tb_name_show.setObjectName("tb_name_show")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.tb_name_show)
        self.tb_name_input = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.tb_name_input.setText("")
        self.tb_name_input.setObjectName("tb_name_input")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.tb_name_input)
        self.keywords_show = QtWidgets.QLabel(self.formLayoutWidget)
        self.keywords_show.setObjectName("keywords_show")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.keywords_show)
        self.keywords_input = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.keywords_input.setObjectName("keywords_input")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.keywords_input)
        self.sex_show = QtWidgets.QLabel(self.formLayoutWidget)
        self.sex_show.setObjectName("sex_show")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.sex_show)
        self.sex_input = QtWidgets.QComboBox(self.formLayoutWidget)
        self.sex_input.setObjectName("sex_input")
        self.sex_input.addItem("")
        self.sex_input.addItem("")
        self.sex_input.addItem("")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.sex_input)
        self.postPageLimit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.postPageLimit.setObjectName("postPageLimit")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.postPageLimit)
        self.postPageLimit_show = QtWidgets.QLabel(self.formLayoutWidget)
        self.postPageLimit_show.setObjectName("postPageLimit_show")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.postPageLimit_show)
        self.postCommentPageLimit_show = QtWidgets.QLabel(self.formLayoutWidget)
        self.postCommentPageLimit_show.setObjectName("postCommentPageLimit_show")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.postCommentPageLimit_show)
        self.postCommentPageLimit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.postCommentPageLimit.setObjectName("postCommentPageLimit")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.postCommentPageLimit)
        self.searchResult = QtWidgets.QListWidget(Widget)
        self.searchResult.setGeometry(QtCore.QRect(30, 160, 221, 141))
        self.searchResult.setObjectName("searchResult")
        self.outputFile = QtWidgets.QPushButton(Widget)
        self.outputFile.setGeometry(QtCore.QRect(250, 100, 101, 31))
        self.outputFile.setObjectName("outputFile")
        self.formLayoutWidget_2 = QtWidgets.QWidget(Widget)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(260, 170, 160, 80))
        self.formLayoutWidget_2.setObjectName("formLayoutWidget_2")
        self.formLayout_2 = QtWidgets.QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setContentsMargins(11, 11, 11, 11)
        self.formLayout_2.setSpacing(6)
        self.formLayout_2.setObjectName("formLayout_2")
        self.dictCountShow = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.dictCountShow.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.dictCountShow.setObjectName("dictCountShow")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.dictCountShow)
        self.dictCountOutput = QtWidgets.QLineEdit(self.formLayoutWidget_2)
        self.dictCountOutput.setObjectName("dictCountOutput")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.dictCountOutput)
        self.searchButton.clicked.connect(self.search)
        self.outputFile.clicked.connect(self.saveFile)
        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", "贴吧用户采集器-01工作室(qq群:595202003)"))
        self.searchButton.setText(_translate("Widget", "开始搜索"))
        self.tb_name_show.setText(_translate("Widget", "贴吧名称"))
        self.keywords_show.setText(_translate("Widget", "搜索关键词"))
        self.sex_show.setText(_translate("Widget", "性别"))
        self.sex_input.setItemText(0, _translate("Widget", "不限"))
        self.sex_input.setItemText(1, _translate("Widget", "男性"))
        self.sex_input.setItemText(2, _translate("Widget", "女性"))
        self.postPageLimit_show.setText(_translate("Widget", "帖子页数限制"))
        self.postCommentPageLimit_show.setText(_translate("Widget", "回复页数限制"))
        self.outputFile.setText(_translate("Widget", "导出"))
        self.dictCountShow.setText(_translate("Widget", "已获取用户个数"))


    def saveFile(self):
        fileName = QFileDialog.getSaveFileName(None, 'save file', 'c:\\')
        curFile = open(fileName[0], "w", encoding="utf-8")
        for i in spider.dict:
            curFile.write(i + "\n")


    def search(self):
        tb_name = self.tb_name_input.text()
        sex = self.sex_input.currentIndex()
        keywords = self.keywords_input.text()
        postPageLimit =  self.postPageLimit.text()
        postCommentPageLimit = self.postCommentPageLimit.text()
        dictMonitor = monitorDictThread(self)
        dictMonitor.setDaemon(True)
        dictMonitor.start()
        mainThread = spider.Main(tb_name, keywords, {"sex": sex},postPageLimit, postCommentPageLimit)
        mainThread.start()

        monitorScanner = monitorScannerThread(spider.totalThread,self, dictMonitor)
        monitorScanner.start()
        # time.sleep(20)
        # model = QStandardItemModel(self.searchResult)
        # for i in spider.dict:
        #     curUser = spider.dict.get(i)
        #     str = curUser.toString()
        #     item = QStandardItem(str)
        #     model.appendRow(item)
        # self.searchResult.setModel(model)
        # self.searchResult.show()
        print()

if __name__ == "__main__":

    import sys


    app = QtWidgets.QApplication(sys.argv)

    Widget = QtWidgets.QWidget()
    ui = Ui_Widget()
    ui.setupUi(Widget)
    Widget.show()
    sys.exit(app.exec_())
    print()




