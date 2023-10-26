import sys
import os
from PyQt6.QtGui import QFontDatabase


def init_fonts():
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

    # Construct the font path relative to the script directory
    font_path_light = os.path.join(script_dir, "assets/fonts/Montserrat/static/Montserrat-Light.ttf")
    font_path_bold = os.path.join(script_dir, "assets/fonts/Montserrat/static/Montserrat-Bold.ttf")

    # ID
    font_id_light = QFontDatabase.addApplicationFont(font_path_light)
    font_id_bold = QFontDatabase.addApplicationFont(font_path_bold)

    # Create the fonts
    font_light = QFontDatabase.applicationFontFamilies(font_id_light)[0]
    font_bold = QFontDatabase.applicationFontFamilies(font_id_bold)[0]

    return font_light, font_bold
