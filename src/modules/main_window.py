from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 Desktop Application")
        self.setGeometry(100, 100, 800, 600)

        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        label = QLabel("Welcome to the PyQt6 Desktop Application!")
        layout.addWidget(label)

        central_widget.setLayout(layout)