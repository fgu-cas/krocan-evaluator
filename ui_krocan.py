# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'evaluate.ui'
#
# Created: Mon Mar 24 19:44:27 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Krocan(object):
    def setupUi(self, Krocan):
        Krocan.setObjectName(_fromUtf8("Krocan"))
        Krocan.resize(666, 370)
        self.horizontalLayout = QtGui.QHBoxLayout(Krocan)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.fileList = QtGui.QListWidget(Krocan)
        self.fileList.setObjectName(_fromUtf8("fileList"))
        item = QtGui.QListWidgetItem()
        self.fileList.addItem(item)
        self.horizontalLayout.addWidget(self.fileList)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.addButton = QtGui.QPushButton(Krocan)
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.verticalLayout.addWidget(self.addButton)
        self.removeButton = QtGui.QPushButton(Krocan)
        self.removeButton.setObjectName(_fromUtf8("removeButton"))
        self.verticalLayout.addWidget(self.removeButton)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.processButton = QtGui.QPushButton(Krocan)
        self.processButton.setEnabled(False)
        self.processButton.setObjectName(_fromUtf8("processButton"))
        self.verticalLayout.addWidget(self.processButton)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Krocan)
        QtCore.QMetaObject.connectSlotsByName(Krocan)

    def retranslateUi(self, Krocan):
        Krocan.setWindowTitle(_translate("Krocan", "Krocan Evaluator", None))
        __sortingEnabled = self.fileList.isSortingEnabled()
        self.fileList.setSortingEnabled(False)
        item = self.fileList.item(0)
        item.setText(_translate("Krocan", "Add files...", None))
        self.fileList.setSortingEnabled(__sortingEnabled)
        self.addButton.setText(_translate("Krocan", "Add files", None))
        self.removeButton.setText(_translate("Krocan", "Remove files", None))
        self.processButton.setText(_translate("Krocan", "Process", None))

