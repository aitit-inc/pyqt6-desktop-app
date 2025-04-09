"""
Image Viewer module for the PyQt6 desktop application.
Provides functionality for opening and viewing image files with zoom capabilities.
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QFileDialog,
    QScrollArea,
    QMessageBox,
)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
import os


class ImageViewer(QWidget):
    """
    Image Viewer class for displaying images with zoom capabilities.
    Provides a simple interface for opening and viewing image files.
    """

    def __init__(self, parent=None):
        """
        Initialize the Image Viewer widget.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.current_image_path = None
        self.zoom_factor = 1.0
        self.setup_ui()

    def setup_ui(self):
        """
        Set up the user interface components.
        """
        layout = QVBoxLayout()

        # Scroll area for the image
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Image label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_area.setWidget(self.image_label)

        layout.addWidget(self.scroll_area)

        # Button layout
        button_layout = QHBoxLayout()

        # Open image button
        self.open_button = QPushButton("画像を開く")
        self.open_button.clicked.connect(self.open_image)
        button_layout.addWidget(self.open_button)

        # Zoom in button
        self.zoom_in_button = QPushButton("拡大")
        self.zoom_in_button.clicked.connect(self.zoom_in)
        self.zoom_in_button.setEnabled(False)
        button_layout.addWidget(self.zoom_in_button)

        # Zoom out button
        self.zoom_out_button = QPushButton("縮小")
        self.zoom_out_button.clicked.connect(self.zoom_out)
        self.zoom_out_button.setEnabled(False)
        button_layout.addWidget(self.zoom_out_button)

        # Reset zoom button
        self.reset_zoom_button = QPushButton("元のサイズに戻す")
        self.reset_zoom_button.clicked.connect(self.reset_zoom)
        self.reset_zoom_button.setEnabled(False)
        button_layout.addWidget(self.reset_zoom_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def open_image(self):
        """
        Open an image file and display it.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "画像ファイルを開く",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif);;All Files (*)",
        )

        if file_path:
            try:
                self.load_image(file_path)
                self.current_image_path = file_path
                self.zoom_factor = 1.0
                self.zoom_in_button.setEnabled(True)
                self.zoom_out_button.setEnabled(True)
                self.reset_zoom_button.setEnabled(True)
            except Exception as e:
                QMessageBox.warning(self, "エラー", f"画像を開けませんでした: {e}")

    def load_image(self, file_path):
        """
        Load and display the image from the specified file path.

        Args:
            file_path: Path to the image file
        """
        self.image = QImage(file_path)
        if self.image.isNull():
            raise ValueError("Invalid image format")

        self.original_pixmap = QPixmap.fromImage(self.image)
        self.update_image()

    def update_image(self):
        """
        Update the displayed image based on the current zoom factor.
        """
        if hasattr(self, "original_pixmap"):
            scaled_width = int(self.original_pixmap.width() * self.zoom_factor)
            scaled_height = int(self.original_pixmap.height() * self.zoom_factor)

            scaled_pixmap = self.original_pixmap.scaled(
                scaled_width,
                scaled_height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

            self.image_label.setPixmap(scaled_pixmap)

    def zoom_in(self):
        """
        Increase zoom factor by 20%.
        """
        self.zoom_factor *= 1.2
        self.update_image()

    def zoom_out(self):
        """
        Decrease zoom factor by 20%.
        """
        self.zoom_factor /= 1.2
        self.update_image()

    def reset_zoom(self):
        """
        Reset zoom factor to 1.0 (original size).
        """
        self.zoom_factor = 1.0
        self.update_image()
