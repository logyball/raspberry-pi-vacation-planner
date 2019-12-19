from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QPushButton, QMainWindow, QLabel

from helpers.styling import load_stylesheet
from resources.BaseContainers import BaseHContainer


class ScrollButton(QPushButton):
    base_window: QMainWindow = None

    def __init__(self, parent=None):
        super(ScrollButton, self).__init__(parent)


class ScrollLeftButton(ScrollButton):
    def __init__(self, parent=None, base_window=None):
        super(ScrollButton, self).__init__(parent)
        self.base_window = base_window
        self.initUI()

    def initUI(self):
        self.setText("<")
        self.setStyleSheet(load_stylesheet('scroll_bar.qss'))

    def mousePressEvent(self, event):
        self.base_window.move_left.emit()


class ScrollRightButton(ScrollButton):
    def __init__(self, parent=None, base_window=None):
        super(ScrollButton, self).__init__(parent)
        self.base_window = base_window
        self.initUI()

    def initUI(self):
        self.setText(">")
        self.setObjectName('leftRightButton')
        self.setStyleSheet(load_stylesheet('scroll_bar.qss'))

    def mousePressEvent(self, event):
        self.base_window.move_right.emit()


class ScrollIndexButton(ScrollButton):
    selected: bool = False
    index: int = None

    def __init__(self, parent=None, base_window=None, index: int = None):
        super(ScrollIndexButton, self).__init__(parent)
        self.base_window = base_window
        self.index = index
        if self.base_window.get_cur_index() == self.index:
            self.selected = True
        self.initUI()

    def initUI(self):
        if self.selected:
            f = QFont()
            f.setPointSize(14)
            f.setBold(True)
            self.setFont(f)
            self.setText("O")
            self.setObjectName('selectedScrollButton')
        else:
            self.setText("o")
            self.setObjectName('scrollButton')
        self.setStyleSheet(load_stylesheet('scroll_bar.qss'))

    def mousePressEvent(self, event):
        self.base_window.move_to_index.emit(self.index)


class ScrollIndexButtonContainer(BaseHContainer):
    def __init__(self, parent=None, base_window=None):
        super(ScrollIndexButtonContainer, self).__init__(parent)
        self.initUI(base_window=base_window)

    def initUI(self, base_window):
        for index in range(base_window.get_num_resorts()):
            self.layout.addWidget(ScrollIndexButton(base_window=base_window, index=index), alignment=Qt.AlignHCenter)
