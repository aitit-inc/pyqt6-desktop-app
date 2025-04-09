"""
Notepad module for the PyQt6 desktop application.
Provides functionality for creating, editing, and saving text files.
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QPushButton,
    QHBoxLayout,
    QFileDialog,
    QMessageBox,
)
from PyQt6.QtCore import Qt


class Notepad(QWidget):
    """
    Notepad class for text editing functionality.
    Provides a simple interface for creating, editing, and saving text files.
    """

    def __init__(self, parent=None):
        """
        Initialize the Notepad widget.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.current_file = None
        self.setup_ui()

    def setup_ui(self):
        """
        Set up the user interface components.
        """
        layout = QVBoxLayout()

        # Text editing area
        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        # Button layout
        button_layout = QHBoxLayout()

        # New file button
        self.new_button = QPushButton("新規")
        self.new_button.clicked.connect(self.new_file)
        button_layout.addWidget(self.new_button)

        # Open file button
        self.open_button = QPushButton("開く")
        self.open_button.clicked.connect(self.open_file)
        button_layout.addWidget(self.open_button)

        # Save file button
        self.save_button = QPushButton("保存")
        self.save_button.clicked.connect(self.save_file)
        button_layout.addWidget(self.save_button)

        # Save As button
        self.save_as_button = QPushButton("名前を付けて保存")
        self.save_as_button.clicked.connect(self.save_file_as)
        button_layout.addWidget(self.save_as_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def new_file(self):
        """
        Create a new file, clearing the current content.
        """
        if self.maybe_save():
            self.text_edit.clear()
            self.current_file = None

    def open_file(self):
        """
        Open a text file and load its content.
        """
        if self.maybe_save():
            file_path, _ = QFileDialog.getOpenFileName(
                self, "テキストファイルを開く", "", "Text Files (*.txt);;All Files (*)"
            )

            if file_path:
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        self.text_edit.setText(file.read())
                    self.current_file = file_path
                except Exception as e:
                    QMessageBox.warning(
                        self, "エラー", f"ファイルを開けませんでした: {e}"
                    )

    def save_file(self):
        """
        Save the current file or open Save As dialog if no file is open.
        """
        if self.current_file:
            return self.save_to_file(self.current_file)
        return self.save_file_as()

    def save_file_as(self):
        """
        Save the current content to a new file.
        """
        file_path, _ = QFileDialog.getSaveFileName(
            self, "テキストファイルを保存", "", "Text Files (*.txt);;All Files (*)"
        )

        if not file_path:
            return False

        return self.save_to_file(file_path)

    def save_to_file(self, file_path):
        """
        Save content to the specified file path.

        Args:
            file_path: Path to save the file

        Returns:
            bool: True if save was successful, False otherwise
        """
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(self.text_edit.toPlainText())
            self.current_file = file_path
            return True
        except Exception as e:
            QMessageBox.warning(self, "エラー", f"ファイルを保存できませんでした: {e}")
            return False

    def maybe_save(self):
        """
        Check if there are unsaved changes and prompt the user to save them.

        Returns:
            bool: True if okay to proceed, False to cancel the operation
        """
        if not self.text_edit.document().isModified():
            return True

        response = QMessageBox.question(
            self,
            "未保存の変更",
            "ドキュメントに未保存の変更があります。保存しますか？",
            QMessageBox.StandardButton.Save
            | QMessageBox.StandardButton.Discard
            | QMessageBox.StandardButton.Cancel,
        )

        if response == QMessageBox.StandardButton.Save:
            return self.save_file()
        elif response == QMessageBox.StandardButton.Cancel:
            return False

        return True
