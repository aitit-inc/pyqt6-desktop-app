"""
AI Chat module for the PyQt6 desktop application.
Provides a chat interface with an AI powered by LangGraph and OpenAI.
"""

import os
import sys
from typing import Any, Dict, List, Optional
from threading import Thread
from queue import Queue

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QPushButton,
    QScrollArea,
    QFrame,
    QSizePolicy,
    QSpacerItem,
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QIcon, QPixmap, QFont, QColor
from PyQt6.QtCore import QObject, QEvent

# Import the AI agent
from modules.ai_agent import AIAgent


# Define message bubble widget for displaying chat messages
class MessageBubble(QFrame):
    """Widget for displaying chat messages as bubbles"""

    def __init__(self, message_text: str, is_user: bool, parent=None):
        super().__init__(parent)
        self.setObjectName("MessageBubble")
        self.is_user = is_user

        # Configure frame appearance
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)
        self.setStyleSheet(
            f"background-color: {'#e1ffc7' if is_user else '#ffffff'}; "
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
        # 文字色を濃いグレー(#222222)に設定（真っ黒より少し明るい）
        self.message.setStyleSheet(
            "background-color: transparent; border: none; color: #222222; padding: 0px;"
        )

        # Adjust the message height based on content
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


class AutoResizingTextEdit(QTextEdit):
    """Text edit that automatically resizes within specified bounds"""

    def __init__(self, min_height=50, max_height=120, parent=None):
        super().__init__(parent)
        self.min_height = min_height
        self.max_height = max_height
        self.setMinimumHeight(min_height)
        self.setMaximumHeight(max_height)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        # Connect document size changes to height adjustment
        self.document().documentLayout().documentSizeChanged.connect(self.adjust_height)

    def adjust_height(self):
        """Adjust height based on content, within specified bounds"""
        doc_height = self.document().size().height()
        height = max(self.min_height, min(int(doc_height + 10), self.max_height))
        self.setFixedHeight(height)


class ChatHistory(QScrollArea):
    """Scrollable area for displaying chat history"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)

        # Create container widget
        self.container = QWidget()
        self.layout = QVBoxLayout(self.container)
        self.layout.setSpacing(15)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.addStretch()

        self.setWidget(self.container)

    def add_message(self, message_text: str, is_user: bool):
        """Add a message to the chat history"""
        # Create message layout
        msg_layout = QHBoxLayout()
        msg_layout.setContentsMargins(0, 0, 0, 0)

        # Create message bubble
        message = MessageBubble(message_text, is_user, self)

        # Add spacer and message to align left/right
        if is_user:
            msg_layout.addStretch()
            msg_layout.addWidget(message)
        else:
            msg_layout.addWidget(message)
            msg_layout.addStretch()

        # Insert message before the stretch
        self.layout.insertLayout(self.layout.count() - 1, msg_layout)

        # Scroll to bottom
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())


class AIChat(QWidget):
    """
    AI Chat widget that provides an interface to interact with an AI assistant.
    Uses LangGraph and OpenAI for chat functionality.
    """

    # Signal for background AI responses
    response_received = pyqtSignal(str)

    def __init__(self, parent=None):
        """
        Initialize the AI Chat widget.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.setup_ui()

        # Create AI agent instance
        self.ai_agent = AIAgent()

        # Connect signal to slot
        self.response_received.connect(self.on_ai_response)

    def setup_ui(self):
        """
        Set up the user interface components.
        """
        layout = QVBoxLayout()

        # Chat history area
        self.chat_history = ChatHistory()
        layout.addWidget(self.chat_history)

        # Input area
        input_layout = QHBoxLayout()

        # Text input
        self.text_input = AutoResizingTextEdit(min_height=50, max_height=120)
        self.text_input.setPlaceholderText("メッセージを入力...")

        # Install event filter to handle Enter key
        self.text_input.installEventFilter(self)

        # Send button
        self.send_button = QPushButton()
        self.send_button.setIcon(self.create_up_arrow_icon())
        self.send_button.setFixedSize(50, 50)
        self.send_button.setStyleSheet(
            "background-color: #128C7E; border-radius: 25px;"
        )
        self.send_button.clicked.connect(self.send_message)

        # Add widgets to layout
        input_layout.addWidget(self.text_input)
        input_layout.addWidget(self.send_button)

        layout.addLayout(input_layout)
        self.setLayout(layout)

        # Add welcome message
        self.chat_history.add_message(
            "こんにちは！AIアシスタントです。何かお手伝いできることはありますか？",
            False,
        )

    def create_up_arrow_icon(self):
        """Create an up arrow icon for the send button"""
        # Create a simple up arrow using QPixmap
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.GlobalColor.transparent)
        return (
            QIcon(":/icons/send.png")
            if QIcon(":/icons/send.png").availableSizes()
            else QIcon.fromTheme("go-up")
        )

    def eventFilter(self, obj, event):
        """Handle events for child widgets"""
        if obj is self.text_input and event.type() == QEvent.Type.KeyPress:
            if (
                event.key() == Qt.Key.Key_Return
                and not event.modifiers() & Qt.KeyboardModifier.ShiftModifier
            ):
                self.send_message()
                return True

        return super().eventFilter(obj, event)

    def send_message(self):
        """Send the user message to the AI agent"""
        message = self.text_input.toPlainText().strip()
        if not message:
            return

        # Add user message to chat history
        self.chat_history.add_message(message, True)

        # Clear input
        self.text_input.clear()

        # Process message in background thread
        self.process_message_async(message)

    def process_message_async(self, message):
        """Process the message in a background thread"""

        def _process():
            response = self.ai_agent.process_message(message)
            self.response_received.emit(response)

        Thread(target=_process, daemon=True).start()

    def on_ai_response(self, response):
        """Handle AI response from background thread"""
        self.chat_history.add_message(response, False)
