import sys
from PyQt5.QtCore import QObject, Qt
from BaseData import BaseData
from UI import MainWindow
class Controller(QObject):
    def __init__(self) -> None:
        super().__init__()
        self.base = BaseData()
        self.ui = MainWindow()

        self.ui.show()