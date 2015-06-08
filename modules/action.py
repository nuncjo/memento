#-*- coding:utf-8 -*-
from PyQt5.QtMultimedia import *
from PyQt5.QtCore import *
import logging

from modules.msbox import MsBoxForm
from modules.alert_box import AlertBoxForm


class ActionHandler(QObject):

    def __init__(self, id=None):

        self._type = None
        self._id = id
        self.actions = {'alarm': MsBoxForm(self._id),
                        'tooltip': AlertBoxForm(self._id)}

    def execute(self):

        if self._type in self.actions.keys():
            self.actions[self._type].show()
            return self.actions[self._type]
        else:
            return False

    @property
    def type(self):
        return self._type

    @type.getter
    def type(self):
        return self._type

    @type.setter
    def type(self, val):
        self._type = val
        return self._type
