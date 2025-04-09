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

        self.initUI()
        self.create_menu_bar()

    def initUI(self):
        """
        Initializes the user interface of the main window.
        This method sets up the layout and widgets for the main window.
        """
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.addStretch()  # 上部の余白を追加
        self.welcome_label = QLabel("Welcome to the PyQt6 Desktop Application!")
        layout.addWidget(
            self.welcome_label, alignment=Qt.AlignmentFlag.AlignCenter
        )  # 中央配置
        layout.addStretch()  # 下部の余白を追加

        central_widget.setLayout(layout)

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

    def open_notepad(self):
        """
        Opens the notepad application.
        """
        self.welcome_label.setVisible(False)
        self.notepad = Notepad(self)
        self.setCentralWidget(self.notepad)

    def open_image_viewer(self):
        """
        Opens the image viewer application.
        """
        self.welcome_label.setVisible(False)
        self.image_viewer = ImageViewer(self)
        self.setCentralWidget(self.image_viewer)

    def open_pdf_viewer(self):
        """
        Opens the PDF viewer application.
        """
        self.welcome_label.setVisible(False)
        self.pdf_viewer = PDFViewer(self)
        self.setCentralWidget(self.pdf_viewer)
