# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'evaluate.ui'
#
# Created: Wed Apr 16 21:11:41 2014
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_Evaluator(object):
    def setupUi(self, Evaluator):
        Evaluator.setObjectName(_fromUtf8("Evaluator"))
        Evaluator.resize(666, 370)
        self.horizontalLayout = QtGui.QHBoxLayout(Evaluator)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.fileList = QtGui.QListWidget(Evaluator)
        self.fileList.setObjectName(_fromUtf8("fileList"))
        item = QtGui.QListWidgetItem()
        self.fileList.addItem(item)
        self.horizontalLayout.addWidget(self.fileList)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.addButton = QtGui.QPushButton(Evaluator)
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.verticalLayout.addWidget(self.addButton)
        self.removeButton = QtGui.QPushButton(Evaluator)
        self.removeButton.setObjectName(_fromUtf8("removeButton"))
        self.verticalLayout.addWidget(self.removeButton)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.singleRadio = QtGui.QRadioButton(Evaluator)
        self.singleRadio.setObjectName(_fromUtf8("singleRadio"))
        self.verticalLayout_2.addWidget(self.singleRadio)
        self.ratbotRadio = QtGui.QRadioButton(Evaluator)
        self.ratbotRadio.setChecked(True)
        self.ratbotRadio.setObjectName(_fromUtf8("ratbotRadio"))
        self.verticalLayout_2.addWidget(self.ratbotRadio)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.processButton = QtGui.QPushButton(Evaluator)
        self.processButton.setEnabled(False)
        self.processButton.setObjectName(_fromUtf8("processButton"))
        self.verticalLayout.addWidget(self.processButton)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Evaluator)
        QtCore.QMetaObject.connectSlotsByName(Evaluator)

    def retranslateUi(self, Evaluator):
        Evaluator.setWindowTitle(_translate("Evaluator", "Evaluator", None))
        __sortingEnabled = self.fileList.isSortingEnabled()
        self.fileList.setSortingEnabled(False)
        item = self.fileList.item(0)
        item.setText(_translate("Evaluator", "Add files...", None))
        self.fileList.setSortingEnabled(__sortingEnabled)
        self.addButton.setText(_translate("Evaluator", "Add files", None))
        self.removeButton.setText(_translate("Evaluator", "Remove files", None))
        self.singleRadio.setText(_translate("Evaluator", "Single mode", None))
        self.ratbotRadio.setText(_translate("Evaluator", "Rat/robot mode", None))
        self.processButton.setText(_translate("Evaluator", "Process", None))

