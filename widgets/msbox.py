# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/msbox_widget.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(320, 196)
        Form.setMinimumSize(QtCore.QSize(320, 196))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/png/tray.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        Form.setWindowOpacity(0.95)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(-1, 2, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_title = QtWidgets.QLabel(Form)
        self.label_title.setObjectName("label_title")
        self.horizontalLayout.addWidget(self.label_title)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.frame_2 = QtWidgets.QFrame(Form)
        self.frame_2.setMinimumSize(QtCore.QSize(38, 38))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_9.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_9.setHorizontalSpacing(0)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.toolButton_close = QtWidgets.QToolButton(self.frame_2)
        self.toolButton_close.setMinimumSize(QtCore.QSize(32, 32))
        self.toolButton_close.setMaximumSize(QtCore.QSize(32, 32))
        self.toolButton_close.setStyleSheet("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/png/cross.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_close.setIcon(icon1)
        self.toolButton_close.setIconSize(QtCore.QSize(48, 48))
        self.toolButton_close.setObjectName("toolButton_close")
        self.gridLayout_9.addWidget(self.toolButton_close, 0, 0, 1, 1)
        self.horizontalLayout.addWidget(self.frame_2)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.pushButton_done = QtWidgets.QPushButton(Form)
        self.pushButton_done.setObjectName("pushButton_done")
        self.gridLayout_3.addWidget(self.pushButton_done, 2, 0, 1, 1)
        self.pushButton_ok = QtWidgets.QPushButton(Form)
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.gridLayout_3.addWidget(self.pushButton_ok, 2, 0, 1, 1)
        self.pushButton_cancel = QtWidgets.QPushButton(Form)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.gridLayout_3.addWidget(self.pushButton_cancel, 2, 1, 1, 1)
        self.label_message = QtWidgets.QLabel(Form)
        self.label_message.setMinimumSize(QtCore.QSize(300, 100))
        self.label_message.setWordWrap(True)
        self.label_message.setObjectName("label_message")
        self.gridLayout_3.addWidget(self.label_message, 0, 0, 1, 2)
        self.gridLayout.addLayout(self.gridLayout_3, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Message"))
        self.label_title.setText(_translate("Form", "Add/edit task"))
        self.toolButton_close.setToolTip(_translate("Form", "Close"))
        self.toolButton_close.setText(_translate("Form", "..."))
        self.pushButton_done.setText(_translate("Form", "Set done"))
        self.pushButton_ok.setText(_translate("Form", "Consider it done"))
        self.pushButton_cancel.setText(_translate("Form", "Remind after 30 min"))
        self.label_message.setText(_translate("Form", "TextLabel"))

import resources_rc
