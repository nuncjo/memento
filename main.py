# -*- coding:utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtQuick import *
from PyQt5.QtQml import *
from datetime import datetime, date
from collections import namedtuple
import sys

from widgets import main_window
from modules.add_task import AddTaskForm
from modules.add_idea import AddIdeaForm
from modules.alert_box import AlertBoxForm
from modules.msbox import MsBoxForm
from modules.thread import ThreadWorker
from modules.action import ActionHandler
from qml_wrapper import *
from pool import task_pool, idea_pool
from tools import *
import config as cfg
from functools import wraps


class MainWindow(QMainWindow, main_window.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setupUi(self)
        self.qml_tasks_view = QQuickView()
        self.tasks_qml = QUrl("tasks.qml")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.statusBar().showMessage("{} ver. {}".format(cfg.APP, cfg.VER))

        self.tray_icon_menu = None
        self.restore_action = None
        self.quit_action = None
        self.tray_icon = None

        self.setStyleSheet(cfg.STYLES_DICT['main_css'])
        self.tableWidget_tasks.setStyleSheet(cfg.STYLES_DICT['table_css'])
        self.tableWidget_ideas.setStyleSheet(cfg.STYLES_DICT['table_css'])
        self.tasks_header_view = self.tableWidget_tasks.horizontalHeader()
        self.tasks_header_view.setSectionResizeMode(2, QHeaderView.Stretch)
        self.tasks_header_view.setStyleSheet(cfg.STYLES_DICT['tableheader_css'])
        self.ideas_header_view = self.tableWidget_ideas.horizontalHeader()
        self.ideas_header_view.setSectionResizeMode(2, QHeaderView.Stretch)
        self.ideas_header_view.setStyleSheet(cfg.STYLES_DICT['tableheader_css'])
        self.scrollbar = QScrollBar()
        self.scrollbar.setStyleSheet(cfg.STYLES_DICT['scrollbar_css'])
        self.scrollbar2 = QScrollBar()
        self.scrollbar2.setStyleSheet(cfg.STYLES_DICT['scrollbar_css'])
        self.tableWidget_tasks.setVerticalScrollBar(self.scrollbar)
        self.tableWidget_ideas.setVerticalScrollBar(self.scrollbar2)
        self.tableWidget_tasks.setFocusPolicy(Qt.NoFocus)
        self.tableWidget_ideas.setFocusPolicy(Qt.NoFocus)

        self.current_task_row_id = None
        self.current_idea_row_id = None

        #buttons actions
        self.show_actual_tasks_action = QAction(QIcon(":/icons/icons/png/2441.png"), self.tr("Actual"), self)
        self.show_tasks_action = QAction(QIcon(":/icons/icons/png/checking1.png"), self.tr("Tasks"), self)
        self.show_ideas_action = QAction(QIcon(":/icons/icons/png/headoutline.png"), self.tr("Ideas"), self)
        self.show_settings_action = QAction(QIcon(":/icons/icons/png/settings39.png"), self.tr("Settings"), self)

        #connecting actions
        #self.tableWidget_tasks.itemSelectionChanged.connect(self.selection_changed_task)
        self.show_actual_tasks_action.triggered.connect(self.show_actual_tasks)
        self.show_tasks_action.triggered.connect(self.show_tasks)
        self.show_ideas_action.triggered.connect(self.show_ideas)
        self.show_settings_action.triggered.connect(self.show_settings)
        self.checkBox_always_top.stateChanged.connect(self.change_on_top)

        #default actions
        self.toolButton_24h.setDefaultAction(self.show_actual_tasks_action)
        self.toolButton_tasks.setDefaultAction(self.show_tasks_action)
        self.toolButton_ideas.setDefaultAction(self.show_ideas_action)
        self.toolButton_settings.setDefaultAction(self.show_settings_action)
        self.toolButton_minimize.clicked.connect(self.hide)

        self.pushButton_add_task.clicked.connect(self.open_add_task_form)
        self.pushButton_add_idea.clicked.connect(self.open_add_idea_form)

        self.offset = None
        self.add_task_form = None
        self.add_idea_form = None
        self.bootstrap()

        self.worker = ThreadWorker()
        self.worker.execSignal.connect(self.execute_task)
        self.worker.start()

    def show(self):
        fade_in(self, 1000)
        super(MainWindow, self).show()

    def execute_task(self, id, type):
        handler = ActionHandler(id)
        handler.type = type
        handler.execute()
        action = handler.execute()
        action.doneSignal.connect(self.on_idea_save)
        action.delaySignal.connect(self.on_idea_save)
        self.load_tasks()
        self.reload_tasks_qml()

    def on_idea_save(self):
        self.load_ideas()
        self.load_tasks()
        self.reload_tasks_qml()

    def on_idea_delete(self):
        self.load_ideas()
        self.load_tasks()
        self.reload_tasks_qml()

    def on_idea_archived(self):
        self.load_ideas()
        self.load_tasks()
        self.reload_tasks_qml()

    def on_task_save(self):
        self.load_tasks()
        self.reload_tasks_qml()

    def on_task_delete(self):
        self.load_tasks()
        self.reload_tasks_qml()

    def on_task_set_done(self):
        self.load_tasks()
        self.reload_tasks_qml()

    @staticmethod
    def wrap_tasks():

        range = today_range()
        today = date.today()
        task_pool.refresh_daily({'cyclic': 1,
                                 'showed': today,
                                 'done': 0})

        tasks = task_pool.load_tasks_period(str(range.start), str(range.end))

        tasks_obj = []
        for task in tasks:
            task['date'] = today
            task['datetime'] = datetime(today.year, today.month, today.day, task['datetime'].hour,
                                        task['datetime'].minute, task['datetime'].second)
            task_pool.update_task_date({'id': task['id'],
                                        'date': task['date'],
                                        'datetime': str(task['datetime'])})
            tasks_obj.append(TaskWrapper(task))

        return tasks_obj

    def connect_signals_qml(self):
        root = self.qml_tasks_view.rootObject()
        root.doneClicked.connect(self.done_checked)
        root.moreClicked.connect(self.open_edit_task_form)

    def load_tasks_qml(self):

        tasks_obj = self.wrap_tasks()
        context = {'Tasks': tasks_obj,
                   'Color': "#000000",
                   'Count': len(tasks_obj)}

        self.qml_tasks_view.setSource(self.tasks_qml)
        ctx = self.qml_tasks_view.rootContext()
        ctx.setContextProperty('context', context)

        container = QOpenGLWidget.createWindowContainer(self.qml_tasks_view, self)
        container.setFocusPolicy(Qt.TabFocus)
        self.connect_signals_qml()
        self.verticalLayout.addWidget(container)

    def reload_tasks_qml(self):

        tasks_obj = self.wrap_tasks()

        context = {'Tasks': tasks_obj,
                   'Color': "#000000",
                   'Count': len(tasks_obj)}

        ctx = self.qml_tasks_view.rootContext()
        ctx.setContextProperty('context', context)
        self.qml_tasks_view.setSource(self.tasks_qml)
        self.connect_signals_qml()

    def done_checked(self, id):
        task_pool.set_done_task({'id': id, 'done': 1})
        self.load_tasks()
        self.reload_tasks_qml()

    def bootstrap(self):
        self.create_actions()
        self.create_tray_icon()
        self.set_hidden()
        self.set_readonly()
        self.load_tasks()
        self.load_ideas()
        self.adjust_size()
        self.load_tasks_qml()

        try:
            with open("about.html") as f:
                self.webView.setHtml(f.read())
        except Exception:
            self.webView.setHtml("404 File not found.")

    def set_readonly(self):
        self.tableWidget_ideas.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_tasks.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def set_hidden(self):
        self.tableWidget_tasks.setColumnHidden(0, True)
        self.tableWidget_tasks.setColumnHidden(3, True)
        self.tableWidget_tasks.setColumnHidden(6, True)
        self.tableWidget_tasks.setColumnHidden(7, True)

        self.tableWidget_ideas.setColumnHidden(0, True)
        self.tableWidget_ideas.setColumnHidden(3, True)
        self.tableWidget_ideas.setColumnHidden(1, True)

    def adjust_size(self):
        self.tableWidget_tasks.setColumnWidth(1, 50)
        self.tableWidget_tasks.setColumnWidth(4, 120)
        self.tableWidget_tasks.setColumnWidth(5, 40)
        self.tableWidget_ideas.setColumnWidth(4, 40)
        self.tableWidget_ideas.setColumnWidth(2, 400)

    def selection_changed_task(self):
        wg = qApp.focusWidget()
        if wg:
            index = self.tableWidget_tasks.indexAt(wg.pos())
            if index.isValid():
                self.current_task_row_id = int(self.tableWidget_tasks.item(index.row(), 0).text())

    def selection_changed_idea(self):
        wg = qApp.focusWidget()
        if wg:
            index = self.tableWidget_ideas.indexAt(wg.pos())
            if index.isValid():
                self.current_idea_row_id = int(self.tableWidget_ideas.item(index.row(), 0).text())

    def index_changed_task(self):

        wg = qApp.focusWidget()
        if wg:
            index = self.tableWidget_tasks.indexAt(wg.pos())

            if index.isValid():
                row = {'id': int(self.tableWidget_tasks.item(index.row(), 0).text()),
                       'priority': self.tableWidget_tasks.cellWidget(index.row(), 1).currentData(),
                       'date': str(self.tableWidget_tasks.cellWidget(index.row(), 4).date().toPyDate()),
                       'datetime': str(self.tableWidget_tasks.cellWidget(index.row(), 4).dateTime().toPyDateTime())}

                self.current_task_row_id = row['id']
                self.update_task_short(row)
                print(row)

    def index_changed_idea(self):

        wg = qApp.focusWidget()
        if wg:
            index = self.tableWidget_ideas.indexAt(wg.pos())
            if index.isValid():
                row = {'id': int(self.tableWidget_ideas.item(index.row(), 0).text()),
                       'id_task': int(self.tableWidget_ideas.cellWidget(index.row(), 1).currentData()),
                       'name': self.tableWidget_ideas.cellWidget(index.row(), 2).text(),
                       'description': self.tableWidget_ideas.cellWidget(index.row(), 3).text(),
                       'id_attachment': int(self.tableWidget_ideas.item(index.row(), 4).text())}

                self.current_idea_row_id = row['id']
                self.update_idea(row)
                print(row)

    @staticmethod
    def update_task(row):
        task_pool.update_task(row)

    @staticmethod
    def update_task_short(row):
        task_pool.update_task_short(row)

    @staticmethod
    def create_action_combobox(action=None):
        """ NOT USED """
        cb = QComboBox()
        for opt, value in cfg.ACTION_DICT.items():
            cb.addItem(opt, value)
        cb.setCurrentIndex(cb.findData(action))
        return cb

    @staticmethod
    def create_task_combobox(tasks, task_id=None):
        """ NOT USED """
        cb = QComboBox()
        for task in tasks:
            cb.addItem(task['message'], task['id'])
        cb.setCurrentIndex(cb.findData(task_id))
        return cb

    @staticmethod
    def create_priority_combobox(priority=None):
        cb = QComboBox()
        for opt in cfg.PRIORITY_LIST:
            cb.addItem(opt, opt)  #item, value
        cb.setCurrentIndex(cb.findData(priority))
        return cb

    def load_tasks(self):
        """ Loads tasks into QTableWidget"""
        tasks = task_pool.load_tasks()
        self.tableWidget_tasks.clearContents()
        self.tableWidget_tasks.setRowCount(0)

        for task in tasks:
            self.tableWidget_tasks.insertRow(0)

            id = QTableWidgetItem(str(task['id']))
            task_date = QTableWidgetItem(str(task['date']))

            self.tableWidget_tasks.setItem(0, 0, id)

            priority_item = QTableWidgetItem(str(task['priority']))
            priority_combobox = self.create_priority_combobox(str(task['priority']))
            priority_combobox.currentIndexChanged.connect(self.index_changed_task)
            self.tableWidget_tasks.setCellWidget(0, 1, priority_combobox)
            self.tableWidget_tasks.setItem(0, 1, priority_item)

            message = QTableWidgetItem(task['message'])
            self.tableWidget_tasks.setItem(0, 2, message)

            self.tableWidget_tasks.setItem(0, 3, task_date)

            dtitem = QTableWidgetItem(str(task['datetime']))
            dt = QDateTimeEdit()
            dt.setDateTime(task['datetime'])
            dt.dateTimeChanged.connect(self.index_changed_task)
            self.tableWidget_tasks.setCellWidget(0, 4, dt)
            self.tableWidget_tasks.setItem(0, 4, dtitem)

            more_button = QPushButton(self.tr("Open"))
            more_button.clicked.connect(self.open_edit_task_form)

            self.tableWidget_tasks.setCellWidget(0, 5, more_button)

        self.tableWidget_tasks.resizeColumnToContents(2)
        self.tableWidget_tasks.selectRow(0)


    def load_ideas(self):
        """ Loads ideas into QTableWidget"""

        ideas = idea_pool.load_ideas()
        self.tableWidget_ideas.clearContents()
        self.tableWidget_ideas.setRowCount(0)

        for idea in ideas:
            self.tableWidget_ideas.insertRow(0)

            id = QTableWidgetItem(str(idea['id']))

            self.tableWidget_ideas.setItem(0, 0, id)

            name = QTableWidgetItem(str(idea['name']))
            self.tableWidget_ideas.setItem(0, 2, name)

            more_button = QPushButton(self.tr("Open"))
            more_button.clicked.connect(self.open_edit_idea_form)
            self.tableWidget_ideas.setCellWidget(0, 4, more_button)

        self.tableWidget_ideas.selectRow(0)

    @staticmethod
    def update_idea(row):
        idea_pool.update_idea(row)

    def open_add_task_form(self):
        self.add_task_form = AddTaskForm()
        self.add_task_form.saveSignal.connect(self.on_task_save)
        self.add_task_form.show()

    def open_edit_task_form(self, id=None):
        self.selection_changed_task()

        if not id:
            id = self.current_task_row_id

        self.add_task_form = AddTaskForm(id)
        self.add_task_form.saveSignal.connect(self.on_task_save)
        self.add_task_form.setdoneSignal.connect(self.on_task_set_done)
        self.add_task_form.deleteSignal.connect(self.on_task_delete)
        self.add_task_form.show()

    def open_add_idea_form(self):
        self.add_idea_form = AddIdeaForm()
        self.add_idea_form.saveSignal.connect(self.on_idea_save)
        self.add_idea_form.show()

    def open_edit_idea_form(self):
        self.selection_changed_idea()
        self.add_idea_form = AddIdeaForm(self.current_idea_row_id)
        self.add_idea_form.saveSignal.connect(self.on_idea_save)
        self.add_idea_form.setarchivedSignal.connect(self.on_idea_archived)
        self.add_idea_form.deleteSignal.connect(self.on_idea_delete)
        self.add_idea_form.show()

    def show_actual_tasks(self):
        self.stackedWidget.setCurrentIndex(0)
        self.toolButton_24h.setChecked(True)
        self.reload_tasks_qml()

    def show_tasks(self):
        self.stackedWidget.setCurrentIndex(1)
        self.toolButton_tasks.setChecked(True)
        self.load_tasks()

    def show_ideas(self):
        self.stackedWidget.setCurrentIndex(2)
        self.toolButton_ideas.setChecked(True)
        self.load_ideas()

    def show_settings(self):
        self.stackedWidget.setCurrentIndex(3)
        self.toolButton_settings.setChecked(True)

    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if event:
            handle_mouse(self, event)

    def change_on_top(self):
        if self.checkBox_always_top.isChecked():
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
        self.show()

    # ----- TRAY handling  section start-----
    def hideEvent(self, event):
        if event:
            self.hide()
            self.tray_icon.show()
            self.showMessage('Memento', 'Works in tray', 1000)
            event.ignore()

    def create_actions(self):
        self.restore_action = QAction("&Restore", self, triggered=self.showNormal)
        self.quit_action = QAction("&Quit", self, triggered=qApp.quit)

    def create_tray_icon(self):
        self.tray_icon_menu = QMenu(self)
        self.tray_icon_menu.addAction(self.restore_action)
        self.tray_icon_menu.addSeparator()
        self.tray_icon_menu.addAction(self.quit_action)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(":/icons/icons/png/tray.png"))
        self.tray_icon.setContextMenu(self.tray_icon_menu)

    def showMessage(self, title, message, duration):
        icon = QSystemTrayIcon.MessageIcon()
        self.tray_icon.showMessage(title, message, icon, duration)
        # ----- TRAY handling end -----