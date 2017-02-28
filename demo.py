# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget.ui'
#
# Created by: PyQt5 UI code generator 5.8
#
# WARNING! All changes made in this file will be lost!
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QFileDialog

import spider


class Ui_Widget(object):
    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(487, 318)
        self.searchButton = QtWidgets.QPushButton(Widget)
        self.searchButton.setGeometry(QtCore.QRect(280, 50, 99, 31))
        self.searchButton.setObjectName("searchButton")
        self.formLayoutWidget = QtWidgets.QWidget(Widget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(40, 30, 191, 121))
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
        self.searchResult = QtWidgets.QColumnView(Widget)
        self.searchResult.setGeometry(QtCore.QRect(40, 160, 221, 141))
        self.searchResult.setObjectName("searchResult")
        self.outputFile = QtWidgets.QPushButton(Widget)
        self.outputFile.setGeometry(QtCore.QRect(280, 110, 101, 31))
        self.outputFile.setObjectName("outputFile")

        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)
        self.searchButton.clicked.connect(self.search)
        self.outputFile.clicked.connect(self.saveFile)

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", "Widget"))
        self.searchButton.setText(_translate("Widget", "开始搜索"))
        self.tb_name_show.setText(_translate("Widget", "贴吧名称"))
        self.keywords_show.setText(_translate("Widget", "搜索关键词"))
        self.sex_show.setText(_translate("Widget", "性别"))
        self.sex_input.setItemText(0, _translate("Widget", "不限"))
        self.sex_input.setItemText(1, _translate("Widget", "男性"))
        self.sex_input.setItemText(2, _translate("Widget", "女性"))
        self.outputFile.setText(_translate("Widget", "导出"))

    def saveFile(self):
        fileName = QFileDialog.getSaveFileName(None, 'save file', 'c:\\')
        curFile = open(fileName[0],"w",encoding="utf-8")
        for i in spider.dict:
            curFile.write(i + "\n")
    def search(self):
        tb_name = self.tb_name_input.text()
        sex = self.sex_input.currentIndex()
        keywords = self.keywords_input.text()
        mainThread = spider.Main(tb_name, keywords, {"sex": sex})
        mainThread.setDaemon(True)
        mainThread.start()
        isAllThreadsStopped = False
        time.sleep(5)
        while(isAllThreadsStopped != True):
            isAllThreadsStopped = True
            for curThread in spider.totalThread:
                if(curThread.isAlive() == True):
                    isAllThreadsStopped = False
                    break
            time.sleep(5)
        model = QStandardItemModel(self.searchResult)
        for i in spider.dict:
            curUser = dict.get(i)
            str = curUser.toString()
            item = QStandardItem(str)
            model.appendRow(item)
        self.searchResult.setModel(model)
        self.searchResult.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Widget = QtWidgets.QWidget()
    ui = Ui_Widget()
    ui.setupUi(Widget)
    Widget.show()
    sys.exit(app.exec_())

