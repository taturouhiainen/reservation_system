import os
import sys
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont, QFontDatabase
from classes.BottomBar import BottomBar
from classes.AdditionalService import AdditionalService
from classes.general import init_fonts


# Class for an additional service button
class ServiceButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def enterEvent(self, event):
        if self.property("is_added"):
            self.setText("Remove Service?")
        super().enterEvent(event)

    def leaveEvent(self, event):
        if self.property("is_added"):
            self.setText("Service Added ✓")
        super().leaveEvent(event)


class AdditionalServicesScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.page_index = 2
        self.added_services = []
        self.setGeometry(20, 20, 700, 350)
        script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

        # Creating the layouts
        self.main_layout = QVBoxLayout()
        self.header_layout = QVBoxLayout()
        self.additional_services_layout = QHBoxLayout()
        self.next_button_layout = QHBoxLayout()

        # Adding the layouts
        self.main_layout.addLayout(self.header_layout)
        self.main_layout.addStretch()
        self.main_layout.addLayout(self.additional_services_layout)
        self.main_layout.addLayout(self.next_button_layout)

        # INITIALIZING FONT
        # Construct the font path relative to the script directory
        font_path_light = os.path.join(script_dir, "assets/fonts/Montserrat/static/Montserrat-Light.ttf")
        font_path_bold = os.path.join(script_dir, "assets/fonts/Montserrat/static/Montserrat-Bold.ttf")

        # ID
        font_id_light = QFontDatabase.addApplicationFont(font_path_light)
        font_id_bold = QFontDatabase.addApplicationFont(font_path_bold)

        # Create the fonts
        font_light = QFontDatabase.applicationFontFamilies(font_id_light)[0]
        font_bold = QFontDatabase.applicationFontFamilies(font_id_bold)[0]

        # INITIALIZING UI
        # Title
        title = QLabel("Enhance your jet ski adventure!", self)
        title.setFont(QFont(font_light, 30))
        title.setStyleSheet("color: #ffffff; text-transform: uppercase;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFixedHeight(80)

        title.setMaximumHeight(100)
        self.header_layout.addWidget(title)
        self.header_layout.setSpacing(20)

        # Let's create a for loop that makes the button for each Jet Ski
        additional_services = [
            AdditionalService("Wet Suits", 10, "rider", "10$ per rider",
                              os.path.join(script_dir, "assets/images/services/wetsuit.png"),
                              "Stay comfortable and protected during your jet ski ride "
                              "with our high-quality wetsuits in a range of sizes."),
            AdditionalService("Fuel Service", 30, "h", "30$ per hour",
                              os.path.join(script_dir, "assets/images/services/fuel1f.png"),
                              "Focus on having a great time "
                              "on the water while we take care of refueling for you."),
            AdditionalService("Snacks & Beverages", 20, "jet_ski", "20$ per jet ski",
                              os.path.join(script_dir, "assets/images/services/snacks.png"),
                              "A curated selection of "
                              "tasty treats and thirst-quenching drinks, "
                              "so you can stay energized and hydrated "
                              "on the water.")
        ]

        colors = ["#00bcd4", "#49FF60", "#FF9482"]
        i = 0

        for additional_service in additional_services:
            self.additional_service_layout = QVBoxLayout()
            name = additional_service.get_name()
            description = additional_service.get_description()
            image = additional_service.get_image()
            price_text = additional_service.get_price_desc()
            color = colors[i]

            # Create the title label for the additional service
            title_label = QLabel(name, self)
            title_label.setFont(QFont(font_bold, 20))
            title_label.setStyleSheet("color: #ffffff; text-transform: uppercase;"
                                      "font-weight: 600")
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            title_label.setFixedHeight(30)

            # Create the price label for the additional service
            price_text_split = price_text.split(" ")
            price_text = price_text_split[0]
            price_text = f"<strong>{price_text}</strong> {' '.join(price_text_split[1:])}"

            price_label = QLabel(price_text, self)
            price_label.setFont(QFont(font_light, 15))
            price_label.setStyleSheet(f"color: {color}; "
                                      "text-transform: uppercase;"
                                      "font-weight: 100;"
                                      "")
            price_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            price_label.setFixedHeight(30)

            # Create the image label for the additional service
            image_label = QLabel(self)
            image_label.setPixmap(QPixmap(image))
            image_label.setScaledContents(True)
            image_label.setFixedSize(150, 150)
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Create the description label for the additional service
            description_label = QLabel(description, self)
            description_label.setFont(QFont(font_light, 12))
            description_label.setStyleSheet("color: #ffffff; font-weight: 500;")
            description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            description_label.setWordWrap(True)
            description_label.setFixedHeight(100)
            description_label.setProperty("service_name", name)

            button = ServiceButton(self)
            button.setText("Add Service")
            button.setFixedWidth(250)
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
                          color: #FFFFFF !important;
                          }}
                          """

            button.setStyleSheet(button_stylesheet)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(self.button_clicked)
            button.setFont(QFont(font_bold))

            # Set custom properties for the button
            button.setProperty("service", additional_service)
            button.setProperty("service_name", name)
            button.setProperty("is_added", False)
            button.setProperty("original_color", color)

            self.additional_service_layout.addWidget(title_label)
            self.additional_service_layout.addWidget(price_label)
            self.additional_service_layout.addWidget(image_label)
            self.additional_service_layout.addWidget(description_label)
            self.additional_service_layout.addWidget(button)
            self.additional_service_layout.addStretch()
            self.additional_service_layout.setAlignment(image_label, Qt.AlignmentFlag.AlignHCenter)
            self.additional_services_layout.addLayout(self.additional_service_layout)
            i += 1

        # Next button to move to next screen
        self.next_button = QLabel("<strong>NEXT</strong>", self)
        self.next_button.setFixedWidth(200)
        self.next_button.setFont(QFont(font_bold, 14))
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
        bottom_bar = BottomBar(self.page_index, True, True)
        self.main_layout.addStretch()
        self.main_layout.addWidget(bottom_bar)
        self.setLayout(self.main_layout)

    # If an additional service button is clicked, this triggers
    def button_clicked(self):
        button = self.sender()
        is_added = button.property("is_added")

        if is_added:
            self.remove_service(button)
        else:
            self.add_service(button)

    # Function to add service to reservation
    def add_service(self, button):
        button.setProperty("is_added", True)
        button.setText("Service Added ✓")
        button.setStyleSheet("""
            * {
                border: 2px solid rgba(255,255,255,0.8);
                border-radius: 5px;
                color: rgba(255,255,255,0.8);
                background-color: rgba(0,0,0,0);
                font-size: 16px;
                font-weight: 800 !important;
                height: 50px;
                text-transform: uppercase;
                opacity: 0.7;
            }

            *:hover {
                background-color: rgba(255,255,255,0.5);
                color: #FFFFFF !important;
            }
        """)

        service = button.property("service")
        self.added_services.append(service)

    # Function to remove service from resrevation
    def remove_service(self, button):
        button.setProperty("is_added", False)
        button.setText("Add Service")
        color = button.property("original_color")  # Retrieve the original color
        button.setStyleSheet(f"""
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
                color: #FFFFFF !important;
            }}
        """)

        service = button.property("service")
        self.added_services.remove(service)

    # Function to handle next button click, set reservation data and take to next page
    def handle_next_button_click(self):

        self.parent().property("reservation_data").additional_services = self.added_services
        self.parent().setCurrentIndex(self.page_index + 1)

    # Function to check if fuel service is available
    def check_fuel_service(self):
        reservation_data = self.parent().property("reservation_data")

        if int(reservation_data.reservation_length) > 5:
            fuel_service_button = None
            fuel_service_desc = None

            for child in self.findChildren(QPushButton):
                if child.property("service_name") == "Fuel Service":
                    fuel_service_button = child
                    break

            if fuel_service_button is not None:
                color = "rgba(255,255,255,0.5)"
                fuel_service_button.setText("NOT AVAILABLE")
                fuel_service_button.setCursor(Qt.CursorShape.ForbiddenCursor)
                fuel_service_button.setEnabled(False)
                fuel_service_button.setStyleSheet(f"""
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
                """)

            for child in self.findChildren(QLabel):
                if child.property("service_name") == "Fuel Service":
                    fuel_service_desc = child
                    break

            if fuel_service_desc is not None:
                fuel_service_desc.setText("Sorry, this service is not available for over 5 hour long reservations. "
                                          "We expect you to take care of the refueling.")
                fuel_service_desc.setStyleSheet("color:rgba(255,255,255,0.65);")
