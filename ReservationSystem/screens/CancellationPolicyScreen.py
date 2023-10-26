import os
import sys
import webbrowser
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont, QFontDatabase
from classes.BottomBar import BottomBar
from classes.general import init_fonts


class CancellationPolicyScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.page_index = 6
        self.setGeometry(20, 20, 700, 350)

        self.main_layout = QVBoxLayout()
        self.content_layout = QVBoxLayout()  # New layout for the content
        self.header_layout = QVBoxLayout()

        # Adding the layouts
        self.content_layout.addLayout(self.header_layout)  # Add header_layout to the content_layout
        self.main_layout.addLayout(self.content_layout)  # Add content_layout to the main_layout

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

        title = QLabel("Cancellation Policy", self)
        title.setFont(QFont(self.font_light, 30))
        title.setStyleSheet("color: #ffffff; text-transform: uppercase;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title.setMaximumHeight(100)
        self.header_layout.addWidget(title)

        self.content_layout.setContentsMargins(100, 0, 100, 0)

        image_width = 100
        image_height = 100

        cancellation_policy_points = [
            {
                "icon": "assets/images/cancel_icon_c.png",
                "color": "#00bcd4",
                "title": "Cancellation Deadline",
                "description": "The deadline for canceling a reservation without penalty is "
                               "48 hours before the scheduled reservation time. "
                               "A penalty of the full reservation fee (excl. additional services) applies "
                               "if the customer cancels after the deadline."
            },
            {
                "icon": "assets/images/reschedule_icon_c.png",
                "color": "#49FF60",
                "title": "Company's Right to Cancel or Reschedule",
                "description": "The company reserves the right to cancel or reschedule a reservation "
                               "at its discretion, for reasons such as adverse weather conditions, "
                               "safety concerns, or equipment issues. In such cases, customers will "
                               "be offered the option to reschedule their reservation or receive a full "
                               "refund, as appropriate."
            },
            {
                "icon": "assets/images/noshow_icon_c.png",
                "color": "#FF9482",
                "title": "No-Show Policy",
                "description": "Not showing up for the reservation without prior notice, will result in "
                               "forfeiting the reservation fee."
            }
        ]

        for point in cancellation_policy_points:
            point_layout = QHBoxLayout()

            point_image = QLabel()
            point_image.setPixmap(QPixmap(point['icon']))
            point_image.setScaledContents(True)
            point_image.setFixedSize(image_width, image_height)
            point_layout.addWidget(point_image)

            spacer = QSpacerItem(30, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
            point_layout.addItem(spacer)

            point_title = QLabel(point['title'])
            point_title.setFont(QFont(self.font_light, 18, QFont.Weight.Bold))
            point_title.setStyleSheet(f"color: {point['color']};")
            point_description = QLabel(point['description'])
            point_description.setFont(QFont(self.font_light, 14))
            point_description.setStyleSheet(f"color: #FFFFFF;")
            point_description.setWordWrap(True)

            point_text_layout = QVBoxLayout()
            point_text_layout.addStretch()
            point_text_layout.addWidget(point_title)
            point_text_layout.addWidget(point_description)
            point_text_layout.addStretch()

            point_layout.addLayout(point_text_layout)
            self.content_layout.addLayout(point_layout)  # Add point_layout to the content_layout instead of main layout

        # CREATE BOTTOM BAR AND ADD MAIN AND SET MAIN
        self.website_button = QLabel("<strong>READ MORE ON OUR WEBSITE</strong>", self)
        self.website_button.setFixedWidth(300)
        self.website_button.setFont(QFont(self.font_bold, 14))
        self.website_button.setStyleSheet("""
                                     * {
                                          border: 2px solid rgba(255, 255, 255, 1);
                                         color: rgba(255, 255, 255, 1);
                                         background-color: rgba(255, 255, 255, 0);
                                         border-radius: 5px;
                                         padding: 8px 16px;
                                         font-weight: 400;
                                     }
                                     *:hover{
                                          border: 2px solid rgba(255, 255, 255, 1);
                                         color: rgba(0, 0, 0, 1);
                                         background-color: rgba(255, 255, 255, 1);
                                     }
                                 """)
        self.website_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.website_button.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.website_button.setMouseTracking(True)
        self.website_button.mousePressEvent = lambda event: self.open_website()
        self.main_layout.addWidget(self.website_button, alignment=Qt.AlignmentFlag.AlignCenter)

        bottom_bar = BottomBar(self.page_index, True, False)

        self.main_layout.addWidget(bottom_bar)  # Add bottom_bar to the main_layout

        self.setLayout(self.main_layout)

    @staticmethod
    def open_website():
        webbrowser.open("https://hetijetti.fi")
