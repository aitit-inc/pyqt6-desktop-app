# PyQt6 Desktop Application

This project is a simple desktop application built using PyQt6. It serves as a template for creating modular PyQt6 applications.

## Project Structure

```
pyqt6-desktop-app
├── src
│   ├── main.py               # Entry point of the application
│   ├── modules               # Contains application modules
│   │   ├── __init__.py       # Marks the modules directory as a package
│   │   └── main_window.py     # Main window logic
│   └── ui                    # Contains UI files
│       └── main_window.ui    # Qt Designer file for the main window
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd pyqt6-desktop-app
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:

```
python src/main.py
```

This will launch the main window of the application. You can modify the `main_window.py` file to customize the functionality and appearance of the main window.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.