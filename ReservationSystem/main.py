import sys
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QLabel
from screens.ReservationLengthScreen import ReservationLengthScreen
from screens.DateSelectionScreen import DateSelectionScreen
from screens.AdditionalServicesScreen import AdditionalServicesScreen
from screens.CustomerInformationScreen import CustomerInformationScreen
from screens.ConfirmationDetailsScreen import ConfirmationDetailsScreen
from screens.ConfirmationScreen import ConfirmationScreen
from classes.ReservationData import ReservationData
from screens.SafetyGuidelinesScreen import SafetyGuidelinesScreen
from screens.CancellationPolicyScreen import CancellationPolicyScreen


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Setting the window title - this is visible for the whole reservation system
        self.setWindowTitle("Hetijetti - Jet Ski Rental System")

        self.stacked_widget = QStackedWidget()

        # Make the reservation data instance, and set it as a property of the stacked_widget
        # This is so that we can access it from every screen of the reservation system
        self.reservation_data = ReservationData()
        self.stacked_widget.setProperty("reservation_data", self.reservation_data)

        # Add all the screens to the stacked widget
        self.reservation_length_screen = ReservationLengthScreen(self.stacked_widget)
        self.date_selection_screen = DateSelectionScreen(self.stacked_widget)
        self.additional_services_screen = AdditionalServicesScreen(self.stacked_widget)
        self.customer_information_screen = CustomerInformationScreen(self.stacked_widget)
        self.confirmation_details_screen = ConfirmationDetailsScreen(self.stacked_widget)
        self.confirmation_screen = ConfirmationScreen(self.stacked_widget)
        self.safety_screen = SafetyGuidelinesScreen(self.stacked_widget)
        self.policy_screen = CancellationPolicyScreen(self.stacked_widget)

        # Initializing the basic user interface for the reservation system
        self.init_ui()

    def init_ui(self):

        # Setting the size
        self.setFixedSize(800, 600)

        # Setting the background image
        background_label = QLabel(self)
        pixmap = QPixmap("assets/images/background.jpg")
        background_label.setPixmap(pixmap)
        background_label.setGeometry(0, 0, self.width(), self.height())

        # Set up the stacked widget for displaying different screens
        self.setCentralWidget(self.stacked_widget)

        # Add all the screens to the stacked_widget as widgets   |   here are the indexes
        self.stacked_widget.addWidget(self.reservation_length_screen)       # 0
        self.stacked_widget.addWidget(self.date_selection_screen)           # 1
        self.stacked_widget.addWidget(self.additional_services_screen)      # 2
        self.stacked_widget.addWidget(self.customer_information_screen)     # 3
        self.stacked_widget.addWidget(self.confirmation_details_screen)     # 4
        self.stacked_widget.addWidget(self.confirmation_screen)             # 5
        self.stacked_widget.addWidget(self.safety_screen)                   # 6
        self.stacked_widget.addWidget(self.policy_screen)                   # 7

        # Set the first screen to be displayed - rest are assigned in their respective files
        self.stacked_widget.setCurrentIndex(0)

        # Show the UI to the user
        self.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec())
