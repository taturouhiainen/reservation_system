import os
import sys
from PyQt6.QtGui import QPixmap, QFont, QFontDatabase
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QWidget, QVBoxLayout
from PyQt6.QtCore import QDate, Qt, pyqtSignal
import re
import csv
from functools import partial
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class HoverImageLabel(QLabel):
    clicked = pyqtSignal()

    active_image = None  # This attribute will store the currently active image
    active_jet_ski = None  # This attribute will store the name of the currently active jet ski

    def __init__(self, path_to_og, path_to_op, header_label, parent=None):
        super().__init__(parent)
        self.path_to_og = path_to_og
        self.path_to_op = path_to_op
        self.header_label = header_label
        pixmap = QPixmap(self.path_to_op).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
        self.setPixmap(pixmap)

    def enterEvent(self, event):
        pixmap = QPixmap(self.path_to_og).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
        self.setPixmap(pixmap)

    def leaveEvent(self, event):
        if self != HoverImageLabel.active_image:
            pixmap = QPixmap(self.path_to_op).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
            self.setPixmap(pixmap)

    def set_active(self, active):
        if active:
            HoverImageLabel.active_image = self
            pixmap = QPixmap(self.path_to_og).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
            self.header_label.setStyleSheet("color: #ffffff; text-transform: uppercase; font-weight: 800;")

        else:
            pixmap = QPixmap(self.path_to_op).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
            self.header_label.setStyleSheet("color: #ffffff; text-transform: uppercase; font-weight: 400;")

        self.setPixmap(pixmap)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if HoverImageLabel.active_image is not None and HoverImageLabel.active_image != self:
                HoverImageLabel.active_image.set_active(False)

            self.set_active(True)
            self.clicked.emit()


class ClickableTimeSlotLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def mousePressEvent(self, event):
        self.clicked.emit()


class WeekSelector(QWidget):

    def __init__(self):
        super().__init__()
        self.page_index = 1

        # Get the directory of the current script
        self.script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

        # Construct the font path relative to the script directory
        font_path_light = os.path.join(self.script_dir, "assets/fonts/Montserrat/static/Montserrat-Light.ttf")
        font_path_bold = os.path.join(self.script_dir, "assets/fonts/Montserrat/static/Montserrat-Bold.ttf")

        # ID
        font_id_light = QFontDatabase.addApplicationFont(font_path_light)
        font_id_bold = QFontDatabase.addApplicationFont(font_path_bold)

        # Create the fonts
        self.font_light = QFontDatabase.applicationFontFamilies(font_id_light)
        self.font_bold = QFontDatabase.applicationFontFamilies(font_id_bold)

        self.available_time_slots = None
        self.time_slots_layouts = None
        self.all_available_time_slots = None
        self.time_slot_labels = None
        self.first_time = True
        self.header_labels = []
        # Get the information from the previous page
        self.length = 1

        self.selected_day_label = None
        self.selected_date = None
        self.active_time_slot_label = None

        self.selected_year = 2023
        self.start_season = QDate(self.selected_year, 5, 1)  # 1st of May
        self.end_season = QDate(self.selected_year, 9, 30)  # Last day of September

        # Get the start of the week and set the date format
        self.current_date = QDate.currentDate()

        self.active_image = None
        self.active_jet_ski = None
        self.active_date = None

        self.SHEET_ID = '1PNneUFO2xL7he9pND-Qo6EQV6hNvVWXz40Hs07EdPrY'
        self.SERVICE_ACCOUNT_FILE = 'assets/json/hetijetti-5dc8c0072bd2.json'
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

        self.fetch_data_from_google_sheets(self.SHEET_ID, self.SERVICE_ACCOUNT_FILE, self.SCOPES)

        # Calculate the starting date based on the season constraints
        if self.current_date < self.start_season:
            self.starting_date = self.start_season
        elif self.current_date > self.end_season:
            self.selected_year += 1
            self.starting_date = QDate(self.selected_year, 5, 1)
        else:
            self.starting_date = self.current_date.addDays(1)

        # Find the start of the week (Monday) of the starting_date
        days_to_monday = self.starting_date.dayOfWeek() - 1
        self.week_start = self.starting_date.addDays(-days_to_monday)
        self.week_end = self.week_start.addDays(6)

        self.date_format = "dd/MM"

        # Set up the layout
        self.main_layout = QVBoxLayout
        self.layout = QHBoxLayout()
        self.mama_time_layout = QVBoxLayout()
        self.header_layout = QHBoxLayout()
        self.time_slots_layout = QVBoxLayout()
        self.next_button_layout = QHBoxLayout()

        self.layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.time_slots_layout.setContentsMargins(130, 20, 130, 0)
        self.next_button_layout.setContentsMargins(0, 20, 0, 0)

        # Add each day of the week to the layout
        self.days = []
        for i in range(9):

            if i == 0:

                # Create a label for the arrow
                arrow_path = os.path.join(self.script_dir, "assets/images/previousfade.png")
                arrow_pixmap = QPixmap(arrow_path).scaled(15, 20)
                arrow_label = QLabel()
                arrow_label.setPixmap(arrow_pixmap)
                arrow_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

                # Add some space at the top of the arrow's layout
                arrow_layout = QVBoxLayout()
                empty_space = QLabel("", self)
                empty_space.setFixedSize(15, 25)
                arrow_layout.addWidget(empty_space)  # empty label with fixed height
                arrow_layout.addWidget(arrow_label)
                arrow_layout.addStretch()

                # Add the vertical layout to the main layout
                self.layout.addLayout(arrow_layout)

                self.previous_arrow_label = arrow_label

            elif i == 8:

                # Create a label for the arrow
                arrow_path = os.path.join(self.script_dir, "assets/images/next.png")
                arrow_pixmap = QPixmap(arrow_path).scaled(15, 20)
                arrow_label = QLabel()
                arrow_label.setPixmap(arrow_pixmap)
                arrow_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
                arrow_label.setCursor(Qt.CursorShape.PointingHandCursor)

                # Add some space at the top of the arrow's layout
                arrow_layout = QVBoxLayout()
                empty_space = QLabel("", self)
                empty_space.setFixedSize(15, 25)
                arrow_layout.addWidget(empty_space)  # empty label with fixed height
                arrow_layout.addWidget(arrow_label)
                arrow_layout.addStretch()

                # Add the vertical layout to the main layout
                self.layout.addLayout(arrow_layout)
                arrow_label.mousePressEvent = lambda event: self.next_week()

            else:
                current_day = self.week_start.addDays(i - 1)
                current_day_str = current_day.toString("ddd")
                current_date_str = current_day.toString(self.date_format)

                # Create a label for the day, date, and calendar icon
                day_label = QLabel()
                self.day_label = QLabel()
                day_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

                day_font = QFont()
                day_font.setBold(True)
                day_label.setFont(day_font)

                date_font = QFont()
                date_font.setPointSize(10)

                day_label.setFixedWidth(50)
                day_label.setFixedHeight(70)
                day_label.setStyleSheet("QLabel:hover { background-color: white; border-radius: 5px }")

                if self.starting_date == current_day:
                    calendar_path = os.path.join(self.script_dir, "assets/images/calendar.png")
                    self.day_label.setText(
                        f"<span style='font-size: 14px;'>{current_day_str}</span><br><span style='font-size: 10px;'>"
                        f"{current_date_str}</span><br><img src='{calendar_path}' width='15' height='15'>")
                    day_label.setText(
                        f"<span style='font-size: 14px;'>{current_day_str}</span><br><span style='font-size: 10px;'>"
                        f"{current_date_str}</span><br><img src='{calendar_path}' width='15' height='15'>")
                    day_label.setStyleSheet("QLabel { background-color: white; border-radius: 5px }")
                    day_label.setCursor(Qt.CursorShape.PointingHandCursor)
                    day_label.setMouseTracking(True)
                    day_label.mousePressEvent = lambda event, day_label=day_label: self.handle_date_click(day_label)
                    self.selected_date = current_day
                    self.selected_day_label = current_date_str
                    self.handle_date_click(day_label)

                elif self.starting_date > current_day:
                    disabled_path = os.path.join(self.script_dir, "assets/images/disabled.png")
                    day_label.setText(
                        f"<span style='font-size: 14px;'>{current_day_str}</span><br><span style='font-size: 10px;'>"
                        f"{current_date_str}</span><br><img src='{disabled_path}' width='15' height='15'>")
                    day_label.setStyleSheet(
                        "QLabel { background-color: transparent; border-radius: 5px; color: #242526 }")
                    day_label.setCursor(Qt.CursorShape.ArrowCursor)
                    day_label.setMouseTracking(False)

                elif self.starting_date < current_day:
                    calendar_path = os.path.join(self.script_dir, "assets/images/calendar.png")
                    day_label.setText(
                        f"<span style='font-size: 14px;'>{current_day_str}</span><br><span style='font-size: 10px;'>"
                        f"{current_date_str}</span><br><img src='{calendar_path}' width='15' height='15'>")
                    day_label.setStyleSheet("QLabel:hover { background-color: white; border-radius: 5px; color:  }")
                    day_label.setCursor(Qt.CursorShape.PointingHandCursor)
                    day_label.setMouseTracking(True)
                    day_label.mousePressEvent = lambda event, day_label=day_label: self.handle_date_click(day_label)
                # Add the label to a layout
                day_layout = QVBoxLayout()
                day_layout.addWidget(day_label)
                day_layout.addStretch()

                self.layout.addLayout(day_layout)

                self.days.append(day_label)

        # Set the widget's layout
        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.layout)
        self.mama_time_layout.addLayout(self.header_layout)
        self.mama_time_layout.addLayout(self.time_slots_layout)
        self.main_layout.addLayout(self.mama_time_layout)
        self.main_layout.addLayout(self.next_button_layout)
        self.setLayout(self.main_layout)

        # Create the pill-shaped button
        self.next_button = QLabel("<strong>NEXT</strong><br>(choose a time)", self)
        self.next_button.setFixedWidth(200)
        self.next_button.setFont(QFont(self.font_bold, 14))
        self.next_button.setStyleSheet("""
            * {
                color: rgba(255, 255, 255, 0.7);
                background-color: rgba(255, 255, 255, 0.3);
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: 400;
            }
        """)
        self.next_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.next_button.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.next_button.setMouseTracking(True)

        # Add the button to the next_button_layout
        self.next_button_layout.addWidget(self.next_button)

    def handle_date_click(self, day_label):
        s = day_label.text()
        match = re.search(r'\d{2}/\d{2}', s)

        if match:
            full_date_format = f"dd/MM/yyyy"
            self.selected_date = QDate.fromString(f"{match.group()}/{self.selected_year}", full_date_format)
            self.selected_day_label = self.selected_date.toString(self.date_format)

        for day in self.days:
            s_two = day.text()
            match_two = re.search(r'\d{2}/\d{2}', s_two)
            stripped_date = match_two.group()

            # To compare these strings we have to turn them into datetime objects

            stripped_format = "%d/%m/%Y"
            selected_year = self.selected_year
            stripped_date = datetime.strptime(f"{stripped_date}/{selected_year}", stripped_format).date()
            selected_date = datetime.strptime(f"{self.selected_day_label}/{selected_year}", stripped_format).date()
            starting_date = datetime.strptime(self.starting_date.toString("dd/MM/yyyy"), stripped_format).date()

            # If the current loaded day object is before the first day of where we start loading days from
            if stripped_date < starting_date:
                day.setStyleSheet(
                    "QLabel { background-color: transparent; border-radius: 5px; color: #242526 } "
                    "QLabel:hover { background-color: transparent;}")

            # If the current loaded day object is the selected date
            elif stripped_date == selected_date:
                day.setStyleSheet("QLabel { background-color: white; border-radius: 5px }")

            # If the current loaded day object is after the first day of where we start loading days from
            elif selected_date > starting_date:
                day.setStyleSheet(
                    "QLabel { background-color: transparent; border-radius: 5px; color: #242526 } "
                    "QLabel:hover { background-color: white; border-radius: 5px }")

            # Else idk
            else:
                day.setStyleSheet(
                    "QLabel { background-color: transparent; border-radius: 5px } "
                    "QLabel:hover { background-color: white; border-radius: 5px }")

        # NOW GET THE AVAILABLE DATES WITH CLICK OF THE DATE

        selected_date_str = self.selected_date.toString("dd/MM/yyyy")
        self.available_time_slots, self.all_available_time_slots = \
            self.get_available_time_slots(selected_date_str, self.length)

        self.display_header_images(self.available_time_slots)
        self.display_available_time_slots(self.available_time_slots, self.all_available_time_slots)

    def next_week(self):
        new_week_start = self.week_start.addDays(7)
        new_week_end = self.week_end.addDays(7)

        # Check if the new dates are beyond 24th September 2023
        if new_week_start <= QDate(2023, 9, 24) and new_week_end <= QDate(2023, 9, 24):
            self.week_start = new_week_start
            self.week_end = new_week_end
            self.update_calendar()

    def previous_week(self):

        self.week_start = self.week_start.addDays(-7)
        self.week_end = self.week_end.addDays(-7)
        self.update_calendar()

    def update_calendar(self):

        can_go_to_previous_week = self.week_start > self.starting_date

        if can_go_to_previous_week:
            previous_path = os.path.join(self.script_dir, "assets/images/previous.png")
            self.previous_arrow_label.setPixmap(QPixmap(previous_path).scaled(15, 20))
            self.previous_arrow_label.setCursor(Qt.CursorShape.PointingHandCursor)
            self.previous_arrow_label.mousePressEvent = lambda event: self.previous_week()
        else:
            previous_fade_path = os.path.join(self.script_dir, "assets/images/previousfade.png")
            self.previous_arrow_label.setPixmap(QPixmap(previous_fade_path).scaled(15, 20))
            self.previous_arrow_label.unsetCursor()
            self.previous_arrow_label.mousePressEvent = None

        for i, day_label in enumerate(self.days):

            current_day = self.week_start.addDays(i)
            current_day_str = current_day.toString("ddd")
            current_date_str = current_day.toString(self.date_format)
            # The rest of the code from the next_week() method related to updating the day_labels
            if self.selected_date and current_day == self.selected_date:
                # Highlight the originally selected date
                calendar_path = os.path.join(self.script_dir, "assets/images/calendar.png")
                day_label.setText(
                    f"<span style='font-size: 14px;'>{current_day_str}</span><br><span style='font-size: 10px;'>"
                    f"{current_date_str}</span><br><img src='{calendar_path}' width='15' height='15'>")
                day_label.setStyleSheet("QLabel { background-color: white; border-radius: 5px }")
                day_label.setCursor(Qt.CursorShape.PointingHandCursor)
                day_label.setMouseTracking(True)
                day_label.mousePressEvent = lambda event, day_label=day_label: self.handle_date_click(day_label)

            elif current_day < self.starting_date:
                disabled_path = os.path.join(self.script_dir, "assets/images/disabled.png")
                day_label.setText(
                    f"<span style='font-size: 14px;'>{current_day_str}</span><br><span style='font-size: 10px;'>"
                    f"{current_date_str}</span><br><img src='{disabled_path}' width='15' height='15'>")
                day_label.setStyleSheet("QLabel { background-color: transparent; border-radius: 5px; color: #242526 }")
                day_label.setCursor(Qt.CursorShape.ArrowCursor)
                day_label.setMouseTracking(False)

            elif current_day >= self.starting_date:
                calendar_path = os.path.join(self.script_dir, "assets/images/calendar.png")
                day_label.setText(
                    f"<span style='font-size: 14px;'>{current_day_str}</span><br><span style='font-size: 10px;'>"
                    f"{current_date_str}</span><br><img src='{calendar_path}' width='15' height='15'>")
                day_label.setStyleSheet("QLabel:hover { background-color: white; border-radius: 5px; color:  }")
                day_label.setCursor(Qt.CursorShape.PointingHandCursor)
                day_label.setMouseTracking(True)
                day_label.mousePressEvent = lambda event, day_label=day_label: self.handle_date_click(day_label)

    @staticmethod
    def get_available_time_slots(date, reservation_length):

        actual_reservation_length = reservation_length
        if reservation_length == 24:
            # We actually need to only search for 12 hour slots
            # As hour 22-10 are off the clock
            reservation_length = 12

        # Read the CSV file
        file = "availability.csv"
        with open(file, "r") as csvfile:
            csvreader = csv.reader(csvfile)
            day_data = []
            jet_ski_names = next(csvreader)[2:]

            # Iterate through each row in the CSV

            for row in csvreader:

                if row[0] == date:
                    day_data.append(row)

            # Get the total number of jet skis
            irrelevant_rows = 2
            num_jet_skis = len(day_data[0]) - irrelevant_rows

            all_jet_skis_available_time_slots = {}

            # ADD THE FIRST ITEM: ALL TIME SLOTS
            all_slots = []
            all_slots_dict = {}

            latest_possible_time_str = day_data[-1][1].split("-")[1]
            latest_possible_time = datetime.strptime(latest_possible_time_str, "%H:%M")
            for row in day_data:
                time_slot = row[1]
                start_time = time_slot.split("-")[0]
                end_time = datetime.strptime(start_time, "%H:%M") + timedelta(hours=reservation_length)
                if end_time > latest_possible_time:
                    break
                else:
                    if actual_reservation_length == 24:
                        time_slot = start_time + "-" + start_time + " (24h)"
                        all_slots.append(time_slot)
                    else:
                        end_time = end_time.strftime("%H:%M")
                        time_slot = start_time + "-" + end_time
                        all_slots.append(time_slot)

            all_slots_dict["ALL"] = all_slots

            # Let's append a fake row to day_data so that it also check the last row
            day_data.append("END00")
            # ADD THE AVAILABLE TIME SLOTS FOR EACH JET SKI
            for jet_ski_index in range(2, num_jet_skis + 2):

                available_time_slots = []
                counter = 1
                i = 0

                for row in day_data:

                    is_available = not row[jet_ski_index]

                    if counter > reservation_length:
                        end_time = day_data[i - 1][1].split("-")[1]
                        end_time_dt = datetime.strptime(end_time, "%H:%M")
                        start_time_dt = end_time_dt - timedelta(hours=reservation_length)
                        start_time = start_time_dt.strftime("%H:%M")
                        if actual_reservation_length == 24:
                            available_time_slots.append(start_time + "-" + start_time + " (24h)")
                        else:
                            available_time_slots.append(start_time + "-" + end_time)

                    if is_available:
                        counter += 1
                    else:
                        counter = 1

                    i += 1

                # Store the available time slots for the current jet ski in the dictionary
                all_jet_skis_available_time_slots[jet_ski_names[jet_ski_index-irrelevant_rows]] = available_time_slots

        return all_jet_skis_available_time_slots, all_slots_dict

    def display_header_images(self, available_time_slots):
        self.clear_layout(self.header_layout)
        jet_ski_names = list(available_time_slots.keys())
        middle_index = len(jet_ski_names) // 2
        i = 0

        for jet_ski_name, time_slots in available_time_slots.items():
            jet_ski_layout = QVBoxLayout()

            # Create a header with the jet ski name
            header_label = QLabel(jet_ski_name)
            header_label.setFont(QFont(self.font_bold, 16))
            header_label.setStyleSheet("color: #ffffff; text-transform: uppercase; font-weight: 400;")
            header_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            jet_ski_layout.addWidget(header_label)

            # Get images
            jet_ski_folder = jet_ski_name.replace(" ", "-")
            jet_ski_file = jet_ski_name.replace(" ", "").replace("-", "").lower()

            path_to_op = os.path.join(self.script_dir, "assets/images/" + jet_ski_folder + "/" + jet_ski_file + "op.png")
            path_to_og = os.path.join(self.script_dir, "assets/images/" + jet_ski_folder + "/" + jet_ski_file + ".png")

            # Add the image below the header_label
            image_label = HoverImageLabel(path_to_og, path_to_op, header_label)
            image_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            jet_ski_layout.addWidget(image_label)
            image_label.setCursor(Qt.CursorShape.PointingHandCursor)

            # Connect the click event to the handle_jet_ski_click method
            image_label.clicked.connect(partial(self.handle_jet_ski_click, image_label, jet_ski_name))

            # Set the middle image as active by default
            if i == middle_index and not self.active_jet_ski:
                image_label.set_active(True)
                self.active_jet_ski = jet_ski_name
                self.active_image = image_label
            elif jet_ski_name == self.active_jet_ski:
                image_label.set_active(True)

            self.header_layout.addLayout(jet_ski_layout)
            # Add the header_label to the header_labels list
            self.header_labels.append(header_label)
            i += 1

    def display_available_time_slots(self, available_time_slots, all_available_time_slots):
        self.clear_layout(self.time_slots_layout)

        i = 0
        current_row_layout = QHBoxLayout()
        self.time_slots_layout.addLayout(current_row_layout)
        self.time_slot_labels = []

        for index, (key, all_time_slots) in enumerate(all_available_time_slots.items()):

            every_other = True
            for time_slot in all_time_slots:

                # A - 2-3-2-3... 7, 4, 2, 1
                # B - 3-2-3-2... 8, 5
                # C - 3-3-3-3... 9, 6, 3
                # D - 3-4-3... 10
                # E - 4-3-4... 11
                # F - 4-4-4... 12

                # F
                if len(all_time_slots) >= 12:
                    if i % 4 == 0 and i > 0:
                        current_row_layout = QHBoxLayout()
                        self.time_slots_layout.addLayout(current_row_layout)
                # E
                elif len(all_time_slots) == 11:
                    if every_other:
                        if i % 4 == 0 and i > 0:
                            current_row_layout = QHBoxLayout()
                            self.time_slots_layout.addLayout(current_row_layout)
                            every_other = False
                            i = 0
                    else:
                        if i % 3 == 0 and i > 0:
                            current_row_layout = QHBoxLayout()
                            self.time_slots_layout.addLayout(current_row_layout)
                            every_other = True
                            i = 0
                # D
                elif len(all_time_slots) == 10:
                    if every_other:
                        if i % 3 == 0 and i > 0:
                            current_row_layout = QHBoxLayout()
                            self.time_slots_layout.addLayout(current_row_layout)
                            every_other = False
                            i = 0
                    else:
                        if i % 4 == 0 and i > 0:
                            current_row_layout = QHBoxLayout()
                            self.time_slots_layout.addLayout(current_row_layout)
                            every_other = True
                            i = 0
                # C
                elif len(all_time_slots) in [3, 6, 9]:
                    if i % 3 == 0 and i > 0:
                        current_row_layout = QHBoxLayout()
                        self.time_slots_layout.addLayout(current_row_layout)
                # B
                elif len(all_time_slots) in [5, 8]:
                    if every_other:
                        if i % 3 == 0 and i > 0:
                            current_row_layout = QHBoxLayout()
                            self.time_slots_layout.addLayout(current_row_layout)
                            every_other = False
                            i = 0
                    else:
                        if i % 2 == 0 and i > 0:
                            current_row_layout = QHBoxLayout()
                            self.time_slots_layout.addLayout(current_row_layout)
                            every_other = True
                            i = 0

                elif len(all_time_slots) in [1, 2, 4, 7]:
                    if every_other:
                        if i % 2 == 0 and i > 0:
                            current_row_layout = QHBoxLayout()
                            self.time_slots_layout.addLayout(current_row_layout)
                            every_other = False
                            i = 0
                    else:
                        if i % 3 == 0 and i > 0:
                            current_row_layout = QHBoxLayout()
                            self.time_slots_layout.addLayout(current_row_layout)
                            every_other = True
                            i = 0
                # Check if the time slot is available
                if time_slot in available_time_slots[self.active_jet_ski]:
                    time_slot_label = ClickableTimeSlotLabel(time_slot)
                    time_slot_label.setFont(QFont(self.font_light, 14))
                    time_slot_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
                    time_slot_label.setFixedWidth(120)

                    if self.length == 24:
                        time_slot_label.setFixedWidth(150)
                    else:
                        time_slot_label.setFixedWidth(120)

                    time_slot_label.setFixedHeight(30)
                    time_slot_label.setCursor(Qt.CursorShape.PointingHandCursor)
                    time_slot_label.setStyleSheet("""
                                                        * {
                                                           color: #ffffff;
                                                           border: 2px solid #ffffff;
                                                           border-radius: 5px;
                                                           padding: 4px 8px;
                                                           background-color: transparent;
                                                           font-size: 14px;
                                                           }
                                                           *:hover {
                                                           background-color: #ffffff;
                                                           color: #000000;
                                                           }
                                                        """)
                    time_slot_label.clicked.connect(
                        lambda ts_label=time_slot_label: self.set_active_time_slot(ts_label))
                    self.time_slot_labels.append(time_slot_label)
                else:
                    time_slot_label = QLabel(time_slot)
                    time_slot_label.setFont(QFont(self.font_light, 14))
                    time_slot_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
                    time_slot_label.setFixedWidth(120)
                    time_slot_label.setFixedHeight(30)
                    time_slot_label.setCursor(Qt.CursorShape.ForbiddenCursor)
                    time_slot_label.setStyleSheet("""
                                                        * {
                                                           color: #000000;
                                                           border: 2px solid rgba(0,0,0,0.3);
                                                           border-radius: 5px;
                                                           padding: 4px 8px;
                                                           background-color: transparent;
                                                           font-size: 14px;
                                                           }
                                                    
                                                        """)

                current_row_layout.addWidget(time_slot_label)
                i += 1

        self.mama_time_layout.setSpacing(20)

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget:
                    # Remove the widget from the layout and hide it
                    layout.removeWidget(widget)
                    widget.hide()
                elif item.layout():
                    # Recursively clear nested layouts
                    self.clear_layout(item.layout())
                    # Remove the nested layout from the parent layout
                    layout.removeItem(item)

    def display_time_slots(self, jet_ski_name, show):
        time_slots_layout = self.time_slots_layouts[jet_ski_name]
        for i in range(time_slots_layout.count()):
            widget = time_slots_layout.itemAt(i).widget()
            if show:
                widget.show()
            else:
                widget.hide()

    def on_image_clicked(self, clicked_image_label):
        if self.active_image != clicked_image_label:
            self.active_image = clicked_image_label

    def set_active_time_slot(self, active_label):
        # Reset all time slots to the default style
        self.active_time_slot_label = active_label.text()

        # Connect the button to the function
        self.next_button.mousePressEvent = lambda event: self.handle_next_button_click()

        self.next_button.setText("<strong>CONFIRM</strong><br>"
                                 + self.selected_day_label
                                 + "/"
                                 + str(self.selected_year)
                                 + " "
                                 + active_label.text()
                                 + "<br>"
                                 + self.active_jet_ski)
        self.next_button.setStyleSheet("""
                    * {
                        color: #FFFFFF;
                        border: 2px solid rgb(255, 255, 255);
                        border-radius: 5px;
                        padding: 8px 16px;
                        font-weight: 400;
                    }
                    *:hover {
                        color: #000000;
                        background-color: rgb(255, 255, 255);
                    }
                """)
        self.next_button.setCursor(Qt.CursorShape.PointingHandCursor)

        for label in self.time_slot_labels:
            label.setStyleSheet("""
                * {
                   color: #ffffff;
                   border: 2px solid #ffffff;
                   border-radius: 5px;
                   padding: 4px 8px;
                   background-color: transparent;
                   font-size: 14px;
                   }
                   *:hover {
                   background-color: #ffffff;
                   color: #000000;
                   }
            """)

        # Set the active time slot to the selected style
        active_label.setStyleSheet("""
            * {
               color: #000000;
               border: 2px solid rgb(73, 255, 96);
               border-radius: 5px;
               padding: 4px 8px;
               background-color: rgb(73, 255, 96);
               font-size: 14px;
               }
               *:hover {
               background-color: rgb(73, 255, 96);
               color: #000000;
               }
        """)

    @staticmethod
    def fetch_data_from_google_sheets(sheet_id, service_account_file, scopes):
        from google.oauth2 import service_account
        from googleapiclient.discovery import build

        credentials = service_account.Credentials.from_service_account_file(service_account_file, scopes=scopes)
        service = build('sheets', 'v4', credentials=credentials)

        range_name = 'Availability!A:Z'  # Adjust the range as needed
        result = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=range_name).execute()
        values = result.get('values', [])

        # Pad the rows with empty strings
        max_columns = max([len(row) for row in values])
        for row in values:
            row.extend([''] * (max_columns - len(row)))

        # Save the data to a CSV file
        with open('availability.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(values)

    def handle_jet_ski_click(self, image_label, jet_ski_name):
        # Set the previous active image to inactive
        if self.active_image:
            self.active_image.set_active(False)

        # Set the new active image and update the active_jet_ski
        image_label.set_active(True)
        self.active_image = image_label
        self.active_jet_ski = jet_ski_name

        # Trigger the display_available_time_slots method
        self.display_available_time_slots(self.available_time_slots, self.all_available_time_slots)

    def handle_next_button_click(self):

        # Update reservation infor
        self.parent().parent().property("reservation_data").jet_ski = self.active_jet_ski
        self.parent().parent().property("reservation_data").reservation_length = self.length
        self.parent().parent().property("reservation_data").reservation_date = \
            self.selected_day_label + "/" + str(self.selected_year)
        self.parent().parent().property("reservation_data").reservation_time = self.active_time_slot_label

        # Activate the check fuel service from the next screen
        next_screen = self.parent().parent().widget(self.page_index + 1)
        next_screen.check_fuel_service()

        self.parent().parent().setCurrentIndex(self.page_index + 1)
