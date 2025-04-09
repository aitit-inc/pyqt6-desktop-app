"""
This module contains the MainWindow class for the PyQt6 desktop application.
The MainWindow class is responsible for setting up the main window of the application,
including its title, size, and layout.
"""

from PyQt6.QtWidgets import (
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QWidget,
    QMenuBar,
    QMenu,
    QApplication,
    QStackedWidget,
)
from PyQt6.QtCore import Qt

from modules.notepad import Notepad
from modules.image_viewer import ImageViewer
from modules.pdf_viewer import PDFViewer


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

        # Create stacked widget to hold all our applications
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Initialize applications
        self.init_welcome_screen()
        self.init_applications()

        # Show welcome screen by default
        self.stacked_widget.setCurrentIndex(0)

        # Create menu bar
        self.create_menu_bar()

    def init_welcome_screen(self):
        """
        Initialize the welcome screen.
        """
        welcome_widget = QWidget()
        layout = QVBoxLayout()

        layout.addStretch()
        self.welcome_label = QLabel("Welcome to the PyQt6 Desktop Application!")
        layout.addWidget(self.welcome_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

        welcome_widget.setLayout(layout)
        self.stacked_widget.addWidget(welcome_widget)

    def init_applications(self):
        """
        Initialize all application widgets.
        """
        # Create all application instances
        self.notepad = Notepad(self)
        self.image_viewer = ImageViewer(self)
        self.pdf_viewer = PDFViewer(self)

        # Add them to the stacked widget
        self.stacked_widget.addWidget(self.notepad)
        self.stacked_widget.addWidget(self.image_viewer)
        self.stacked_widget.addWidget(self.pdf_viewer)

    def create_menu_bar(self):
        """
        Creates the menu bar with options for demo applications.
        """
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        # Create Demo menu
        demo_menu = QMenu("Demo", self)
        menu_bar.addMenu(demo_menu)

        # Add actions for each application
        notepad_action = demo_menu.addAction("メモ帳")
        notepad_action.triggered.connect(self.open_notepad)

        image_viewer_action = demo_menu.addAction("イメージビューア")
        image_viewer_action.triggered.connect(self.open_image_viewer)

        pdf_viewer_action = demo_menu.addAction("PDFビューア")
        pdf_viewer_action.triggered.connect(self.open_pdf_viewer)

        # Add Home menu option
        home_action = demo_menu.addAction("ホーム")
        home_action.triggered.connect(self.show_welcome_screen)

    def open_notepad(self):
        """
        Opens the notepad application.
        """
        self.stacked_widget.setCurrentWidget(self.notepad)

    def open_image_viewer(self):
        """
        Opens the image viewer application.
        """
        self.stacked_widget.setCurrentWidget(self.image_viewer)

    def open_pdf_viewer(self):
        """
        Opens the PDF viewer application.
        """
        self.stacked_widget.setCurrentWidget(self.pdf_viewer)

    def show_welcome_screen(self):
        """
        Show the welcome screen.
        """
        self.stacked_widget.setCurrentIndex(0)
