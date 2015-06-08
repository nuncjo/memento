#-*- coding: utf-8 -*-
from datetime import datetime, timedelta

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtQuick import *
from PyQt5.QtQml import *

from widgets import alert_box
import config as cfg
from tools import fade_in, fade_out
from qml_wrapper import TaskWrapper
from pool import task_pool
from tools import fade_in, fade_out, handle_mouse, move_right_bottom


class AlertBoxForm(QWidget, alert_box.Ui_Form):
    doneSignal = pyqtSignal(dict)
    delaySignal = pyqtSignal(dict)

    def __init__(self, id=None, parent=None):
        super(AlertBoxForm, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet(cfg.STYLES_DICT['alert_css'])
        self._id = id
        self._task = task_pool.load_task(self._id)
        self.alert_qml = QUrl("alert.qml")

        self.context = {'Task': TaskWrapper(self._task)}
        self.qml_alert_view = QQuickView()
        self.qml_alert_view.setSource(self.alert_qml)
        self.ctx = self.qml_alert_view.rootContext()
        self.ctx.setContextProperty('context', self.context)

        self.container = QOpenGLWidget.createWindowContainer(self.qml_alert_view, self)
        self.container.setFocusPolicy(Qt.TabFocus)
        self.root = self.qml_alert_view.rootObject()
        self.root.doneClicked.connect(self.done)
        self.root.cancelClicked.connect(self.delay)
        self.verticalLayout.addWidget(self.container)
        self.offset = None

    def show(self):
        """Overrides QWidget method"""
        move_right_bottom(self)
        fade_in(self, 2000)

        super(AlertBoxForm, self).show()

    def hide(self):
        """Overrides QWidget method"""
        fade_out(self, 2000)
        super(AlertBoxForm, self).hide()

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

    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if event:
            handle_mouse(self, event)

