from PyQt5.QtCore import QFile
from os.path import sep
from os import getcwd


def load_stylesheet(sheet_name: str):
    base_style_path = ''.join([getcwd(), sep, "resources", sep, "stylesheets"])
    with open(''.join([base_style_path, sep, sheet_name])) as st_file:
        style = st_file.read()
    return style
