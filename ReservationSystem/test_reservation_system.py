import unittest
from unittest.mock import Mock, call
import sys
from PyQt6.QtWidgets import QApplication
from classes.myCalendar import WeekSelector
from classes.ReservationData import ReservationData
from classes.Customer import Customer
from classes.AdditionalService import AdditionalService
from classes.BottomBar import BottomBar
from classes.ProgressBar import ProgressBar
from classes.JetSki import JetSki
from screens.CustomerInformationScreen import CustomerInformationScreen
from screens.ConfirmationDetailsScreen import ConfirmationDetailsScreen

class TestReservationSystem(unittest.TestCase):

    def setUp(self):
        self.app = QApplication(sys.argv)
        self.weekSelector = WeekSelector()
        self.reservation_data = ReservationData()
        self.customer = Customer("Erkki", "Eerikki", "erkki@erkki.com", "1234567890", "Kissan synttarit")

    def test_reservation_data_initialization(self):
        # Check if the attributes are initialized with the correct default values
        self.assertIsNone(self.reservation_data.reservation_number)
        self.assertIsNone(self.reservation_data.jet_ski)
        self.assertIsNone(self.reservation_data.reservation_length)
        self.assertIsNone(self.reservation_data.reservation_date)
        self.assertIsNone(self.reservation_data.reservation_time)
        self.assertIsNone(self.reservation_data.reservation_price)
        self.assertIsNone(self.reservation_data.additional_services)
        self.assertIsNone(self.reservation_data.customer)
        self.assertIsNone(self.reservation_data.confirmation_details)
        self.assertIsNone(self.reservation_data.timestamp)

    def test_setting_reservation_data(self):
        # Set the attributes of the ReservationData instance
        self.reservation_data.jet_ski = "Sea-Doo GTI 130"
        self.reservation_data.reservation_length = 2
        self.reservation_data.reservation_date = "2023/05/05"
        self.reservation_data.reservation_time = "10:00-12:00"
        self.reservation_data.additional_services = ["Life Jackets", "Snacks"]
        self.reservation_data.customer = {"name": "Erkki Eerikki", "email": "erkki@erkki.com"}
        self.reservation_data.confirmation_details = {"booking_id": "12345", "price": 200}

        # Check if the attributes were set correctly
        self.assertEqual(self.reservation_data.jet_ski, "Sea-Doo GTI 130")
        self.assertEqual(self.reservation_data.reservation_length, 2)
        self.assertEqual(self.reservation_data.reservation_date, "2023/05/05")
        self.assertEqual(self.reservation_data.reservation_time, "10:00-12:00")
        self.assertEqual(self.reservation_data.additional_services, ["Life Jackets", "Snacks"])
        self.assertEqual(self.reservation_data.customer, {"name": "Erkki Eerikki", "email": "erkki@erkki.com"})
        self.assertEqual(self.reservation_data.confirmation_details, {"booking_id": "12345", "price": 200})

    def test_customer_initialization(self):
        # Check if the attributes are initialized with the correct values
        self.assertEqual(self.customer.first_name, "Erkki")
        self.assertEqual(self.customer.last_name, "Eerikki")
        self.assertEqual(self.customer.email, "erkki@erkki.com")
        self.assertEqual(self.customer.phone_number, "1234567890")
        self.assertEqual(self.customer.additional_info, "Kissan synttarit")

    def test_customer_initialization_with_missing_data(self):
        with self.assertRaises(TypeError):
            # Missing the 'additional_info' field
            Customer("Erkki", "Eerikki", "erkki@erkki.com", "1234567890")

    def test_customer_initialization_with_invalid_data(self):
        with self.assertRaises(TypeError):
            # Invalid email address
            Customer("Erkki", "Eerikki", "1234567890", "Kissan synttarit")

    def test_jetski_initialization(self):
        # Create an instance of the JetSki class
        jetski = JetSki(1, "Sea-Doo GTI 130", "Red", True, "Fast and reliable")

        # Check if the attributes are initialized with the correct values
        self.assertEqual(jetski.id, 1)
        self.assertEqual(jetski.label, "Sea-Doo GTI 130")
        self.assertEqual(jetski.color, "Red")
        self.assertTrue(jetski.availability)
        self.assertEqual(jetski.additional_info, "Fast and reliable")

    def test_additional_service_initialization(self):
        # Create an instance of the AdditionalService class
        additional_service = AdditionalService("Life Jacket", 10, "per hour", "$10/hour", "image.jpg",
                                               "Keep safe with our life jackets")

        # Check if the attributes are initialized with the correct values
        self.assertEqual(additional_service.name, "Life Jacket")
        self.assertEqual(additional_service.price, 10)
        self.assertEqual(additional_service.price_for, "per hour")
        self.assertEqual(additional_service.price_desc, "$10/hour")
        self.assertEqual(additional_service.image, "image.jpg")
        self.assertEqual(additional_service.description, "Keep safe with our life jackets")

    def test_get_available_start_times(self):
        # Case 1: A valid date and length with available start times
        date_1 = "30/05/2023"
        length_1 = 2

        result_1 = self.weekSelector.get_available_time_slots(date_1, length_1)
        print(result_1)
        self.assertIsInstance(result_1, tuple)  # Checks if tuple
        self.assertGreater(len(result_1), 0)  # Checks if empty

        # Case 2: A valid date and length with no available start times
        date_2 = "03/05/2023"
        length_2 = 12

        result_2 = self.weekSelector.get_available_time_slots(date_2, length_2)
        all_empty = all(len(value) == 0 for value in result_2[0].values())
        self.assertTrue(all_empty)

        # Case 3: An invalid date or length
        date_3 = "1990-200.56"
        length_3 = -1

        with self.assertRaises(IndexError):
            self.weekSelector.get_available_time_slots(date_3, length_3)

    def test_additional_service_to_dict(self):
        # Create an instance of the AdditionalService class
        additional_service = AdditionalService(
            "Life Jacket",
            10,
            "per hour",
            "$10/hour",
            "image.jpg",
            "Keep safe with our life jackets"
        )

        # Call to_dict on the instance and store the result
        result = additional_service.to_dict()

        # Check that the result is a dictionary with the correct values
        expected_result = {
            "name": "Life Jacket",
            "price": 10,
            "unit": "per hour",
            "price_info": "$10/hour",
            "image_path": "image.jpg",
            "description": "Keep safe with our life jackets"
        }
        self.assertEqual(result, expected_result)

    def test_generate_unique_reservation_number(self):
        result = CustomerInformationScreen.generate_unique_reservation_number()
        timestamp, random_string = result.split('-')

        self.assertTrue(timestamp.isdigit())
        self.assertEqual(len(random_string), 5)
        self.assertTrue(random_string.isalnum())


if __name__ == "__main__":
    unittest.main()
