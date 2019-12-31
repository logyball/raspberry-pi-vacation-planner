from PyQt5.QtWidgets import QWidget, QFrame
from PyQt5.QtCore import Qt
from src.backend.styling import load_stylesheet
from src.resources import left_sidebar
from src.resources import right_sidebar
from src.resources.base_containers import BaseHContainer
from src.resources.scroll_bar import ScrollLeftButton, ScrollRightButton, ScrollIndexButtonContainer
from src.backend.config import get_width


class BottomBar(BaseHContainer):
    left: ScrollLeftButton = None
    middle: ScrollIndexButtonContainer = None
    right: ScrollRightButton = None

    def __init__(self, parent: QWidget = None):
        super(BottomBar, self).__init__(parent)
        self.initUI(base_window=parent)
        self._set_sizes_positions()
        self._set_style()

    def initUI(self, base_window: QWidget = None):
        self.left = ScrollLeftButton(parent=self, base_window=base_window)
        self.middle = ScrollIndexButtonContainer(parent=self, base_window=base_window)
        self.right = ScrollRightButton(parent=self, base_window=base_window)

    def _set_sizes_positions(self):
        self.left.setMinimumWidth(int(get_width() * 0.04))
        self.middle.setMinimumWidth(int(get_width() * 0.9))
        self.right.setMinimumWidth(int(get_width() * 0.04))
        self.layout.addWidget(self.left, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.middle,  alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.right, alignment=Qt.AlignRight)

    def _set_style(self):
        self.left.setObjectName('leftRightButton')
        self.right.setObjectName('leftRightButton')
        self.middle.setObjectName('midScrollBar')
        self.setStyleSheet(load_stylesheet('scroll_bar.qss'))
        self.setFrameShape(QFrame.Box)


class CentralBar(BaseHContainer):
    left: left_sidebar.LeftSidebar = None
    right: right_sidebar.ResortInfo = None

    def __init__(self, parent=None, resort=''):
        super(CentralBar, self).__init__(parent)
        self.initUI(resort=resort)

    def initUI(self, resort=''):
        self.left = left_sidebar.LeftSidebar(parent=self, resort=resort)
        self.right = right_sidebar.ResortInfo(parent=self, resort=resort)
        self.left.setFixedWidth(int(get_width() * 0.3))
        self.right.setFixedWidth(int(get_width() * 0.69))
        self.layout.addWidget(self.left, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.right, alignment=Qt.AlignRight)
