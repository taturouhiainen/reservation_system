import os
import sys
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont, QFontDatabase
from classes.myCalendar import WeekSelector
from classes.BottomBar import BottomBar
from screens.DateSelectionScreen import DateSelectionScreen


class ReservationLengthScreen(QWidget):

    def __init__(self, parent=None):

        # SCREEN INITIALIZATION
        super().__init__(parent)
        self.page_index = 0
        script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

        # Setting window properties
        self.setGeometry(0, 0, 800, 600)

        # Creating the layouts
        self.main_layout = QVBoxLayout()
        self.header_layout = QVBoxLayout()
        self.image_layout = QHBoxLayout()
        self.price_layout = QHBoxLayout()
        self.button_layout = QHBoxLayout()

        # Special settings for price_layout
        self.price_layout.setSpacing(0)
        self.price_layout.setContentsMargins(0, 0, 0, -50)

        # Adding the layouts to the main_layout
        self.main_layout.addLayout(self.header_layout)
        self.main_layout.addStretch()
        self.main_layout.addLayout(self.image_layout)
        self.main_layout.addStretch()
        self.main_layout.addLayout(self.price_layout)
        self.main_layout.addLayout(self.button_layout)

        # Initializing fonts
        # Construct the font path relative to the script directory
        font_path_light = os.path.join(script_dir, "assets/fonts/Montserrat/static/Montserrat-Light.ttf")
        font_path_bold = os.path.join(script_dir, "assets/fonts/Montserrat/static/Montserrat-Bold.ttf")

        # ID
        font_id_light = QFontDatabase.addApplicationFont(font_path_light)
        font_id_bold = QFontDatabase.addApplicationFont(font_path_bold)

        # Create the fonts
        font_light = QFontDatabase.applicationFontFamilies(font_id_light)[0]
        font_bold = QFontDatabase.applicationFontFamilies(font_id_bold)[0]
        # CREATING THE UI
        # Creating the title
        title = QLabel("Pick Your Ride Time,<br>Let the Adventure Begin!", self)
        title.setFont(QFont(font_light, 30))
        title.setStyleSheet("color: #ffffff; text-transform: uppercase;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setMaximumHeight(100)
        self.header_layout.addWidget(title)
        self.header_layout.setSpacing(20)

        # Creating image labels
        image_paths = [
            os.path.join(script_dir, 'assets/images/170.png'),
            os.path.join(script_dir, 'assets/images/spark.png'),
            os.path.join(script_dir, 'assets/images/170.png'),
            os.path.join(script_dir, 'assets/images/130.png'),
            os.path.join(script_dir, 'assets/images/170.png')
        ]

        for image_path in image_paths:
            image = QLabel(self)
            image.setPixmap(QPixmap(image_path))
            image.setScaledContents(True)
            image.setFixedSize(150, 150)
            self.image_layout.addWidget(image)

        # Reservable items
        # Reservation length, and it's assigned
        reservation_lengths = {
            "1 hour": "69 €",
            "2 hours": "119 €",
            "Half Day / 5h": "199 €",
            "Full Day / 10h": "299 €",
            "24 hours": "399 €"
        }

        # The colors we want to use
        colors = ["#00BCD4", "#38FFDD", "#49FF60", "#D7FF45", "#FF9482"]

        # Create the price labels
        i = 0
        for length, price_label in reservation_lengths.items():
            color = colors[i]
            price = QLabel(price_label, self)
            price.setStyleSheet("color: #ffffff; text-transform: uppercase;")
            price.setAlignment(Qt.AlignmentFlag.AlignCenter)
            price.setMaximumHeight(30)

            price_stylesheet: str = f"""
                   * {{
                   color: {color};
                   font-size: 20px;
                   font-weight: 800 !important;
                   text-transform: uppercase;
                   }}
                   """

            price.setStyleSheet(price_stylesheet)
            price.setFont(QFont(font_bold))

            self.price_layout.addWidget(price)
            i += 1

        # Create the length buttons
        i = 0
        for length, price in reservation_lengths.items():
            color = colors[i]
            alt_color = "#FFFFFF"
            button = QPushButton(self)
            button.setText(length)

            button_stylesheet: str = f"""
                   * {{
                   border: 2px solid {color};
                   border-radius: 5px;
                   color: {color};
                   background-color: rgba(0,0,0,0);
                   font-size: 16px;
                   font-weight: 800 !important;
                   height: 50px;
                   text-transform: uppercase;
                   }}

                   *:hover {{
                   background-color: {color};
                   color: {alt_color} !important;
                   }}
                   """

            button.setStyleSheet(button_stylesheet)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setFont(QFont(font_bold))

            # Connect the button to a function
            button.clicked.connect(self.handle_button_click)

            self.button_layout.addWidget(button)
            i += 1

        # Add the bottom bar
        bottom_bar = BottomBar(self.page_index, False, True)
        self.main_layout.addStretch()
        self.main_layout.addWidget(bottom_bar)
        self.setLayout(self.main_layout)

    # Function to handle a click of a reservable item
    def handle_button_click(self):
        button = self.sender()
        reservation_length = button.text()
        if reservation_length.split(" ")[0] == "1":
            reservation_length = 1
        elif reservation_length.split(" ")[0] == "2":
            reservation_length = 2
        elif reservation_length.split(" ")[0].lower() == "half":
            reservation_length = 5
        elif reservation_length.split(" ")[0].lower() == "full":
            reservation_length = 10
        else:
            reservation_length = 24

        # Modify the information on the next page
        date_selection_screen = next(obj for obj in self.parent().children() if isinstance(obj, DateSelectionScreen))
        my_calendar = next(obj for obj in date_selection_screen.children() if isinstance(obj, WeekSelector))

        my_calendar.length = reservation_length
        day_label = my_calendar.day_label
        my_calendar.handle_date_click(day_label)

        # Change the view to the next page
        self.parent().setCurrentIndex(self.page_index + 1)
