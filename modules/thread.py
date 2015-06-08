#-*- coding:utf-8 -*-
from PyQt5.QtCore import *
from datetime import datetime, timedelta
from time import sleep
import logging
from tools import today_range
from pool import task_pool
from pool import task_pool
from qml_wrapper import TaskWrapper

_logger = logging.getLogger(__name__)


class ThreadWorker(QThread):
    execSignal = pyqtSignal(int, str)
    remindSignal = pyqtSignal(int, str)

    def __init__(self, parent=None):
        super(ThreadWorker, self).__init__(parent)
        self.mutex = QMutex()
        self._stop = False
        self._running = False
        self._interval = 5
        self._timedelta_interval = 30  #timedelta for creating period in which alert will occur
        self._start_day_range = today_range()
        self._actual_date = None
        self._tasks = None
        self._executed_tasks = []

    def check_day_change(self):
        self._actual_date = datetime.now()
        if self._actual_date < self._start_day_range.start or self._actual_date > self._start_day_range.end:
            return False
        else:
            self._start_day_range = today_range(self._actual_date)
            return True

    def load_current_tasks(self):
        self.mutex.lock()
        self._tasks = [TaskWrapper(task) for task in
                       task_pool.load_tasks_period(str(self._start_day_range.start), str(self._start_day_range.end))]
        self.mutex.unlock()
        return self._tasks

    def tasks_to_execute(self):
        now = datetime.now()
        to_exec = []
        for task in self._tasks:
            task_datetime = datetime.strptime(task.datetime, "%Y-%m-%d %H:%M:%S")
            if task_datetime < now < task_datetime + timedelta(seconds=self._timedelta_interval):
                to_exec.append(task)
        return to_exec

    def execute_tasks(self):
        to_exec = self.tasks_to_execute()
        for task in to_exec:
            if task.id not in self._executed_tasks:
                self.execSignal.emit(task.id, task.action)
                self._executed_tasks.append(task.id)

    def run(self):
        self.load_current_tasks()
        _logger.info("starting thread...")
        self._running = True

        while True and not self._stop:
            self.execute_tasks()
            sleep(1)
            if self.check_day_change():
                self.load_current_tasks()

            sleep(self._interval)
            _logger.info("working")

        self._running = False

    @property
    def running(self):
        return self._running

    @property
    def stop(self):
        return self._stop

    @stop.setter
    def stop(self, value):
        self._stop = value
        return self._stop

    @stop.getter
    def stop(self):
        return self._stop