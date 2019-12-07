from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QFrame


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