from PyQt5.QtWidgets import (
    QApplication, QVBoxLayout, QMainWindow, QWidget, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal
from sys import argv
from resources.outer_layer import BottomBar, CentralBar
from resources.BaseContainers import BaseMainWindow
from helpers.config import get_width, get_height
from helpers.scrolling_resort_list import ResortMasterList


class MainWindow(BaseMainWindow):
    resorts: ResortMasterList = None
    central_widget: QWidget = None
    move_left = pyqtSignal()
    move_right = pyqtSignal()

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.resorts = ResortMasterList()
        self.move_left.connect(self.move_left_handler)
        self.move_right.connect(self.move_right_handler)
        self.initUI()
        self.paintUI(resort=self.resorts.get_resort_at_index(0))

    def initUI(self):
        self.central_widget = QWidget(parent=self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.layout)

    def clearUI(self):
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)

    def paintUI(self, resort=''):
        cb = CentralBar(parent=self, resort=resort)
        cb.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        cb.setFixedHeight(int(get_height() * 0.95))
        bb = BottomBar(parent=self)
        bb.setFixedHeight(int(get_height() * 0.05))
        self.layout.addWidget(cb, alignment=Qt.AlignVCenter)
        self.layout.addWidget(bb, alignment=Qt.AlignBottom)

    def move_left_handler(self):
        self.clearUI()
        self.initUI()
        self.paintUI(self.resorts.get_previous_resort())

    def move_right_handler(self):
        self.clearUI()
        self.initUI()
        self.paintUI(self.resorts.get_next_resort())


if __name__ == '__main__':
    argv.append("--disable-web-security")
    app = QApplication(argv)
    window = MainWindow()
    window.show()
    app.exec_()
