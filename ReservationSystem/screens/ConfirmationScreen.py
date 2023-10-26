import os
import sys
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QFont, QFontDatabase
from classes.BottomBar import BottomBar
from screens.SafetyGuidelinesScreen import SafetyGuidelinesScreen
from screens.CancellationPolicyScreen import CancellationPolicyScreen
from classes.general import init_fonts


class ConfirmationScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cancellation_policy_screen = CancellationPolicyScreen()
        self.safety_guidelines_screen = SafetyGuidelinesScreen()

        self.page_index = 5
        self.reservation_data = None
        self.setGeometry(20, 20, 700, 350)

        # Get the directory of the current script
        self.script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

        # Creating the layouts
        self.main_layout = QVBoxLayout()
        self.header_layout = QVBoxLayout()

        # Adding the layouts
        self.main_layout.addLayout(self.header_layout)

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

        title = QLabel("Reservation succesful!", self)
        title.setFont(QFont(self.font_light, 30))
        title.setStyleSheet("color: #ffffff; text-transform: uppercase;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title.setMaximumHeight(100)
        self.header_layout.addWidget(title)
        self.header_layout.setSpacing(20)

        # Generate a unique reservation confirmation number
        reservation_number = "12345"

        # Creating reservation number label
        self.reservation_number_label = QLabel(f"Reservation Confirmation Number: {reservation_number}", self)
        self.reservation_number_label.setFont(QFont(self.font_light, 14))
        self.reservation_number_label.setStyleSheet("color: #ffffff;")
        self.reservation_number_label.setWordWrap(True)
        self.reservation_number_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header_layout.addWidget(self.reservation_number_label)

        # Creating check-in instructions label
        check_in_instructions = QLabel(self)
        check_in_instructions.setFont(QFont(self.font_light, 14))
        check_in_instructions.setStyleSheet("color: #ffffff;")
        check_in_instructions.setWordWrap(True)
        check_in_instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        check_in_instructions.setText(
            "Please arrive <strong>at least 20 minutes</strong> before the reservation time at "
            "<strong>Teivaan satama, 15110 Lahti</strong>.<br>This will allow us to sign the contracts "
            "and provide instructions on how to use the jet ski, ensuring you can "
            "fully enjoy your time on the water.")
        self.header_layout.addWidget(check_in_instructions)
        self.header_layout.setSpacing(20)

        # Safety Guidelines and Cancellation Policy
        self.guidelines_policy_layout = QHBoxLayout()
        self.guidelines_policy_layout.setSpacing(20)

        # Safety Guidelines
        self.safety_guidelines_layout = QVBoxLayout()
        self.safety_guidelines_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.safety_guidelines_icon = QLabel(self)
        self.safety_guidelines_icon.setPixmap(QPixmap(os.path.join(script_dir, "assets/images/safety_icon_c.png")))
        self.safety_guidelines_icon.setScaledContents(True)
        self.safety_guidelines_icon.setFixedSize(100, 100)

        # Safety Guidelines
        self.safety_guidelines_button = QPushButton("SAFETY GUIDELINES", self)
        self.safety_guidelines_button.setFont(QFont(self.font_bold, 14))
        self.safety_guidelines_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.safety_guidelines_button.setFixedWidth(220)
        self.safety_guidelines_button.setStyleSheet("""
                                                    * {
                                                        border: 2px solid rgba(0, 188, 212, 1);
                                                        color: rgba(0, 188, 212, 1);
                                                        background-color: rgba(0, 188, 212, 0);
                                                        border-radius: 5px;
                                                        padding: 8px 16px;
                                                        font-weight: 800;
                                                    }
                                                    *:hover{
                                                        color: rgba(255, 255, 255, 1);
                                                        background-color: rgba(0, 188, 212, 1);
                                                    }
                                                """)

        self.safety_guidelines_layout.addWidget(self.safety_guidelines_icon, alignment=Qt.AlignmentFlag.AlignCenter)
        self.safety_guidelines_layout.addWidget(self.safety_guidelines_button)
        self.safety_guidelines_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Cancellation Policy
        self.cancellation_policy_layout = QVBoxLayout()
        self.cancellation_policy_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.cancellation_policy_icon = QLabel(self)
        self.cancellation_policy_icon.setPixmap(QPixmap(os.path.join(script_dir, "assets/images/policy_icon_c.png")))
        self.cancellation_policy_icon.setScaledContents(True)
        self.cancellation_policy_icon.setFixedSize(100, 100)

        self.cancellation_policy_button = QPushButton("CANCELLATION POLICY", self)
        self.cancellation_policy_button.setFont(QFont(self.font_bold, 14))
        self.cancellation_policy_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancellation_policy_button.setFixedWidth(220)
        self.cancellation_policy_button.setStyleSheet("""
                                                    * {
                                                        border: 2px solid rgb(255,148,130);
                                                        color: rgb(255,148,130);
                                                        background-color: rgba(255, 255, 255, 0);
                                                        border-radius: 5px;
                                                        padding: 8px 16px;
                                                        font-weight: 800;
                                                    }
                                                    *:hover{
                                                        color: rgba(255, 255, 255, 1);
                                                        background-color: rgba(255, 148, 130, 1);
                                                    }
                                                """)

        self.cancellation_policy_layout.addWidget(self.cancellation_policy_icon, alignment=Qt.AlignmentFlag.AlignCenter)
        self.cancellation_policy_layout.addWidget(self.cancellation_policy_button)
        self.cancellation_policy_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add the layouts to the guidelines_policy_layout
        self.guidelines_policy_layout.addLayout(self.safety_guidelines_layout)
        self.guidelines_policy_layout.addLayout(self.cancellation_policy_layout)

        self.safety_guidelines_button.clicked.connect(self.open_safety_guidelines)
        self.cancellation_policy_button.clicked.connect(self.open_cancellation_policy)

        # Add guidelines_policy_layout to the main layout
        self.main_layout.addLayout(self.guidelines_policy_layout)

        # Creating contact information label
        contact_information = QLabel("For any inquiries or assistance, please contact us at:<br>"
                                     "<strong>Phone:</strong> +358 45 277 8520<br>"
                                     "<strong>Email:</strong> varaukset@hetijetti.fi", self)
        contact_information.setFont(QFont(self.font_light, 14))
        contact_information.setStyleSheet("color: #ffffff;")
        contact_information.setWordWrap(True)
        contact_information.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header_layout.addWidget(contact_information)

        # The button to close the program
        self.close_button = QPushButton("READ MORE ON OUR WEBSITE", self)
        self.close_button.setFont(QFont(self.font_bold, 14))
        self.close_button.setStyleSheet("""
                                            * {
                                                 border: 2px solid rgba(255, 255, 255, 1);
                                                color: rgba(255, 255, 255, 1);
                                                background-color: rgba(255, 255, 255, 0);
                                                border-radius: 5px;
                                                padding: 8px 16px;
                                                font-weight: 800;
                                            }
                                            *:hover{
                                                 border: 2px solid rgba(255, 255, 255, 1);
                                                color: rgba(0, 0, 0, 1);
                                                background-color: rgba(255, 255, 255, 1);
                                            }
                                        """)
        self.close_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_button.clicked.connect(self.close_program)
        self.close_button.setFixedWidth(400)
        spacer = QSpacerItem(0, 50, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        self.main_layout.addItem(spacer)
        self.main_layout.addWidget(self.close_button, alignment=Qt.AlignmentFlag.AlignCenter)  # Center the button

        # CREATE BOTTOM BAR AND ADD MAIN AND SET MAIN
        bottom_bar = BottomBar(self.page_index, False, False)
        self.main_layout.addWidget(bottom_bar)
        self.setLayout(self.main_layout)

    def open_safety_guidelines(self):
        self.parent().setCurrentIndex(self.page_index + 1)

    def open_cancellation_policy(self):
        self.parent().setCurrentIndex(self.page_index + 2)

    def close_program(self):
        self.parent().parent().close()

    def update_info(self):
        reservation_data = self.parent().property("reservation_data")
        reservation_number = reservation_data.reservation_number
        self.reservation_number_label.setText(f"Reservation Confirmation Number: {reservation_number}")
