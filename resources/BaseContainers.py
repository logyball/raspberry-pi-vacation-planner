from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget


class BaseVContainer(QWidget):
    layout: QVBoxLayout = None

    def __init__(self, parent=None):
        super(BaseVContainer, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)


class BaseHContainer(QWidget):
    layout: QHBoxLayout = None

    def __init__(self, parent=None):
        super(BaseHContainer, self).__init__(parent)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)