from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt


class ProgressBar(QWidget):
    def __init__(self, page_index, parent=None):
        super().__init__(parent)
        self.init_ui(page_index)
        self.page_index = page_index
        
    def init_ui(self, page_index):
        self.setMinimumHeight(50)
        self.setMaximumHeight(50)
        self.layout = QHBoxLayout()
        self.steps = []
        self.layout.setContentsMargins(10, 0, 10, 0)
        self.setLayout(self.layout)

        for i in range(1, 7):
            step = QLabel(str(i))
            step.setFixedSize(20, 20)
            step.setAlignment(Qt.AlignmentFlag.AlignCenter)
            step.setStyleSheet("""
                border-radius: 10px;
                border: 2px solid #000000;
                font-size: 14px;
                font-weight: bold;
            """)
            self.steps.append(step)
            self.layout.addWidget(step)

        # Set the first step as active
        self.set_active_step(page_index)

    def set_active_step(self, index):
        for i, step in enumerate(self.steps):
            if i == index:
                step.setStyleSheet("""
                    border-radius: 10px;
                    border: 2px solid #000000;
                    background-color: #000000;
                    color: #ffffff;
                    font-size: 14px;
                    font-weight: bold;
                """)
            elif i < index:
                step.setStyleSheet("""
                    border-radius: 10px;
                    border: 2px solid #000000;
                    background-color: #000000;
                    color: #ffffff;
                    font-size: 14px;
                    font-weight: bold;
                """)
            else:
                step.setStyleSheet("""
                    border-radius: 10px;
                    border: 2px solid #000000;
                    background-color: #ffffff;
                    color: #000000;
                    font-size: 14px;
                    font-weight: bold;
                """)
