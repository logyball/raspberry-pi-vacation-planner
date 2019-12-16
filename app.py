from PyQt5.QtWidgets import (
    QApplication, QVBoxLayout, QMainWindow, QWidget, QSizePolicy
)
from PyQt5.QtCore import Qt
from sys import argv
from resources.outer_layer import BottomBar, CentralBar
from resources.BaseContainers import BaseMainWindow
from helpers.config import get_width, get_height


class MainWindow(BaseMainWindow):
    central_widget: QWidget = None

    def __init__(self, parent=None, resort=''):
        super(MainWindow, self).__init__(parent)
        self.initUI()
        self.paintUI(resort=resort)

    def initUI(self):
        self.central_widget = QWidget(parent=self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.layout)

    def clearUI(self):
        self.layout = QVBoxLayout()

    def paintUI(self, resort=''):
        cb = CentralBar(parent=self, resort=resort)
        cb.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        cb.setFixedHeight(int(get_height() * 0.95))
        bb = BottomBar(parent=self)
        bb.setFixedHeight(int(get_height() * 0.05))
        self.layout.addWidget(cb, alignment=Qt.AlignVCenter)
        self.layout.addWidget(bb, alignment=Qt.AlignBottom)


if __name__ == '__main__':
    argv.append("--disable-web-security")
    app = QApplication(argv)
    window = MainWindow(
        resort="hood"
    )
    window.show()
    app.exec_()
