import os
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont, QFontDatabase
from classes.BottomBar import BottomBar
import socket
import smtplib
from email.message import EmailMessage
from classes.AdditionalService import AdditionalService
from classes.Customer import Customer
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from classes.general import init_fonts


class ConfirmationDetailsScreen(QWidget):
    def __init__(self, parent=None):
        # INITIALIZING Screen
        super().__init__(parent)
        self.page_index = 4
        self.reservation_data = self.parent().property("reservation_data")
        self.setGeometry(20, 20, 700, 350)

        self.script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

        # Google Sheets API credentials
        self.SHEET_ID = '1PNneUFO2xL7he9pND-Qo6EQV6hNvVWXz40Hs07EdPrY'
        self.SERVICE_ACCOUNT_FILE = os.path.join(self.script_dir, "assets/json/hetijetti-5dc8c0072bd2.json")
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

        # Creating the layouts
        self.main_layout = QVBoxLayout()
        self.header_layout = QVBoxLayout()
        self.details_layout = QHBoxLayout()
        self.jet_ski_layout = QHBoxLayout()
        self.rider_layout = QHBoxLayout()
        self.additional_services_prices_layout = QVBoxLayout()
        self.details_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.next_button_layout = QHBoxLayout()

        # Adding the layouts
        self.main_layout.addLayout(self.header_layout)
        spacer = QSpacerItem(0, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        self.main_layout.addItem(spacer)
        self.main_layout.addLayout(self.details_layout)
        self.main_layout.addLayout(self.next_button_layout)

        # Center the content
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

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

        bold_font = QFont(self.font_light, 14)
        bold_font.setBold(True)

        # DUMMY VALUES FOR TESTING AND INITIAL PAGE LOAD
        self.reservation_data.reservation_time = "10:00-12:00"
        self.reservation_data.reservation_date = "01/05/2023"
        self.reservation_data.reservation_length = "2"
        add_ser = [
            AdditionalService("Wet Suits", 10, "pc", "10$ per rider", "assets/images/services/wetsuit.png",
                              "Stay comfortable and protected during your jet ski ride "
                              "with our high-quality wetsuits in a range of sizes.")
        ]
        self.reservation_data.additional_services = add_ser
        cust = Customer("Erkki", "Eerikki", "erkki@erkki.com", "1234567890", "Kissan synttarit")
        self.reservation_data.customer = cust
        self.reservation_data.jet_ski = "Sea-Doo GTI 130"
        self.reservation_data.reservation_price = self.reservation_data.get_reservation_price(
            self.reservation_data.reservation_length)
        self.reservation_data.number_of_riders = 1

        # INITIALIZING UI
        # Title
        title = QLabel("Almost There!<br>Confirm Your Jet Ski Adventure", self)
        title.setFont(QFont(self.font_light, 30))
        title.setStyleSheet("color: #ffffff; text-transform: uppercase;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title.setMaximumHeight(100)
        self.header_layout.addWidget(title)
        self.header_layout.setSpacing(20)

        # Display jet ski image
        if self.reservation_data.jet_ski:
            jet_ski = self.reservation_data.jet_ski.replace(" ", "-")
            jet_ski_image_path = os.path.join(self.script_dir, f"assets/images/{jet_ski}/{jet_ski.lower().replace('-', '')}.png")
        else:
            jet_ski_image_path = "../assets/images/Sea-Doo-GTI-130/seadoogti130.png"
        self.jet_ski_image = QPixmap(jet_ski_image_path)
        self.jet_ski_image_label = QLabel()
        self.jet_ski_image_label.setPixmap(self.jet_ski_image.scaled(360, 180, Qt.AspectRatioMode.KeepAspectRatio))
        self.jet_ski_image_label.setFixedWidth(250)  # Set fixed width for jet_ski_image_label
        self.jet_ski_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Align the QLabel to the right

        # Display reservation length and date
        self.reservation_layout = QVBoxLayout()

        label_width = 175
        data_width = 250

        # JET SKI
        # Create QLabel for jet ski label
        jet_ski_label = QLabel("Jet Ski:")
        jet_ski_label.setFont(QFont(self.font_light, 14))
        jet_ski_label.setStyleSheet("color: #ffffff;")

        # Create QLabel for jet ski data
        self.jet_ski_data = QLabel(f"{self.reservation_data.jet_ski}")
        self.jet_ski_data.setFont(bold_font)
        self.jet_ski_data.setStyleSheet("color: #ffffff;")

        # Make hbox
        jet_ski_hbox = QHBoxLayout()
        jet_ski_hbox.addWidget(jet_ski_label, alignment=Qt.AlignmentFlag.AlignTop)
        jet_ski_hbox.addWidget(self.jet_ski_data, alignment=Qt.AlignmentFlag.AlignTop)
        jet_ski_hbox.addStretch(1)
        jet_ski_label.setFixedWidth(label_width)
        self.jet_ski_data.setFixedWidth(data_width)
        self.reservation_layout.addLayout(jet_ski_hbox)

        # RESERVATION DATE
        # Create QLabel for reservation date label
        reservation_date_label = QLabel("Reservation Date:")
        reservation_date_label.setFont(QFont(self.font_light, 14))
        reservation_date_label.setStyleSheet("color: #ffffff;")

        # Create QLabel for reservation date data
        self.reservation_date_data = QLabel(f"{self.reservation_data.reservation_date}")
        self.reservation_date_data.setFont(bold_font)
        self.reservation_date_data.setStyleSheet("color: #ffffff;")

        # Make hbox
        date_hbox = QHBoxLayout()
        date_hbox.addWidget(reservation_date_label, alignment=Qt.AlignmentFlag.AlignTop)
        date_hbox.addWidget(self.reservation_date_data, alignment=Qt.AlignmentFlag.AlignTop)
        date_hbox.addStretch(1)
        reservation_date_label.setFixedWidth(label_width)
        self.reservation_date_data.setFixedWidth(data_width)
        self.reservation_layout.addLayout(date_hbox)

        # RESERVATION TIME
        # Create QLabel for reservation time label
        reservation_time_label = QLabel("Reservation Time:")
        reservation_time_label.setFont(QFont(self.font_light, 14))
        reservation_time_label.setStyleSheet("color: #ffffff;")

        # Create QLabel for reservation time data
        self.reservation_time_data = QLabel(f"{self.reservation_data.reservation_time}")
        self.reservation_time_data.setFont(bold_font)
        self.reservation_time_data.setStyleSheet("color: #ffffff;")

        # Make hbox
        time_hbox = QHBoxLayout()
        time_hbox.addWidget(reservation_time_label, alignment=Qt.AlignmentFlag.AlignTop)
        time_hbox.addWidget(self.reservation_time_data, alignment=Qt.AlignmentFlag.AlignTop)
        time_hbox.addStretch(1)
        reservation_time_label.setFixedWidth(label_width)
        self.reservation_time_data.setFixedWidth(data_width)
        self.reservation_layout.addLayout(time_hbox)

        # RESERVATION LENGTH
        # Create QLabel for reservation length label
        reservation_length_label = QLabel("Reservation Length:")
        reservation_length_label.setFont(QFont(self.font_light, 14))
        reservation_length_label.setStyleSheet("color: #ffffff;")

        # Create QLabel for reservation length data
        self.reservation_length_data = QLabel(f"{self.reservation_data.reservation_length} hours")
        self.reservation_length_data.setFont(bold_font)
        self.reservation_length_data.setStyleSheet("color: #ffffff;")

        # Create QLabel for reservation length price
        self.reservation_length_price = QLabel(f"{self.reservation_data.reservation_price} $")
        self.reservation_length_price.setFont(bold_font)
        self.reservation_length_price.setStyleSheet("color: #ffffff;")

        # Make hbox
        length_hbox = QHBoxLayout()
        length_hbox.addWidget(reservation_length_label, alignment=Qt.AlignmentFlag.AlignTop)
        length_hbox.addWidget(self.reservation_length_data, alignment=Qt.AlignmentFlag.AlignTop)
        length_hbox.addWidget(self.reservation_length_price, alignment=Qt.AlignmentFlag.AlignTop)
        length_hbox.addStretch(1)
        reservation_length_label.setFixedWidth(label_width)
        self.reservation_length_data.setFixedWidth(data_width)
        self.reservation_layout.addLayout(length_hbox)

        # NUMBER OF RIDERS
        # Create QLabel for rider label
        rider_label = QLabel("Riders on Reservation: ")
        rider_label.setFont(QFont(self.font_light, 14))
        rider_label.setStyleSheet("color: #ffffff;")
        self.rider_layout.addWidget(rider_label)

        # Create QLabel for rider data
        self.rider_data = QLabel(f"{self.reservation_data.number_of_riders} riders")
        self.rider_data.setFont(bold_font)
        self.rider_data.setStyleSheet("color: #ffffff;")
        self.rider_layout.addWidget(self.rider_data)

        # Make hbox
        rider_hbox = QHBoxLayout()
        rider_hbox.addWidget(rider_label, alignment=Qt.AlignmentFlag.AlignTop)
        rider_hbox.addWidget(self.rider_data, alignment=Qt.AlignmentFlag.AlignTop)
        rider_hbox.addStretch(1)
        rider_label.setFixedWidth(label_width)
        self.rider_data.setFixedWidth(data_width)
        self.reservation_layout.addLayout(rider_hbox)

        # ADDITIONAL SERVICES
        # Create QLabel for additional services label
        additional_services_label = QLabel("Additional Services:")
        additional_services_label.setFont(QFont(self.font_light, 14))
        additional_services_label.setStyleSheet("color: #ffffff;")

        if self.reservation_data.additional_services:
            self.additional_service_names = []
            self.additional_service_prices = []
            for service in self.reservation_data.additional_services:
                self.additional_service_names.append(service.name)
                price = ""
                if service.price_for == "h":
                    price = service.price * int(self.reservation_data.reservation_length)
                elif service.price_for == "rider":
                    print(self.reservation_data.number_of_riders)
                    price = service.price * int(self.reservation_data.number_of_riders)

                self.additional_service_prices.append(str(price) + " $")

            self.additional_services_data = QLabel(f"{'<br>'.join(self.additional_service_names)}")
            self.additional_services_data.setFont(bold_font)
            self.additional_services_data.setStyleSheet("color: #ffffff;")

            self.additional_services_prices = QLabel(f"{'<br>'.join(self.additional_service_prices)}")
            self.additional_services_prices.setFont(bold_font)
            self.additional_services_prices.setStyleSheet("color: #ffffff;")

        else:
            self.additional_services_data = QLabel("None")

        additional_services_hbox = QHBoxLayout()
        additional_services_hbox.addWidget(additional_services_label, alignment=Qt.AlignmentFlag.AlignTop)
        additional_services_hbox.addWidget(self.additional_services_data, alignment=Qt.AlignmentFlag.AlignTop)
        additional_services_hbox.addWidget(self.additional_services_prices, alignment=Qt.AlignmentFlag.AlignTop)
        additional_services_hbox.addStretch(1)
        additional_services_label.setFixedWidth(label_width)
        self.additional_services_data.setFixedWidth(data_width)
        self.reservation_layout.addLayout(additional_services_hbox)

        # TOTAL PRICE
        # Create QLabel for total price label
        total_label = QLabel("Total price:")
        total_label.setFont(QFont(self.font_light, 14))
        total_label.setStyleSheet("color: #ffffff;")

        # Create QLabel for total data
        total_data = QLabel("-----------------------------------")
        total_data.setFont(QFont(self.font_light, 14))
        total_data.setStyleSheet("color: #ffffff;")

        # Create QLabel for actual total price
        the_price = 0
        for service in self.reservation_data.additional_services:
            price_for = service.price_for
            if price_for == "h":
                the_price += service.price * int(self.reservation_data.reservation_length)
            elif price_for == "jet_ski":
                the_price += service.price * 1
            elif price_for == "rider":
                the_price += service.price * int(self.reservation_data.number_of_riders)

        the_price += self.reservation_data.reservation_price
        self.total_price = QLabel(f"{the_price} $")
        self.total_price.setFont(bold_font)
        self.total_price.setStyleSheet("color: #ffffff;")

        # Make hbox
        total_price_hbox = QHBoxLayout()
        total_price_hbox.addWidget(total_label, alignment=Qt.AlignmentFlag.AlignTop)
        total_price_hbox.addWidget(total_data, alignment=Qt.AlignmentFlag.AlignTop)
        total_price_hbox.addWidget(self.total_price, alignment=Qt.AlignmentFlag.AlignTop)
        total_price_hbox.addStretch(1)
        total_label.setFixedWidth(label_width)
        total_data.setFixedWidth(data_width)
        self.reservation_layout.addLayout(total_price_hbox)

        # Customer
        # Create QLabel for customer label
        customer_label = QLabel("Customer:")
        customer_label.setFont(QFont(self.font_light, 14))
        customer_label.setStyleSheet("color: #ffffff;")

        # Create QLabel for customer data
        customer = self.reservation_data.customer
        if customer:
            self.customer_data = QLabel(
                f"{customer.first_name} {customer.last_name}\n{customer.email}\n{customer.phone_number}\n{customer.additional_info}")
        else:
            self.customer_data = QLabel("None")
        self.customer_data.setFont(bold_font)
        self.customer_data.setWordWrap(True)
        self.customer_data.setStyleSheet("color: #ffffff;")

        # Make hbox
        customer_hbox = QHBoxLayout()
        customer_hbox.addWidget(customer_label, alignment=Qt.AlignmentFlag.AlignTop)
        customer_hbox.addWidget(self.customer_data, alignment=Qt.AlignmentFlag.AlignTop)
        customer_hbox.addStretch(1)
        customer_label.setFixedWidth(label_width)
        self.customer_data.setFixedWidth(data_width)
        self.reservation_layout.addLayout(customer_hbox)

        self.jet_ski_layout.addWidget(self.jet_ski_image_label)
        self.details_layout.addLayout(self.jet_ski_layout)
        self.details_layout.addLayout(self.reservation_layout)

        self.next_button = QLabel("<strong>CONFIRM RESERVATION</strong>", self)
        self.next_button.setFixedWidth(300)
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

        # Add a spacer with a fixed height
        spacer = QSpacerItem(0, 50, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        self.main_layout.addItem(spacer)

        button_layout = QHBoxLayout()

        # Create a QLabel for the error message and set it as a class attribute
        self.error_message = QLabel(self)
        self.main_layout.addWidget(self.error_message)
        self.error_message.hide()  # Hide the label initially

        # Add stretches on both sides of the button to center it
        button_layout.addStretch()
        button_layout.addWidget(self.next_button)
        button_layout.addStretch()

        # Add the button layout to the main layout
        self.main_layout.addLayout(button_layout)

        # CREATE BOTTOM BAR AND ADD MAIN AND SET MAIN
        bottom_bar = BottomBar(self.page_index, True, True)

        self.main_layout.addStretch()
        self.main_layout.addWidget(bottom_bar)
        self.setLayout(self.main_layout)

    def update_info(self):
        # Update the reservation_data
        self.reservation_data = self.parent().property("reservation_data")

        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

        if self.reservation_data.jet_ski:
            jet_ski = self.reservation_data.jet_ski.replace(" ", "-")
            jet_ski_image_path = os.path.join(self.script_dir,
                                              f"assets/images/{jet_ski}/{jet_ski.lower().replace('-', '')}.png")
        else:
            jet_ski_image_path = os.path.join(script_dir, "assets/images/Sea-Doo-GTI-130/seadoogti130.png")

        # CHANGE JET SKI IMAGE TO JET_SKI_IMAGE_PATH
        self.jet_ski_image = QPixmap(jet_ski_image_path)
        self.jet_ski_image_label.setPixmap(self.jet_ski_image.scaled(360, 180, Qt.AspectRatioMode.KeepAspectRatio))

        # CHANGE JET SKI NAME
        self.jet_ski_data.setText(f"{self.reservation_data.jet_ski}")

        # CHANGE RESERVATION INFO TO reservation_info
        self.reservation_length_data.setText(f"{self.reservation_data.reservation_length} hours")
        self.reservation_date_data.setText(f"{self.reservation_data.reservation_date}")
        self.reservation_time_data.setText(f"{self.reservation_data.reservation_time}")
        self.rider_data.setText(f"{self.reservation_data.number_of_riders}")
        self.reservation_data.reservation_price = self.reservation_data.get_reservation_price(
            self.reservation_data.reservation_length)
        self.reservation_length_price.setText(f"{self.reservation_data.reservation_price} $")

        # Display additional services
        total_price = 0

        if self.reservation_data.additional_services:
            additional_service_names = []
            additional_service_prices = []

            for service in self.reservation_data.additional_services:
                additional_service_names.append(service.name)
                price = 0
                if service.price_for == "h":
                    price = int(service.price) * int(self.reservation_data.reservation_length)
                elif service.price_for == "rider":
                    price = int(service.price) * int(self.reservation_data.number_of_riders)
                elif service.price_for == "jet_ski":
                    price = int(service.price) * 1

                total_price += price

                additional_service_prices.append(str(price) + " $")

            self.additional_services_prices.setText(f"{'<br>'.join(additional_service_prices)}")
            self.additional_services_data.setText(f"{'<br>'.join(additional_service_names)}")
        else:
            self.additional_services_data.setText("None")
            self.additional_services_prices.setText("")

        total_price += self.reservation_data.get_reservation_price(self.reservation_data.reservation_length)
        self.total_price.setText(f"{total_price} $")
        self.reservation_data.reservation_price = total_price
        # Display customer details
        customer = self.reservation_data.customer
        if customer:
            additional_info = customer.additional_info
            if len(additional_info) > 25:
                additional_info = additional_info[:25] + "..."

            self.customer_data.setText(
                f"{customer.first_name} {customer.last_name}\n{customer.email}\n{customer.phone_number}\n{additional_info}")
        else:
            self.customer_data.setText("No additional requests")

        self.error_message.hide()
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
        self.next_button.setText("<strong>CONFIRM RESERVATION</strong>")
        self.next_button.mousePressEvent = lambda event: self.handle_next_button_click()


    def handle_next_button_click(self):

        success = self.add_reservation_to_google_sheets()
        if success:
            self.send_confirmation_email()
            success = True
            if success is True:
                # Call the update_info method of the next_age
                confirmation_screen = self.parent().widget(self.page_index + 1)
                confirmation_screen.update_info()
                # Go to next pag
                self.parent().setCurrentIndex(self.page_index + 1)

            elif success == "invalid_email":
                self.display_error_message("The email address is invalid. Please go back and check your email address.")
            else:
                self.display_error_message()
        else:
            self.display_error_message()

    def remove_reservation_from_google_sheets(self, reservation_data):
        try:
            # Set up the Google Sheets API client
            credentials = service_account.Credentials.from_service_account_file(self.SERVICE_ACCOUNT_FILE,
                                                                                scopes=self.SCOPES)
            service = build('sheets', 'v4', credentials=credentials)

            # Define the range and values to search for
            range_name = 'Reservations!A1:L'
            timestamp = reservation_data.timestamp

            # Get all the rows in the sheet
            result = service.spreadsheets().values().get(
                spreadsheetId=self.SHEET_ID, range=range_name).execute()
            rows = result.get('values', [])

            # Find the row index with the matching timestamp
            row_index = -1
            for i, row in enumerate(rows):
                if row[0] == timestamp:
                    row_index = i + 1
                    break

            if row_index > 0:
                # Delete the row with the matching timestamp
                body = {
                    'requests': [
                        {
                            'deleteDimension': {
                                'range': {
                                    'sheetId': 0,
                                    'dimension': 'ROWS',
                                    'startIndex': row_index - 1,
                                    'endIndex': row_index
                                }
                            }
                        }
                    ]
                }
                result = service.spreadsheets().batchUpdate(
                    spreadsheetId=self.SHEET_ID, body=body).execute()
                return True
            else:
                # Row not found
                print("Row not found in the sheet.")
                return False

        except HttpError as error:
            print(f"An error occurred: {error}")
            return False

    def add_reservation_to_google_sheets(self):
        # Add a timestamp to the reservation data
        self.reservation_data.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # reservation_data = self.parent().property("reservation_data")
        reservation_data = self.reservation_data

        try:
            # Set up the Google Sheets API client
            credentials = service_account.Credentials.from_service_account_file(self.SERVICE_ACCOUNT_FILE, scopes=self.SCOPES)
            service = build('sheets', 'v4', credentials=credentials)

            # Define the range and values to append
            range_name = 'Reservations!A1'
            values = [[
                reservation_data.reservation_number,
                reservation_data.timestamp,
                reservation_data.jet_ski,
                reservation_data.reservation_length,
                reservation_data.reservation_date,
                reservation_data.reservation_time,
                reservation_data.get_additional_services(),
                reservation_data.reservation_price,
                reservation_data.customer.first_name,
                reservation_data.customer.last_name,
                reservation_data.customer.email,
                reservation_data.customer.phone_number,
                reservation_data.customer.additional_info
            ]]

            # Append the values to the Google Sheet
            body = {'values': values}
            result = service.spreadsheets().values().append(
                spreadsheetId=self.SHEET_ID, range=range_name,
                valueInputOption='RAW', insertDataOption='INSERT_ROWS', body=body).execute()

            # Update the Availability sheet
            availability_range = 'Availability!A1:G'  # Adjust the range as needed
            availability_data = service.spreadsheets().values().get(spreadsheetId=self.SHEET_ID,
                                                                    range=availability_range).execute()
            availability_values = availability_data.get('values', [])

            date_index = 0
            time_index = 1
            jet_ski_index = None
            for index, jet_ski_name in enumerate(availability_values[0]):
                if jet_ski_name.strip().lower() == reservation_data.jet_ski.lower():
                    jet_ski_index = index
                    break

            if jet_ski_index is None:
                raise ValueError(f"Jet ski '{reservation_data.jet_ski}' not found in the Availability sheet header")

            start_time, end_time = reservation_data.reservation_time.split('-')

            for i, row in enumerate(availability_values[1:], start=1):  # Skip the header row
                if row[date_index].replace(" ", "") == reservation_data.reservation_date and start_time <= row[time_index].split('-')[0] < end_time:
                    update_range = f'Availability!{chr(jet_ski_index + 65)}{i + 1}'
                    update_body = {'values': [[reservation_data.reservation_number]]}
                    update_result = service.spreadsheets().values().update(
                        spreadsheetId=self.SHEET_ID, range=update_range,
                        valueInputOption='RAW', body=update_body).execute()

            return True

        except HttpError as error:
            print(f"An error occurred: {error}")
            return False

    def send_confirmation_email(self):
        # Set a timeout for all new socket objects
        socket.setdefaulttimeout(10)  # 10 seconds timeout

        # reservation_data = self.parent().property("reservation_data")
        reservation_data = self.reservation_data
        try:
            # Set up the email message
            msg = EmailMessage()

            # This is a plain-text fallback for email clients that do not support HTML.
            msg.set_content(f"""
                    Reservation details:
                    Jet ski: {reservation_data.jet_ski}
                    Reservation length: {reservation_data.reservation_length}
                    Reservation date: {reservation_data.reservation_date}
                    Reservation time: {reservation_data.reservation_time}
                    Additional services:
                    Customer details:
                    Name: {reservation_data.customer.first_name} {reservation_data.customer.last_name}
                    Email: {reservation_data.customer.email}
                    Phone: {reservation_data.customer.phone_number}
                    Additional info: {reservation_data.customer.additional_info}
                """)
            # Read the HTML content from the file

            with open(os.path.join(self.script_dir, 'assets/html/confirmation_email.html'), 'r') as file:
                html_content = file.read()

            # Replace placeholders with actual reservation data
            html_content = html_content.replace('{{order.order_id}}', reservation_data.reservation_number)
            html_content = html_content.replace('{{order.items.title}}', reservation_data.jet_ski + ", " + str(reservation_data.reservation_length) + " hours")
            html_content = html_content.replace('{{order.date}}', reservation_data.reservation_date + " " + reservation_data.reservation_time)
            html_content = html_content.replace('{{order.total.price}}', self.total_price.text())
            msg.add_alternative(html_content, subtype='html')

            msg['Subject'] = 'Hetijetti Reservation Confirmation'
            msg['From'] = 'vuokraus@hetijetti.fi'
            msg['To'] = reservation_data.customer.email
            # Set up the SMTP server
            server = smtplib.SMTP_SSL('mail.hetijetti.fi', 465)
            server.login('vuokraus@hetijetti.fi', 'Hetijetti2023')
            # Send the email
            server.send_message(msg)
            server.quit()
            # Reset the timeout to the system default
            socket.setdefaulttimeout(None)

            return True

        except socket.timeout:

            print("The mail server is not responding. Confirmation email not sent.")

            return False

        except Exception as error:

            print(f"An error occurred: {error}")

            if 'recipient address must contain a domain' in str(error):
                return "invalid_email"

            # Reset the timeout to the system default

            socket.setdefaulttimeout(None)

            return False

    def display_error_message(self, custom_message=None):
        error_color = "#FF9482"

        # Update the next button style, text, and disable it
        self.next_button.setText("<strong>CLOSE PROGRAM</strong>")
        self.next_button.setStyleSheet(f"""
            * {{
                border: 2px solid {error_color};
                color: {error_color};
                background-color: rgba(255, 255, 255, 0);
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: 400;
            }}
            *:hover{{
                border: 2px solid {error_color};
                color: rgba(0, 0, 0, 1);
                background-color: {error_color};
            }}
        """)

        if custom_message is not None:
            message = custom_message
        else:
            message = "Something went wrong in the reservation system. Please contact us directly via phone or email to make a reservation."

        self.error_message.setText(message)

        self.error_message.setStyleSheet(f"color: {error_color}; font-weight: bold;")
        self.error_message.setWordWrap(True)
        self.error_message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_message.setGeometry(50, 100, 500, 100)  # Adjust the position and size as needed
        self.error_message.show()  # Show the label

        # Update the button click event to close the program
        self.next_button.mousePressEvent = lambda event: QApplication.instance().quit()
