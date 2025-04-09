"""
PDF Viewer module for the PyQt6 desktop application.
Provides functionality for opening and viewing PDF files with scrolling capabilities.
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QFileDialog,
    QMessageBox,
    QScrollArea,
    QLabel,
    QSizePolicy,
)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt, QBuffer, QIODevice
from PyPDF2 import PdfReader
import io


class PDFViewer(QWidget):
    """
    PDF Viewer class for displaying PDF files with scrolling capabilities.
    Provides a simple interface for opening and viewing PDF files.
    """

    def __init__(self, parent=None):
        """
        Initialize the PDF Viewer widget.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.current_pdf_path = None
        self.current_page = 0
        self.total_pages = 0
        self.pdf_reader = None
        self.setup_ui()

    def setup_ui(self):
        """
        Set up the user interface components.
        """
        layout = QVBoxLayout()

        # Scroll area for the PDF content
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # PDF content label
        self.pdf_label = QLabel("PDFファイルを開いてください")
        self.pdf_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pdf_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.scroll_area.setWidget(self.pdf_label)

        layout.addWidget(self.scroll_area)

        # Navigation buttons layout
        nav_layout = QHBoxLayout()

        # Open PDF button
        self.open_button = QPushButton("PDFを開く")
        self.open_button.clicked.connect(self.open_pdf)
        nav_layout.addWidget(self.open_button)

        # Previous page button
        self.prev_button = QPushButton("前のページ")
        self.prev_button.clicked.connect(self.prev_page)
        self.prev_button.setEnabled(False)
        nav_layout.addWidget(self.prev_button)

        # Page indicator
        self.page_label = QLabel("0 / 0")
        nav_layout.addWidget(self.page_label)

        # Next page button
        self.next_button = QPushButton("次のページ")
        self.next_button.clicked.connect(self.next_page)
        self.next_button.setEnabled(False)
        nav_layout.addWidget(self.next_button)

        layout.addLayout(nav_layout)
        self.setLayout(layout)

    def open_pdf(self):
        """
        Open a PDF file and display its first page.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self, "PDFファイルを開く", "", "PDF Files (*.pdf);;All Files (*)"
        )

        if file_path:
            try:
                self.load_pdf(file_path)
                self.current_pdf_path = file_path
                self.current_page = 0
                self.update_navigation_buttons()
                self.render_current_page()
            except Exception as e:
                QMessageBox.warning(self, "エラー", f"PDFを開けませんでした: {e}")

    def load_pdf(self, file_path):
        """
        Load a PDF file from the specified path.

        Args:
            file_path: Path to the PDF file
        """
        self.pdf_reader = PdfReader(file_path)
        self.total_pages = len(self.pdf_reader.pages)

        if self.total_pages == 0:
            raise ValueError("PDFにページがありません")

    def render_current_page(self):
        """
        Render the current PDF page and display it.
        """
        if not self.pdf_reader or self.current_page >= self.total_pages:
            return

        # Update page indicator
        self.page_label.setText(f"{self.current_page + 1} / {self.total_pages}")

        try:
            # For PyQt6, we need to render PDF page as an image
            # This is a simplified version - in a production app, you might want
            # to use a dedicated PDF rendering library like PyMuPDF

            # Get the current page
            page = self.pdf_reader.pages[self.current_page]

            # Create a blank image with some default size
            # Note: This is a simplified approach. Real implementation would extract
            # page dimensions and render at appropriate resolution
            from PIL import Image, ImageDraw

            img = Image.new("RGB", (800, 1100), (255, 255, 255))
            draw = ImageDraw.Draw(img)

            # Draw some page info as this is just a demo
            draw.text((50, 50), f"Page {self.current_page + 1}", fill=(0, 0, 0))
            draw.text((50, 100), "PDF content would be rendered here", fill=(0, 0, 0))
            draw.text((50, 150), f"File: {self.current_pdf_path}", fill=(0, 0, 0))

            # Convert PIL Image to QImage
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)

            qimage = QImage.fromData(buffer.getvalue())
            pixmap = QPixmap.fromImage(qimage)

            self.pdf_label.setPixmap(pixmap)

        except Exception as e:
            self.pdf_label.setText(f"ページの読み込みエラー: {e}")

    def next_page(self):
        """
        Navigate to the next page of the PDF.
        """
        if self.pdf_reader and self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.update_navigation_buttons()
            self.render_current_page()

    def prev_page(self):
        """
        Navigate to the previous page of the PDF.
        """
        if self.pdf_reader and self.current_page > 0:
            self.current_page -= 1
            self.update_navigation_buttons()
            self.render_current_page()

    def update_navigation_buttons(self):
        """
        Update the state of navigation buttons based on the current page.
        """
        if not self.pdf_reader:
            self.prev_button.setEnabled(False)
            self.next_button.setEnabled(False)
            return

        self.prev_button.setEnabled(self.current_page > 0)
        self.next_button.setEnabled(self.current_page < self.total_pages - 1)
