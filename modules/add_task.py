#-*- coding: utf-8 -*-
from datetime import datetime
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from widgets import add_task
from pool import task_pool, idea_pool
import config as cfg
from tools import fade_in, handle_mouse
from modules.add_idea import AddIdeaForm


class AddTaskForm(QWidget, add_task.Ui_Form):

    saveSignal = pyqtSignal(dict)
    setdoneSignal = pyqtSignal(dict)
    deleteSignal = pyqtSignal(dict)

    def __init__(self, id=None, parent=None):
        super(AddTaskForm, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(cfg.STYLES_DICT['forms_css'])
        self._id = id
        self.idea = None
        self.add_idea_form = None

        for opt in cfg.PRIORITY_LIST:
            self.comboBox_priority.addItem(opt, opt)

        for opt, value in cfg.ACTION_DICT.items():
            self.comboBox_event.addItem(opt, value)

        if not self._id:
            self.pushButton_ok.clicked.connect(self.create)
            self.pushButton_done.setDisabled(True)
            self.pushButton_delete.setDisabled(True)
            self.pushButton_show_idea.hide()

        else:
            self.task = task_pool.load_task(self._id)
            self.pushButton_ok.clicked.connect(self.update)

            if self.task.get('done'):
                self.pushButton_done.setText("Restore")
                self.pushButton_done.clicked.connect(self.set_not_done_task)
            else:
                self.pushButton_done.clicked.connect(self.set_done_task)

            self.pushButton_delete.clicked.connect(self.delete)

            self.idea = idea_pool.load_idea_by_task_id(self._id)

            if self.idea:
                self.pushButton_show_idea.clicked.connect(self.open_edit_idea_form)
            else:
                self.pushButton_show_idea.setDisabled(True)

            self.fill_form()

        self.pushButton_cancel.clicked.connect(self.hide)
        self.toolButton_close.clicked.connect(self.hide)
        self.offset = None


    def show(self):
        """Overrides method of QWidget"""
        fade_in(self, 300)
        super(AddTaskForm, self).show()

    def fill_form(self):

        self.plainTextEdit.setPlainText(self.task.get('message'))
        self.comboBox_priority.setCurrentIndex(self.comboBox_priority.findData(self.task.get('priority')))
        self.comboBox_event.setCurrentIndex(self.comboBox_event.findData(self.task.get('action')))
        self.calendarWidget.setSelectedDate(self.task.get('date'))
        self.checkBox_cyclic.setChecked(self.task.get('cyclic'))
        self.timeEdit.setTime(QTime(self.task.get('datetime').hour, self.task.get('datetime').minute))


    def open_edit_idea_form(self):
        self.add_idea_form = AddIdeaForm(self.idea.get('id', None))
        self.add_idea_form.show()

    def create(self):

        data = {
            'id': None,
            'id_idea': None,
            'date': str(self.calendarWidget.selectedDate().toPyDate()),
            'priority': self.comboBox_priority.currentData(),
            'datetime': str(
                datetime.combine(self.calendarWidget.selectedDate().toPyDate(), self.timeEdit.time().toPyTime())),
            'cyclic': self.checkBox_cyclic.isChecked(),
            'action': self.comboBox_event.currentData(),
            'message': self.plainTextEdit.toPlainText(),
            'done': False
        }

        task_pool.add_task(data)
        self.hide()
        self.saveSignal.emit(data)

    def update(self):

        data = {
            'id': self._id,
            'id_idea': None,
            'date': str(self.calendarWidget.selectedDate().toPyDate()),
            'priority': self.comboBox_priority.currentData(),
            'datetime': str(
                datetime.combine(self.calendarWidget.selectedDate().toPyDate(), self.timeEdit.time().toPyTime())),
            'cyclic': self.checkBox_cyclic.isChecked(),
            'action': self.comboBox_event.currentData(),
            'message': self.plainTextEdit.toPlainText(),
            'done': False
        }

        task_pool.update_task(data)
        self.hide()
        self.saveSignal.emit(data)

    def delete(self):

        data = {'id': self._id}
        task_pool.delete_task(data)
        self.hide()
        self.deleteSignal.emit(data)

    def set_done_task(self):

        data = {'id': self._id,
                'done': 1}

        task_pool.set_done_task(data)
        self.hide()
        self.setdoneSignal.emit(data)

    def set_not_done_task(self):

        data = {'id': self._id,
                'done': 0}

        task_pool.set_done_task(data)
        self.hide()
        self.setdoneSignal.emit(data)

    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if event:
            handle_mouse(self, event)

