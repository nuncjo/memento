# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/add_idea_widget.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(436, 507)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/png/tray.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        Form.setWindowOpacity(0.95)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEdit_name = QtWidgets.QLineEdit(Form)
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.verticalLayout.addWidget(self.lineEdit_name)
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.lineEdit_fuzzyfilter = QtWidgets.QLineEdit(Form)
        self.lineEdit_fuzzyfilter.setObjectName("lineEdit_fuzzyfilter")
        self.verticalLayout.addWidget(self.lineEdit_fuzzyfilter)
        self.comboBox_tasks = QtWidgets.QComboBox(Form)
        self.comboBox_tasks.setObjectName("comboBox_tasks")
        self.verticalLayout.addWidget(self.comboBox_tasks)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_save = QtWidgets.QPushButton(Form)
        self.pushButton_save.setObjectName("pushButton_save")
        self.horizontalLayout.addWidget(self.pushButton_save)
        self.pushButton_archive = QtWidgets.QPushButton(Form)
        self.pushButton_archive.setObjectName("pushButton_archive")
        self.horizontalLayout.addWidget(self.pushButton_archive)
        self.pushButton_cancel = QtWidgets.QPushButton(Form)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.horizontalLayout.addWidget(self.pushButton_cancel)
        self.pushButton_delete = QtWidgets.QPushButton(Form)
        self.pushButton_delete.setObjectName("pushButton_delete")
        self.horizontalLayout.addWidget(self.pushButton_delete)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_3.setContentsMargins(-1, 2, -1, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_3.addWidget(self.label_8)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.frame_2 = QtWidgets.QFrame(Form)
        self.frame_2.setMinimumSize(QtCore.QSize(38, 38))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_10.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_10.setHorizontalSpacing(0)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.toolButton_close = QtWidgets.QToolButton(self.frame_2)
        self.toolButton_close.setMinimumSize(QtCore.QSize(32, 32))
        self.toolButton_close.setMaximumSize(QtCore.QSize(32, 32))
        self.toolButton_close.setStyleSheet("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/png/cross.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_close.setIcon(icon1)
        self.toolButton_close.setIconSize(QtCore.QSize(48, 48))
        self.toolButton_close.setObjectName("toolButton_close")
        self.gridLayout_10.addWidget(self.toolButton_close, 0, 0, 1, 1)
        self.horizontalLayout_3.addWidget(self.frame_2)
        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Idea"))
        self.lineEdit_name.setPlaceholderText(_translate("Form", "Name"))
        self.textEdit.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.textEdit.setPlaceholderText(_translate("Form", "Your idea description"))
        self.lineEdit_fuzzyfilter.setPlaceholderText(_translate("Form", "Type to filter task"))
        self.pushButton_save.setText(_translate("Form", "Save"))
        self.pushButton_archive.setText(_translate("Form", "Archive"))
        self.pushButton_cancel.setText(_translate("Form", "Cancel"))
        self.pushButton_delete.setText(_translate("Form", "Delete"))
        self.label_8.setText(_translate("Form", "Add/edit idea"))
        self.toolButton_close.setToolTip(_translate("Form", "Close"))
        self.toolButton_close.setText(_translate("Form", "..."))

import resources_rc
