# Hetijetti Reservation System

## Introduction

This project is a comprehensive reservation system for jet skis, created as part of Y2 Ohjelmoinnin Peruskurssi.
The application allows users to select a date, choose a jet ski, and reserve it for a certain duration.
It also includes additional features such as adding additional services, custom calendar widget and a confirmation email.
The system is integrated with Google Sheets for data management and uses a clean, user-friendly interface designed with PyQt6.


## File and directory structure

The project is structured in several directories:

assets: Contains various resources used by the application, organized in subdirectories:
    csv: Contains csv files used by the application.
    fonts: Contains font files used in the application UI.
    html: Contains HTML files used by the application.
    images: Contains images and icons used in the application.
    json: Contains JSON files used by the application.

classes: Contains Python files for the classes used in the application. These files define the objects used in the system, such as JetSki, Customer, ReservationData, etc.

screens: Contains Python files for each screen in the application. These files define the user interface and behavior of each screen in the system.

in the main directory are located availability.csv used to store data fetched from Google Sheets, as well as the unit tests and the main.py file.


## Installation instructions

This project requires Python 3.10 or higher and the following Python libraries:

PyQt6
Google Sheets API

You can install the necessary libraries using pip:
    pip install pyqt6
    pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib


## User instructions

To start the application, navigate to the project directory in your command line or terminal and run the following command:

python main.py

(or execute the main.py file)
The application is graphical, and once launched, the user interface guides you through the reservation process.
There are no additional command-line commands or setup files required to use the program.
