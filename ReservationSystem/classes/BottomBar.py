import os
import sys
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QWidget, QSizePolicy
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize
from classes.ProgressBar import ProgressBar


class BottomBar(QWidget):
    def __init__(self, page_index, we_want_previous_button, we_want_next_button):
        super().__init__()

        self.page_index = page_index
        self.script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

        if we_want_previous_button:
            previous_button = QPushButton(self)
            previous_button.setStyleSheet("border: none; background-color: transparent;")
            previous_button_path = os.path.join(self.script_dir, "assets/images/previous_2.png")
            previous_button.setIcon(QIcon(previous_button_path))
            previous_button.setIconSize(QSize(40, 40))
            previous_button.clicked.connect(self.previous_clicked)  # Connect the signal to the slot
        else:
            previous_button = QPushButton(self)
            previous_button.setStyleSheet("border: none; background-color: transparent;")
            previous_button_path = os.path.join(self.script_dir, "assets/images/arrow_tp.png")
            previous_button.setIcon(QIcon(previous_button_path))
            previous_button.setIconSize(QSize(40, 40))

        progress_bar = ProgressBar(self.page_index)

        if we_want_next_button:
            next_button = QPushButton(self)
            next_button.setStyleSheet("border: none; background-color: transparent;")
            next_button_path = os.path.join(self.script_dir, "assets/images/nextfade.png")
            next_button.setIcon(QIcon(next_button_path))
            next_button.setIconSize(QSize(40, 40))
        else:
            next_button = QPushButton(self)
            next_button.setStyleSheet("border: none; background-color: transparent;")
            next_button_path = os.path.join(self.script_dir, "assets/images/arrow_tp.png")
            next_button.setIcon(QIcon(next_button_path))
            next_button.setIconSize(QSize(40, 40))

        layout = QHBoxLayout()
        layout.addWidget(previous_button)
        layout.addStretch()
        layout.addWidget(progress_bar)
        layout.addStretch()
        layout.addWidget(next_button)

        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(60)
        self.setFixedWidth(780)

        self.setLayout(layout)

    def previous_clicked(self):
        last_screen_index = 5
        page_index = self.parent().page_index

        if page_index > last_screen_index:
            self.parent().parent().setCurrentIndex(last_screen_index)
        else:
            self.parent().parent().setCurrentIndex(page_index - 1)
