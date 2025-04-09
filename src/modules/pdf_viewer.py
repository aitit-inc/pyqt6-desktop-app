"""
PDF Viewer module for the PyQt6 desktop application.
Provides functionality for opening and viewing PDF files with scrolling capabilities.

reference: https://github.com/BBC-Esq/PyQt6-PDF-Viewer
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QFileDialog,
    QMessageBox,
)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage


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
        self.setup_ui()

    def setup_ui(self):
        """
        Set up the user interface components.
        """
        layout = QVBoxLayout()

        # Web view for PDF rendering
        self.web_view = QWebEngineView()
        self.web_view.settings().setAttribute(
            self.web_view.settings().WebAttribute.PluginsEnabled, True
        )
        self.web_view.settings().setAttribute(
            self.web_view.settings().WebAttribute.PdfViewerEnabled, True
        )

        # Set default content
        self.web_view.setHtml(
            """
            <html>
            <body style="display: flex; justify-content: center; align-items: center; height: 100vh; font-family: Arial, sans-serif;">
                <div style="text-align: center;">
                    <h2>PDFビューア</h2>
                    <p>「PDFを開く」ボタンをクリックしてPDFファイルを表示します</p>
                </div>
            </body>
            </html>
            """
        )

        layout.addWidget(self.web_view)

        # Button layout
        button_layout = QHBoxLayout()

        # Open PDF button
        self.open_button = QPushButton("PDFを開く")
        self.open_button.clicked.connect(self.open_pdf)
        button_layout.addWidget(self.open_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def open_pdf(self):
        """
        Open a PDF file and display it.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self, "PDFファイルを開く", "", "PDF Files (*.pdf);;All Files (*)"
        )

        if file_path:
            try:
                self.current_pdf_path = file_path
                # Convert file path to URL with page-width zoom setting
                pdf_url = QUrl.fromLocalFile(file_path)
                pdf_url.setFragment(
                    "zoom=page-width"
                )  # This sets initial zoom to fit page width
                self.web_view.setUrl(pdf_url)
            except Exception as e:
                QMessageBox.warning(self, "エラー", f"PDFを開けませんでした: {e}")
