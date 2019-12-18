from PyQt5.QtWidgets import (
    QApplication, QVBoxLayout, QMainWindow, QWidget, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal
from sys import argv
from resources.outer_layer import BottomBar, CentralBar
from resources.BaseContainers import BaseMainWindow
from helpers.config import get_width, get_height, get_db_path
from helpers.scrolling_resort_list import ResortMasterList
from helpers.threading_functions import cntdown_timer
from db.db_logic import TravelDbReader
from db.db_daemon import db_daemon
from time import time
from threading import Thread


class MainWindow(BaseMainWindow):
    resorts: ResortMasterList = None
    central_widget: QWidget = None
    move_left = pyqtSignal()
    move_right = pyqtSignal()
    db_reader: TravelDbReader = None
    time_to_move: int = None

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.resorts = ResortMasterList()
        self.move_left.connect(self._move_left_handler)
        self.move_right.connect(self._move_right_handler)
        self.initUI()
        self.paintUI(resort=self.resorts.get_resort_at_index(0))

    def initUI(self):
        self.central_widget = QWidget(parent=self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.layout)

    def clearUI(self):
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)

    def paintUI(self, resort: str):
        cb = CentralBar(parent=self, resort=resort)
        cb.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        cb.setFixedHeight(int(get_height() * 0.95))
        bb = BottomBar(parent=self)
        bb.setFixedHeight(int(get_height() * 0.05))
        self.layout.addWidget(cb, alignment=Qt.AlignVCenter)
        self.layout.addWidget(bb, alignment=Qt.AlignBottom)
        self._set_timer()

    def _move_left_handler(self):
        self.clearUI()
        self.initUI()
        self.paintUI(self.resorts.get_previous_resort())

    def _move_right_handler(self):
        self.clearUI()
        self.initUI()
        self.paintUI(self.resorts.get_next_resort())

    def _set_timer(self):
        self.time_to_move = int(time()) + 60


if __name__ == '__main__':
    db_watcher = Thread(target=db_daemon, args=(get_db_path(),), daemon=True)
    db_watcher.start()
    argv.append("--disable-web-security")
    app = QApplication(argv)
    window = MainWindow()
    window.show()
    timer = Thread(target=cntdown_timer, args=(window,), daemon=True)
    timer.start()
    app.exec_()
