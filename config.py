#-*- coding:utf-8 -*-

from configparser import SafeConfigParser
from collections import OrderedDict
import os

VER = 0.2
APP = "Memento"

PRIORITY_LIST = ['A', 'B', 'C']

actions = {
    'Alarm': 'alarm',
    'Tooltip': 'tooltip',
}

ACTION_DICT = OrderedDict(sorted(actions.items(), key=lambda x: x[0]))

config_ini = SafeConfigParser()
config_ini.read("config.ini")

def css_open(template, file):
    css = ''
    with open(os.path.join(template, file), "r") as f:
        css = f.read()
    return css

template = config_ini['SETTINGS'].get('template')

STYLES_DICT = {config_item:css_open(template, config_ini['STYLES'].get(config_item)) for config_item in config_ini['STYLES']}
