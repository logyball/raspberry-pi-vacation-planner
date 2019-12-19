from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QFrame, QMainWindow
)
from PyQt5.Qt import Qt
from helpers.config import get_width, get_height


class BaseVContainer(QFrame):
    layout: QVBoxLayout = None

    def __init__(self, parent=None):
        super(BaseVContainer, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.setFrameShape(QFrame.Panel)


class BaseHContainer(QFrame):
    layout: QHBoxLayout = None

    def __init__(self, parent=None):
        super(BaseHContainer, self).__init__(parent)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.setFrameShape(QFrame.Panel)


class BaseMainWindow(QMainWindow):
    layout: QVBoxLayout = None

    def __init__(self, parent=None):
        super(BaseMainWindow, self).__init__(parent)
        self.set_base_ui()

    def set_base_ui(self):
        self.layout = QVBoxLayout()
        self.setFixedHeight(get_height())
        self.setFixedWidth(get_width())
        self.layout.setContentsMargins(0, 0, 0, 0)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
