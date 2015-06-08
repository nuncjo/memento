#-*- coding: utf-8 -*-
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtQuick import *

import logging
import main

logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = main.MainWindow()
    main_window.show()

    app.exec_()
    sys.exit()


'''    
C:\Python34\Scripts\pyside-uic main_window.ui -o main_window.py
C:\Python34\Scripts\pyside-uic add_task_widget.ui -o add_task.py
C:\Python34\Scripts\pyside-uic add_idea_widget.ui -o add_idea.py
C:\Python34\Lib\site-packages\PySide\pyside-rcc.exe -py3 resources.qrc -o resources_rc.py

pyuic5 ui/main_window.ui > widgets/main_window.py
pyuic5 ui/add_task_widget.ui > widgets/add_task.py
pyuic5 ui/add_idea_widget.ui > widgets/add_idea.py
pyuic5 ui/alert_box_widget.ui > widgets/alert_box.py
pyuic5 ui/msbox_widget.ui > widgets/msbox.py
pyrcc5 resources.qrc > resources_rc.py
'''