from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QPushButton, QMainWindow, QLabel
from resources.BaseContainers import BaseHContainer


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


class ScrollIndexButton(QLabel):
    selected: bool = False
    index: int = None

    def __init__(self, parent=None, base_window=None, index: int = None):
        super(ScrollIndexButton, self).__init__(parent)
        if base_window.get_cur_index() == index:
            self.selected = True
        self.initUI()

    def initUI(self):
        if self.selected:
            f = QFont()
            f.setBold(True)
            f.setPointSize(18)
            self.setFont(f)
            self.setText("O")
        else:
            self.setText("o")


class ScrollIndexButtonContainer(BaseHContainer):
    def __init__(self, parent=None, base_window=None):
        super(ScrollIndexButtonContainer, self).__init__(parent)
        self.initUI(base_window=base_window)

    def initUI(self, base_window):
        for index in range(base_window.get_num_resorts()):
            self.layout.addWidget(ScrollIndexButton(base_window=base_window, index=index), alignment=Qt.AlignHCenter)
