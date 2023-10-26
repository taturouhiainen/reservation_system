import os
import sys
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QFontDatabase
from classes.BottomBar import BottomBar
from classes.myCalendar import WeekSelector
from classes.general import init_fonts


class DateSelectionScreen(QWidget):
    def __init__(self, parent=None):

        # SCREEN INITIALIZATION
        super().__init__(parent)
        self.page_index = 1

        # Setting window properties
        self.setGeometry(0, 0, 800, 600)
        self.reservation_length = None

        # Creating the layouts
        self.main_layout = QVBoxLayout()
        self.header_layout = QVBoxLayout()
        self.calendar_layout = QHBoxLayout()
        self.time_layout = QHBoxLayout()

        # Adding the layouts
        self.main_layout.addLayout(self.header_layout)
        self.main_layout.addLayout(self.calendar_layout)
        self.main_layout.addLayout(self.time_layout)

        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

        # Construct the font path relative to the script directory
        font_path_light = os.path.join(script_dir, "assets/fonts/Montserrat/static/Montserrat-Light.ttf")
        font_path_bold = os.path.join(script_dir, "assets/fonts/Montserrat/static/Montserrat-Bold.ttf")

        # ID
        font_id_light = QFontDatabase.addApplicationFont(font_path_light)
        font_id_bold = QFontDatabase.addApplicationFont(font_path_bold)

        # Create the fonts
        self.font_light = QFontDatabase.applicationFontFamilies(font_id_light)[0]
        self.font_bold = QFontDatabase.applicationFontFamilies(font_id_bold)[0]

        # CREATING THE UI
        # Title
        title = QLabel("Pick Your Ride Date!", self)
        title.setFont(QFont(self.font_light, 30))
        title.setStyleSheet("color: #ffffff; text-transform: uppercase;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setMaximumHeight(100)

        self.header_layout.addWidget(title)
        self.header_layout.setSpacing(20)

        # Calendar view, and the time slot items
        self.week_selector = WeekSelector()
        self.main_layout.addWidget(self.week_selector)

        # Bottom bar
        bottom_bar = BottomBar(self.page_index, True, True)
        self.main_layout.addWidget(bottom_bar)

        # Set the main layout
        self.setLayout(self.main_layout)