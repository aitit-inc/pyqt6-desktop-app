"""
This module contains the MainWindow class for the PyQt6 desktop application.
The MainWindow class is responsible for setting up the main window of the application,
including its title, size, and layout.
"""

from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    """
    MainWindow class for the PyQt6 desktop application.
    This class inherits from QMainWindow and sets up the main window of the application.
    Attributes:
        None
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 Desktop Application")
        self.setGeometry(100, 100, 800, 600)

        self.initUI()

    def initUI(self):
        """
        Initializes the user interface of the main window.
        This method sets up the layout and widgets for the main window.
        """
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        label = QLabel("Welcome to the PyQt6 Desktop Application!")
        layout.addWidget(label)

        central_widget.setLayout(layout)
