import os
import sys
from PyQt6.QtWidgets import QLineEdit, QFormLayout, QSpacerItem, QSizePolicy, QTextEdit, QVBoxLayout, QLabel, QWidget, QHBoxLayout, QCheckBox, QSpinBox
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QFont, QFontDatabase
from classes.BottomBar import BottomBar
from classes.Customer import Customer
import time
import random
import string
from classes.general import init_fonts


class CustomerInformationScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.page_index = 3

        self.setGeometry(20, 20, 700, 350)
        self.update_confirmation_details = pyqtSignal()

        # Creating the layouts
        self.main_layout = QVBoxLayout()
        self.header_layout = QVBoxLayout()
        self.form_layout = QFormLayout()
        self.service_layout = QHBoxLayout()

        self.next_button_layout = QHBoxLayout()
        # Adding the layouts
        self.main_layout.addLayout(self.header_layout)
        spacer = QSpacerItem(0, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        self.main_layout.addItem(spacer)
        self.main_layout.addLayout(self.form_layout)

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

        # INITIALIZE UI
        # TItle
        title = QLabel("Hang Tight! Share Your Details to Ride", self)
        title.setFont(QFont(self.font_light, 30))
        title.setStyleSheet("color: #ffffff; text-transform: uppercase;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title.setMaximumHeight(100)
        self.header_layout.addWidget(title)
        self.header_layout.setSpacing(20)

        input_field_style = """
            QLineEdit, QTextEdit {
                background-color: transparent;
                border: none;
                border-bottom: 2px solid #ffffff;
                padding: 0px 5px 0px 5px;
                color: #FFFFFF
            }
            QLineEdit:focus, QTextEdit:focus {
                border-bottom-color: #49FF60;
            }
            """

        fixed_height = 23

        # Create inputs
        self.first_name_input_wrapper, self.first_name_input = self.create_input_field("First Name *",                                                                input_field_style)
        self.first_name_input.setFixedHeight(fixed_height)  # set the height of the textboxes

        self.last_name_input_wrapper, self.last_name_input = self.create_input_field("Last Name *", input_field_style)
        self.last_name_input.setFixedHeight(fixed_height)  # set the height of the textboxes

        self.email_input_wrapper, self.email_input = self.create_input_field("Email *", input_field_style)
        self.email_input.setFixedHeight(fixed_height)  # set the height of the textboxes

        self.phone_number_input_wrapper, self.phone_number_input = self.create_input_field("Phone Number *", input_field_style)
        self.phone_number_input.setFixedHeight(fixed_height)  # set the height of the textboxes

        self.additional_info_input_wrapper, self.additional_info_input = self.create_input_field("Additional Information", input_field_style)
        self.additional_info_input.setFixedHeight(fixed_height)  # set the height of the textboxes

        # Add them as rows
        self.form_layout.addRow(self.first_name_input_wrapper)
        self.form_layout.addRow(self.last_name_input_wrapper)
        self.form_layout.addRow(self.email_input_wrapper)
        self.form_layout.addRow(self.phone_number_input_wrapper)
        self.form_layout.addRow(self.additional_info_input_wrapper)

        # Create the number of riders label
        self.number_of_riders_label = QLabel("Number of Riders (1-3) *")
        self.number_of_riders_label.setStyleSheet("color: #FFFFFF")
        self.number_of_riders_label.setFixedWidth(335)
        self.number_of_riders = QSpinBox()
        self.number_of_riders.setRange(1, 3)
        self.number_of_riders.setFixedWidth(50)
        self.number_of_riders.setStyleSheet("color: #000000")
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.number_of_riders)
        self.hbox.addWidget(self.number_of_riders_label)
        self.hbox_widget = QWidget()
        self.hbox_widget.setLayout(self.hbox)
        self.center_aligned_spinbox = self.create_center_aligned_row(self.hbox_widget)

        # Add a 18 y o check checkbox
        self.agree_checkbox_wrapper, self.agree_checkbox = self.create_wrapped_checkbox(
            "I confirm that I am at least 18 years old")
        self.center_aligned_checkbox = self.create_center_aligned_row(self.agree_checkbox_wrapper)

        self.extra_layout = QVBoxLayout()
        self.extra_layout.addWidget(self.center_aligned_spinbox)
        self.extra_layout.addWidget(self.center_aligned_checkbox)
        self.extra_layout.setSpacing(2)
        self.main_layout.addLayout(self.extra_layout)

        # Add a required note
        required_note = QLabel("Fields marked with an * are required.")
        required_note.setStyleSheet("color: #FFFFFF; font-size: 12px;")
        required_note.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addWidget(required_note)

        # Add next button
        self.next_button = QLabel("<strong>NEXT</strong>", self)
        self.next_button.setFixedWidth(200)
        self.next_button.setFont(QFont(self.font_bold, 14))
        self.next_button.setStyleSheet("""
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
        self.next_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.next_button.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.next_button.setMouseTracking(True)

        # Connect the button to the function
        self.next_button.mousePressEvent = lambda event: self.handle_next_button_click()

        # Add the button to the next_button_layout
        self.next_button_layout.addWidget(self.next_button)
        self.main_layout.addLayout(self.next_button_layout)

        # CREATE BOTTOM BAR AND ADD MAIN AND SET MAIN
        bottom_bar = BottomBar(self.page_index, True, True)
        self.main_layout.addWidget(bottom_bar)
        self.setLayout(self.main_layout)

        # Connect input fields to the slot
        self.first_name_input.textChanged.connect(self.check_required_fields)
        self.last_name_input.textChanged.connect(self.check_required_fields)
        self.email_input.textChanged.connect(self.check_required_fields)
        self.phone_number_input.textChanged.connect(self.check_required_fields)
        self.number_of_riders.valueChanged.connect(self.check_required_fields)
        self.agree_checkbox.stateChanged.connect(self.check_required_fields)

        # Call the slot to set the initial state of the Next button
        self.check_required_fields()

    @pyqtSlot()
    def check_required_fields(self):
        # Check if all required fields are filled and terms and conditions are agreed
        all_filled = (bool(self.first_name_input.text()) and
                      bool(self.last_name_input.text()) and
                      bool(self.email_input.text()) and
                      bool(self.phone_number_input.text()) and
                      self.agree_checkbox.isChecked())

        # Enable or disable the Next button based on whether all required fields are filled
        if all_filled:
            self.next_button.setEnabled(True)
            self.next_button.setStyleSheet("""
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
            self.next_button.setCursor(Qt.CursorShape.PointingHandCursor)

        else:
            # They were not filled
            self.next_button.setEnabled(False)
            self.next_button.setStyleSheet("""
                          * {
                               border: 2px solid rgba(255, 255, 255, 0.3);
                              color: rgba(255, 255, 255, 0.3);
                              background-color: rgba(255, 255, 255, 0);
                              border-radius: 5px;
                              padding: 8px 16px;
                              font-weight: 400;
                          }
                      """)
            self.next_button.setCursor(Qt.CursorShape.ArrowCursor)

    def handle_next_button_click(self):
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        email = self.email_input.text()
        phone_number = self.phone_number_input.text()
        number_of_riders = self.number_of_riders.value()
        additional_info = self.additional_info_input.text()

        customer = Customer(first_name, last_name, email, phone_number, additional_info)

        unique_reservation_number = self.generate_unique_reservation_number()

        self.parent().property("reservation_data").customer = customer
        self.parent().property("reservation_data").number_of_riders = number_of_riders
        self.parent().property("reservation_data").reservation_number = unique_reservation_number

        self.parent().setCurrentIndex(self.page_index + 1)

        # Call the update_info method of the confirmation_details_screen
        confirmation_details_screen = self.parent().widget(self.page_index + 1)
        confirmation_details_screen.update_info()

    @staticmethod
    def create_input_field(label_text, style, is_text_edit=False):
        input_field = QTextEdit() if is_text_edit else QLineEdit()
        input_field.setStyleSheet(style)
        input_field.setMaximumWidth(400)
        input_field.setPlaceholderText(label_text)
        # input_field.setFixedHeight(25)  # Add this line to set the height of the textboxes

        wrapper_widget = QWidget()
        hbox = QHBoxLayout()
        hbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hbox.addWidget(input_field)
        wrapper_widget.setLayout(hbox)

        return wrapper_widget, input_field

    @staticmethod
    def create_wrapped_checkbox(text):
        widget = QWidget()
        layout = QHBoxLayout()  # Change QVBoxLayout to QHBoxLayout
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Align the checkbox to the center
        widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        checkbox = QCheckBox(text)
        checkbox.setFixedWidth(400)
        checkbox.setStyleSheet("color: #FFFFFF")
        layout.addWidget(checkbox)
        widget.setLayout(layout)
        return widget, checkbox

    @staticmethod
    def create_center_aligned_row(widget):
        wrapper_widget = QWidget()
        hbox = QHBoxLayout()
        hbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hbox.addWidget(widget)
        wrapper_widget.setLayout(hbox)
        return wrapper_widget

    @staticmethod
    def generate_unique_reservation_number():
        timestamp = int(time.time())  # Get the current timestamp
        random_string = ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=5))  # Generate a random string of length 5
        reservation_number = f"{timestamp}-{random_string}"
        return reservation_number
