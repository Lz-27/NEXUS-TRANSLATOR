import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from model import TranslatorModel
from view import TranslatorView
from controller import TranslatorController

def main():
    # Set high DPI support for clearer fonts
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Set global font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Initialize MVC components
    model = TranslatorModel()
    
    # Pass available languages to the View
    available_langs = model.get_languages()
    view = TranslatorView(available_langs)
    
    # Controller connects Model and View
    controller = TranslatorController(model, view)
    
    view.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
