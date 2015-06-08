#-*- coding: utf-8 -*-
from datetime import datetime, timedelta
import winsound

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtQuick import *
from PyQt5.QtQml import *

from widgets import msbox
import config as cfg
from qml_wrapper import TaskWrapper
from pool import task_pool
from tools import fade_in, handle_mouse, move_center

class MsBoxForm(QWidget, msbox.Ui_Form):


    doneSignal = pyqtSignal(dict)
    delaySignal = pyqtSignal(dict)
    closeSignal = pyqtSignal()

    def __init__(self, id, parent=None):
        super(MsBoxForm, self).__init__(parent)

        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet(cfg.STYLES_DICT['forms_css'])

        self._id = id
        self._task = task_pool.load_task(self._id)

        self.pushButton_ok.clicked.connect(self.done)
        self.pushButton_cancel.clicked.connect(self.delay)
        self.toolButton_close.clicked.connect(self.close)

        self.label_title.setText("Reminder")
        self.label_message.setText(self._task['message'])

    def close(self):
        self.closeSignal.emit()
        self.hide()

    def delay(self):
        delayed_time = self._task['datetime'] + timedelta(minutes=30)

        task_pool.delay_task({'id': self._id,
                              'datetime': delayed_time})

        self.delaySignal.emit({'id': self._id,
                               'datetime': delayed_time})
        self.hide()

    def done(self):
        task_pool.set_done_task({'done': 1,
                                 'id': self._id})
        self.doneSignal.emit({'id': self._id})
        self.hide()

    def show(self):
        move_center(self)
        fade_in(self, 2000)
        #TODO: better sound handling (not windows only)
        winsound.PlaySound("sounds/alert.wav", winsound.SND_FILENAME)
        super(MsBoxForm, self).show()

    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if event:
            handle_mouse(self, event)