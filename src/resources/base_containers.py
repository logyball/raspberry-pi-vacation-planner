from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QFrame, QMainWindow
)
from PyQt5.Qt import Qt
from src.backend.config import ConfigFunctions


class BaseVContainer(QFrame):
    layout: QVBoxLayout = None
    config: ConfigFunctions = None

    def __init__(self, parent=None):
        super(BaseVContainer, self).__init__(parent)
        self.config = ConfigFunctions()
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)


class BaseHContainer(QFrame):
    layout: QHBoxLayout = None
    config: ConfigFunctions = None

    def __init__(self, parent=None):
        super(BaseHContainer, self).__init__(parent)
        self.config = ConfigFunctions()
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)


class BaseMainWindow(QMainWindow):
    layout: QVBoxLayout = None
    config: ConfigFunctions = None

    def __init__(self, parent=None):
        super(BaseMainWindow, self).__init__(parent)
        self.config = ConfigFunctions()
        self.set_base_ui()

    def set_base_ui(self):
        self.layout = QVBoxLayout()
        self.setFixedHeight(self.config.get_height())
        self.setFixedWidth(self.config.get_width())
        self.layout.setContentsMargins(0, 0, 0, 0)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
