"""
main.py
"""

from PyQt6.QtWidgets import QApplication
import sys
from modules.main_window import MainWindow


def main():
    """
    Main function to run the PyQt6 application.
    This function initializes the QApplication, creates the main window,
    and starts the event loop.
    Attributes:
        None
    """
    try:
        app = QApplication(sys.argv)
        main_window = MainWindow()
        main_window.show()
        sys.exit(app.exec())
    except Exception as e:
        import traceback

        with open("error_log.txt", "w") as f:
            f.write(f"Error: {e}\n")
            f.write(traceback.format_exc())


if __name__ == "__main__":
    main()
