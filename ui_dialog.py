# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created: Tue Sep 20 21:12:02 2011
#      by: pyside-uic 0.2.9 running on PySide 1.0.3
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.NonModal)
        Dialog.resize(300, 280)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setModal(True)
        self.horizontalLayout_3 = QtGui.QHBoxLayout(Dialog)
        self.horizontalLayout_3.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.tableView = QtGui.QTableView(Dialog)
        self.tableView.setSortingEnabled(True)
        self.tableView.setObjectName("tableView")
        self.horizontalLayout_3.addWidget(self.tableView)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.btnNew = QtGui.QPushButton(Dialog)
        self.btnNew.setDefault(True)
        self.btnNew.setObjectName("btnNew")
        self.verticalLayout.addWidget(self.btnNew)
        self.btnDelete = QtGui.QPushButton(Dialog)
        self.btnDelete.setEnabled(True)
        self.btnDelete.setObjectName("btnDelete")
        self.verticalLayout.addWidget(self.btnDelete)
        self.btnSubmit = QtGui.QPushButton(Dialog)
        self.btnSubmit.setDefault(False)
        self.btnSubmit.setObjectName("btnSubmit")
        self.verticalLayout.addWidget(self.btnSubmit)
        self.btnRevert = QtGui.QPushButton(Dialog)
        self.btnRevert.setAutoDefault(True)
        self.btnRevert.setObjectName("btnRevert")
        self.verticalLayout.addWidget(self.btnRevert)
        self.btnClose = QtGui.QPushButton(Dialog)
        self.btnClose.setObjectName("btnClose")
        self.verticalLayout.addWidget(self.btnClose)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.btnNew, self.btnDelete)
        Dialog.setTabOrder(self.btnDelete, self.btnSubmit)
        Dialog.setTabOrder(self.btnSubmit, self.btnRevert)
        Dialog.setTabOrder(self.btnRevert, self.btnClose)
        Dialog.setTabOrder(self.btnClose, self.tableView)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Manage Projects", None, QtGui.QApplication.UnicodeUTF8))
        self.btnNew.setText(QtGui.QApplication.translate("Dialog", "&New", None, QtGui.QApplication.UnicodeUTF8))
        self.btnDelete.setText(QtGui.QApplication.translate("Dialog", "&Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSubmit.setText(QtGui.QApplication.translate("Dialog", "&Submit", None, QtGui.QApplication.UnicodeUTF8))
        self.btnRevert.setText(QtGui.QApplication.translate("Dialog", "&Revert", None, QtGui.QApplication.UnicodeUTF8))
        self.btnClose.setText(QtGui.QApplication.translate("Dialog", "&Close", None, QtGui.QApplication.UnicodeUTF8))

