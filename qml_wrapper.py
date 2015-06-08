# -*- coding:utf8 -*-
from PyQt5.QtCore import *
from datetime import datetime as dt

class TaskWrapper(QObject):
    def __init__(self, task, parent=None):
        """
        Wrapping task from sql row. Wrapped task is shown on QML list (QQuickView()).
        :param task: dict
        :param parent: object
        """
        super(TaskWrapper, self).__init__(parent)

        self._task = task
        self._message = ''
        self._id = None
        self._date = None
        self._priority = ''
        self._datetime = None
        self._hour_minute = None
        self._cyclic = None
        self._action = None
        self._done = None
        self._expired = False
        
    @pyqtProperty(str)
    def message(self):
        return self._task['message']

    @message.setter
    def message(self, message):
        self._message = message

    @pyqtProperty(int)
    def id(self):
        return self._task['id']

    @id.setter
    def id(self, id):
        self._id = id

    @pyqtProperty(str)
    def date(self):
        return self._task['date']

    @date.setter
    def date(self, date):
        self._date = date

    @pyqtProperty(str)
    def priority(self):
        return self._task['priority']

    @priority.setter
    def priority(self, priority):
        self._priority = priority

    @pyqtProperty(str)
    def datetime(self):
        return str(self._task['datetime'])

    @datetime.setter
    def datetime(self, datetime):
        self._datetime = datetime
    
    @pyqtProperty(str)
    def hour_minute(self):
        return str(self._task['datetime'].strftime("%H:%M"))
 
    @hour_minute.setter
    def hour_minute(self, hour_minute):
        self._hour_minute = hour_minute
  
    @pyqtProperty(bool)
    def cyclic(self):
        return self._task['cyclic']

    @cyclic.setter
    def cyclic(self, cyclic):
        self._cyclic = cyclic

    @pyqtProperty(int)
    def action(self):
        return self._task['action']

    @action.setter
    def action(self, action):
        self._action = action

    @pyqtProperty(bool)
    def done(self):
        return self._task['done']

    @done.setter
    def done(self, done):
        self._done = done

    @pyqtProperty(bool)
    def expired(self):
        now = dt.now()
        if self._task['datetime'] < now:
            return True
        else:
            return False
