# -*- coding:utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from datetime import datetime
from collections import namedtuple
import config as cfg


def fade_in(obj, milisecond):
    animate = QPropertyAnimation(obj, "windowOpacity", obj)
    animate.setDuration(milisecond)
    animate.setStartValue(0)
    animate.setEndValue(0.9)
    animate.start()


def fade_out(obj, milisecond):
    animate = QPropertyAnimation(obj, "windowOpacity", obj)
    animate.setDuration(milisecond)
    animate.setStartValue(0.9)
    animate.setEndValue(0)
    animate.start()

def move_center(obj):
    """
     Moves form to center of the screen
     :param obj: QtObject
    """
    desktop = QApplication.desktop()
    dw = desktop.width()
    dh = desktop.height()
    size = obj.size()
    mw = size.width()
    mh = size.height()
    obj.move(dw/2-mw/2, dh/2-mh/2)

def move_right_bottom(obj):
    """
     Moves form on bottom right corner
     :param obj: QtObject
    """
    desktop = QApplication.desktop()
    dw = desktop.width()
    dh = desktop.height()
    size = obj.size()
    mw = size.width()
    mh = size.height()
    w = dw - mw
    h = dh - mh
    obj.move(w, h - 40)

def handle_mouse(obj, event):
    """
     Handles move object with mouse button pressed
     :param obj: QtObject
     :param event: QtEvent
    """
    if event:
        x = event.globalX()
        y = event.globalY()
        x_w = obj.offset.x()
        y_w = obj.offset.y()
        obj.move(x - x_w, y - y_w)


def today_range(now=None):
    TodayRange = namedtuple('TodayRange', ['start', 'end'])
    if not now:
        now = datetime.now()
    start = datetime(now.year, now.month, now.day, 0, 0, 0)
    end = datetime(now.year, now.month, now.day, 23, 59, 59)
    return TodayRange(start, end)