from PyQt5.QtWidgets import QWidget, QSizePolicy, QPushButton, QMainWindow
from PyQt5.QtCore import Qt, QObject, pyqtSignal
from resources import left_sidebar, right_sidebar
from resources.BaseContainers import BaseHContainer
from helpers.testing_utils import set_random_background_color
from helpers.config import get_width


class ScrollButton(QPushButton):
    base_window: QMainWindow = None

    def __init__(self, parent=None):
        super(ScrollButton, self).__init__(parent)


class ScrollLeftButton(ScrollButton):
    def __init__(self, parent=None, base_window=None):
        super(ScrollButton, self).__init__(parent)
        self.setText("<")
        self.base_window = base_window

    def mousePressEvent(self, event):
        self.base_window.move_left.emit()


class ScrollRightButton(ScrollButton):
    def __init__(self, parent=None, base_window=None):
        super(ScrollButton, self).__init__(parent)
        self.setText(">")
        self.base_window = base_window

    def mousePressEvent(self, event):
        self.base_window.move_right.emit()


class BottomBar(BaseHContainer):
    left: QWidget = None
    middle: QWidget = None
    right: QWidget = None

    def __init__(self, parent=None):
        super(BottomBar, self).__init__(parent)
        self.initUI(base_window=parent)

    def initUI(self, base_window):
        self.left = ScrollLeftButton(parent=self, base_window=base_window)
        self.middle = QWidget()
        self.right = ScrollRightButton(parent=self, base_window=base_window)
        self.left.setMinimumWidth(int(get_width() * 0.05))
        self.middle.setMinimumWidth(int(get_width() * 0.89))
        self.middle.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.right.setMinimumWidth(int(get_width() * 0.05))
        for w in (self.left, self.middle, self.right):
            set_random_background_color(w)
        self.layout.addWidget(self.left, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.middle,  alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.right, alignment=Qt.AlignRight)


class CentralBar(BaseHContainer):
    left: left_sidebar.LeftSidebar = None
    right: right_sidebar.ResortInfo = None

    def __init__(self, parent=None, resort=''):
        super(CentralBar, self).__init__(parent)
        self.initUI(resort=resort)

    def initUI(self, resort=''):
        self.left = left_sidebar.LeftSidebar(parent=self, resort=resort)
        self.right = right_sidebar.ResortInfo(parent=self, resort=resort)
        self.left.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.left.setMinimumWidth(int(get_width() * 0.3))
        self.right.setMinimumWidth(int(get_width() * 0.7))
        self.layout.addWidget(self.left, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.right, alignment=Qt.AlignRight)
