from PyQt5.QtWidgets import (
    QLabel, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy
)
from PyQt5.QtCore import Qt
from resources import left_sidebar, right_sidebar
from helpers.testing_utils import set_random_background_color
from helpers.config import get_width, get_height


class BottomBar(QWidget):
    left: QWidget = None
    middle: QWidget = None
    right: QWidget = None
    layout: QHBoxLayout = None

    def __init__(self, parent=None):
        super(BottomBar, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.left = QWidget()
        self.middle = QWidget()
        self.right = QWidget()
        self.left.setMinimumWidth(int(get_width() * 0.05))
        self.middle.setMinimumWidth(int(get_width() * 0.89))
        self.middle.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.right.setMinimumWidth(int(get_width() * 0.05))
        for w in (self.left, self.middle, self.right):
            set_random_background_color(w)
        self.layout.addWidget(self.left, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.middle,  alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.right, alignment=Qt.AlignRight)
        self.setLayout(self.layout)


class MiddleBar(QWidget):
    left: left_sidebar.LeftSidebar = None
    right: right_sidebar.ResortInfo = None
    layout: QHBoxLayout = None

    def __init__(self, parent=None):
        super(MiddleBar, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.left = left_sidebar.LeftSidebar(parent=self)
        self.right = right_sidebar.ResortInfo(parent=self)
        self.left.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.left.setMinimumWidth(int(get_width() * 0.3))
        self.right.setMinimumWidth(int(get_width() * 0.7))
        self.layout.addWidget(self.left, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.right, alignment=Qt.AlignRight)
        self.setLayout(self.layout)


class TopBar(QWidget):
    left: QWidget = None
    middle: QWidget = None
    right: QWidget = None
    layout: QHBoxLayout = None

    def __init__(self, parent=None):
        super(TopBar, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.left = QWidget()
        self.left.setMinimumWidth(int(get_width() * 0.3))
        self.middle = QWidget()
        self.middle.setMinimumWidth(int(get_width() * 0.5))
        self.middle.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.right = QWidget()
        self.right.setMinimumWidth(int(get_width() * 0.2))
        for w in (self.left, self.middle, self.right):
            set_random_background_color(w)
        self.layout.addWidget(self.left, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.middle,  alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.right, alignment=Qt.AlignRight)
        self.setLayout(self.layout)