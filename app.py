from PyQt5.QtWidgets import (
    QApplication, QVBoxLayout, QMainWindow, QWidget, QSizePolicy
)
from PyQt5.QtCore import Qt
from sys import argv
from resources.outer_layer import (
    BottomBar, TopBar, MiddleBar
)
from helpers.config import get_width, get_height


class MainWindow(QMainWindow):
    central_widget: QWidget = None
    layout: QVBoxLayout = None

    def __init__(self, parent=None, height=480, width=800):
        super(MainWindow, self).__init__(parent)
        self._setup(height, width)
        self.initUI()

    def initUI(self):
        # tb = TopBar(parent=self)
        # tb.setFixedHeight(int(get_height() * 0.05))
        mb = MiddleBar(parent=self)
        mb.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        mb.setFixedHeight(int(get_height() * 0.94))
        bb = BottomBar(parent=self)
        bb.setFixedHeight(int(get_height() * 0.05))
        # self.layout.addWidget(tb, alignment=Qt.AlignTop)
        self.layout.addWidget(mb, alignment=Qt.AlignVCenter)
        self.layout.addWidget(bb, alignment=Qt.AlignBottom)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.central_widget.setLayout(self.layout)

    def _setup(self, height, width):
        self.setFixedHeight(height)
        self.setFixedWidth(width)
        self.central_widget = QWidget(parent=self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()


if __name__ == '__main__':
    app = QApplication(argv)
    window = MainWindow(
        height=get_height(),
        width=get_width()
    )
    window.show()
    app.exec_()