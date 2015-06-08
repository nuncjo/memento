#-*- coding: utf-8 -*-
from datetime import datetime

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from fuzzywuzzy import process  #remember about python-Levenstein in case of compilation

from widgets import add_idea
from pool import idea_pool, task_pool
import config as cfg
from tools import fade_in, handle_mouse


class AddIdeaForm(QWidget, add_idea.Ui_Form):
    saveSignal = pyqtSignal(dict)
    setarchivedSignal = pyqtSignal(dict)
    deleteSignal = pyqtSignal(dict)

    def __init__(self, id=None, parent=None):
        super(AddIdeaForm, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(cfg.STYLES_DICT['forms_css'])
        self._id = id

        self.tasks = task_pool.load_tasks()
        self.messages = [task['message'] for task in self.tasks]

        if not self._id:
            self.pushButton_save.clicked.connect(self.create)
            self.pushButton_archive.setDisabled(True)
            self.pushButton_delete.setDisabled(True)
            self.fill_task_combobox(self.tasks)
        else:
            self.pushButton_save.clicked.connect(self.update)
            self.pushButton_archive.clicked.connect(self.set_archived_idea)
            self.pushButton_delete.clicked.connect(self.delete)
            self.fill_form()

        self.pushButton_cancel.clicked.connect(self.cancel)
        self.toolButton_close.clicked.connect(self.hide)
        self.lineEdit_fuzzyfilter.textChanged.connect(self.filter_tasks_combobox)
        self.offset = None
        self.idea_index = 0
        self.idea = None
        self.bootstrap()

    def show(self):
        """Overrides method of QWidget"""
        fade_in(self, 300)
        super(AddIdeaForm, self).show()

    def fill_form(self):
        idea = idea_pool.load_idea(self._id)
        self.lineEdit_name.setText(idea.get('name'))
        self.textEdit.setText(idea.get('description'))
        self.fill_task_combobox(self.tasks, idea.get('id_task'))

    def bootstrap(self):
        self.pushButton_archive.setVisible(False)

    def fill_task_combobox(self, tasks, task_id=None):
        for task in tasks:
            self.comboBox_tasks.addItem(task['message'], task['id'])
        if task_id:
            self.comboBox_tasks.setCurrentIndex(self.comboBox_tasks.findData(task_id))

    def filter_tasks_combobox(self):

        phrase = self.lineEdit_fuzzyfilter.text()

        filtered = process.extract(phrase, self.messages, limit=10)
        filtered_tasks = []
        for message, score in filtered:
            found = [item for item in self.tasks if item['message'] == message]
            filtered_tasks.append(found[0])

        self.comboBox_tasks.clear()
        self.fill_task_combobox(filtered_tasks)

    def create(self):

        data = {
            'id': None,
            'id_task': self.comboBox_tasks.currentData(),
            'id_attachment': 1,
            'name': self.lineEdit_name.text(),
            'description': self.textEdit.toPlainText(),
            'archived': False
        }
        print(data)
        idea_pool.add_idea(data)
        self.saveSignal.emit(data)
        self.hide()


    def delete(self):

        data = {'id': self._id}
        idea_pool.delete_idea(data)
        self.hide()
        self.deleteSignal.emit(data)

    def update(self):
        data = {
            'id': self._id,
            'id_task': self.comboBox_tasks.currentData(),
            'id_attachment': 1,
            'name': self.lineEdit_name.text(),
            'description': self.textEdit.toPlainText(),
            'archived': False
        }

        idea_pool.update_idea(data)
        self.hide()
        self.saveSignal.emit(data)

    def set_archived_idea(self):

        data = {'id': self._id,
                'archived': True}

        idea_pool.set_archived_idea(data)
        self.hide()
        self.setarchivedSignal.emit(data)

    def cancel(self):
        self.hide()

    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if event:
            handle_mouse(self, event)

