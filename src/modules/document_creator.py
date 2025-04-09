"""
Document Creator module for the PyQt6 desktop application.
Provides a document creation interface with AI-powered editing and assistance.
"""

import os
from typing import Literal, Optional, Dict, Any, Union
from enum import Enum
from threading import Thread

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QPushButton,
    QSplitter,
    QComboBox,
    QLabel,
    QFrame,
    QSizePolicy,
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QFont, QTextCursor

from pydantic import BaseModel, Field

# Import AI agent for document processing
from modules.ai_agent import DocumentAIAgent, DocumentResponse


class ProcessingMode(str, Enum):
    """Enum for processing modes"""

    ASK = "ask"
    EDIT = "edit"


class DocumentRequest(BaseModel):
    """
    Request model for document processing
    """

    mode: ProcessingMode
    prompt: str
    content: str = Field(default="")


class ChatBubble(QFrame):
    """Widget for displaying chat messages in the Document Creator"""

    def __init__(self, message_text: str, is_user: bool, parent=None):
        super().__init__(parent)
        self.setObjectName("ChatBubble")

        # Configure frame appearance
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)
        self.setStyleSheet(
            # f"background-color: {'#e1ffc7' if is_user else '#ffffff'}; "
            f"border-radius: 10px; "
            f"padding: 5px; "
            f"margin: 0px 5px 0px 5px; "
        )

        # Create layout
        layout = QVBoxLayout()
        layout.setContentsMargins(2, 2, 2, 2)

        # Add message text
        self.message = QTextEdit()
        self.message.setReadOnly(True)
        self.message.setText(message_text)
        self.message.setStyleSheet(
            "background-color: transparent; border: none; color: #222222; padding: 0px;"
        )

        # Adjust height based on content
        self.message.document().documentLayout().documentSizeChanged.connect(
            self.adjust_text_edit_height
        )

        layout.addWidget(self.message)
        self.setLayout(layout)

        # Set maximum width based on parent
        if parent:
            self.setMaximumWidth(int(parent.width() * 0.8))

    def adjust_text_edit_height(self):
        """Adjust QTextEdit height based on content"""
        doc_height = self.message.document().size().height()
        self.message.setFixedHeight(int(doc_height + 5))


class DocumentCreator(QWidget):
    """
    Document Creator widget that provides an interface for creating and editing documents
    with AI assistance.

    Features:
    - Split view with AI chat on the left and document editor on the right
    - Support for asking questions about the document content
    - Support for AI-powered document editing based on user instructions
    """

    # Signal for background AI responses
    response_received = pyqtSignal(DocumentResponse)

    def __init__(self, parent=None):
        """
        Initialize the Document Creator widget.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.ai_agent = DocumentAIAgent()
        self.setup_ui()

        # Connect signal to slots
        self.response_received.connect(self.on_ai_response)

    def setup_ui(self):
        """Set up the user interface components."""
        main_layout = QVBoxLayout(self)

        # Create a splitter for the main widgets
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.setSizes([1, 2])  # 1:2 ratio for left:right areas

        # Left side - Chat interface
        self.chat_widget = QWidget()
        chat_layout = QVBoxLayout(self.chat_widget)

        # Chat history - messages area
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        chat_layout.addWidget(self.chat_history)

        # Mode selector
        mode_layout = QHBoxLayout()
        mode_label = QLabel("モード:")
        self.mode_selector = QComboBox()
        self.mode_selector.addItem("質問する", ProcessingMode.ASK)
        self.mode_selector.addItem("テキスト編集", ProcessingMode.EDIT)
        mode_layout.addWidget(mode_label)
        mode_layout.addWidget(self.mode_selector)
        mode_layout.addStretch()
        chat_layout.addLayout(mode_layout)

        # Chat input area
        self.chat_input = QTextEdit()
        self.chat_input.setPlaceholderText("AIアシスタントへの指示を入力...")
        self.chat_input.setMaximumHeight(100)
        chat_layout.addWidget(self.chat_input)

        # Send button
        self.send_button = QPushButton("送信")
        self.send_button.clicked.connect(self.process_request)
        chat_layout.addWidget(self.send_button)

        # Right side - Document editor
        self.editor_widget = QWidget()
        editor_layout = QVBoxLayout(self.editor_widget)

        self.document_editor = QTextEdit()
        self.document_editor.setPlaceholderText("ここにテキストを入力または編集...")
        editor_layout.addWidget(self.document_editor)

        # Add both widgets to the splitter
        self.splitter.addWidget(self.chat_widget)
        self.splitter.addWidget(self.editor_widget)

        main_layout.addWidget(self.splitter)

        # Add welcome message
        self.add_message(
            "こんにちは！書類作成アシスタントです。テキストエリアに文章を入力して、質問や編集指示をしてください。",
            False,
        )

    def add_message(self, text: str, is_user: bool):
        """Add a message to the chat history"""
        # Create cursor for inserting text
        cursor = self.chat_history.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)

        # Set alignment based on who's sending the message
        format = cursor.blockFormat()
        if is_user:
            format.setAlignment(Qt.AlignmentFlag.AlignRight)
        else:
            format.setAlignment(Qt.AlignmentFlag.AlignLeft)
        cursor.setBlockFormat(format)

        # Create message bubble with background color and styling
        bubble_style = (
            "border-radius: 10px; padding: 5px;"
            if is_user
            else "border-radius: 10px; padding: 5px;"
        )
        message_html = f"""
        <div style="{bubble_style}; margin: 5px; display: inline-block; max-width: 80%; text-align: left;">
            {text}
        </div>
        """

        # Insert HTML and a new line
        cursor.insertHtml(message_html)
        cursor.insertBlock()

        # Set cursor position to the end
        self.chat_history.setTextCursor(cursor)

        # Scroll to bottom
        self.chat_history.verticalScrollBar().setValue(
            self.chat_history.verticalScrollBar().maximum()
        )

    def process_request(self):
        """Process the user request based on selected mode"""
        prompt = self.chat_input.toPlainText().strip()
        if not prompt:
            return

        # Get the current mode
        mode = self.mode_selector.currentData()
        content = self.document_editor.toPlainText()

        # Add user message to chat history
        self.add_message(prompt, True)

        # Clear input
        self.chat_input.clear()

        # Create request model
        request = DocumentRequest(mode=mode, prompt=prompt, content=content)

        # Process in background thread
        self.process_in_background(request)

    def process_in_background(self, request: DocumentRequest):
        """Process document request in a background thread"""

        def _process():
            try:
                # Process with DocumentAIAgent
                is_edit_mode = request.mode == ProcessingMode.EDIT
                response = self.ai_agent.process_document_request(
                    prompt=request.prompt,
                    content=request.content,
                    is_edit_mode=is_edit_mode,
                )

                # Send response to main thread
                self.response_received.emit(response)

            except Exception as e:
                error_response = DocumentResponse(
                    message=f"エラーが発生しました: {str(e)}", edited_content=None
                )
                self.response_received.emit(error_response)

        Thread(target=_process, daemon=True).start()

    def on_ai_response(self, response: DocumentResponse):
        """Handle AI response from background thread"""
        # Always display the message in chat history
        self.add_message(response.message, False)

        # If there's edited content, update the document editor
        if response.edited_content:
            self.document_editor.setText(response.edited_content)
